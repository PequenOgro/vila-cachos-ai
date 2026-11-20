"""
dependencies.py
Provedores de dependências compartilhadas, rate limiting e injeção de serviços da API.
"""

import logging
import sys
import threading
from fastapi import Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from fastapi import FastAPI
    from recommender_engine import VilaCachosRecommender
    from repositories.feedback_repository import FeedbackRepository

logger = logging.getLogger("vila_cachos.dependencies")
_init_lock = threading.Lock()

def get_client_ip(request: Request) -> str:
    """Extrai o IP real do cliente com suporte seguro a proxies reversos (Vercel, Render, Cloudflare)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
        if client_ip:
            return client_ip
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


limiter = Limiter(key_func=get_client_ip)


def ensure_motor_and_repo(
    target_app: "FastAPI",
) -> Tuple[Optional["FeedbackRepository"], Optional["VilaCachosRecommender"]]:
    """Inicializa preguiçosamente (thread-safe) o repositório CSV e o motor K-Means sob demanda."""
    curr_repo = getattr(target_app.state, "repo", None)
    curr_motor = getattr(target_app.state, "motor", None)
    if getattr(target_app.state, "_disable_lazy_init", False):
        return curr_repo, curr_motor
    if curr_repo is not None and curr_motor is not None:
        return curr_repo, curr_motor

    with _init_lock:
        curr_repo = getattr(target_app.state, "repo", None)
        curr_motor = getattr(target_app.state, "motor", None)
        if getattr(target_app.state, "_disable_lazy_init", False):
            return curr_repo, curr_motor

        api_mod = sys.modules.get("api")

        if curr_repo is None:
            try:
                from repositories.feedback_repository import CsvFeedbackRepository

                curr_repo = CsvFeedbackRepository()
                target_app.state.repo = curr_repo
                if api_mod is not None and getattr(api_mod, "app", None) is target_app:
                    api_mod.repo = curr_repo
            except Exception as exc:
                logger.error(f"[!] Falha ao inicializar repositório CSV: {exc}", exc_info=True)
                curr_repo = None
                target_app.state.repo = None

        if curr_motor is None and curr_repo is not None:
            try:
                if api_mod is not None and hasattr(api_mod, "carregar_e_treinar_motor"):
                    curr_motor = api_mod.carregar_e_treinar_motor(curr_repo)
                else:
                    from recommender_engine import VilaCachosRecommender

                    df_historico = curr_repo.obter_historico()
                    curr_motor = VilaCachosRecommender(n_clusters=4, random_state=42)
                    curr_motor.fit(df_historico, copy=False)
                    del df_historico
                target_app.state.motor = curr_motor
                if api_mod is not None and getattr(api_mod, "app", None) is target_app:
                    api_mod.motor = curr_motor
            except Exception as exc:
                logger.error(f"[!] Falha ao inicializar motor de recomendação: {exc}", exc_info=True)
                curr_motor = None
                target_app.state.motor = None

        return curr_repo, curr_motor


def get_motor(request: Request) -> "VilaCachosRecommender":
    """Obtém a instância do motor de recomendação treinado a partir do app.state."""
    motor = getattr(request.app.state, "motor", None)
    if motor is None:
        _, motor = ensure_motor_and_repo(request.app)
    if motor is None or not getattr(motor, "is_fitted", False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Motor de recomendação ainda não foi treinado ou está indisponível."
        )
    return motor


def get_repository(request: Request) -> "FeedbackRepository":
    """Obtém o repositório de persistência de feedbacks a partir do app.state."""
    repo = getattr(request.app.state, "repo", None)
    if repo is None:
        repo, _ = ensure_motor_and_repo(request.app)
    if repo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Repositório de persistência de feedbacks não inicializado."
        )
    return repo
