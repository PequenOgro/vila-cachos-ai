"""
dependencies.py
Provedores de dependências compartilhadas, rate limiting e injeção de serviços da API.
"""

from fastapi import Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recommender_engine import VilaCachosRecommender
    from repositories.feedback_repository import FeedbackRepository

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


def get_motor(request: Request) -> "VilaCachosRecommender":
    """Obtém a instância do motor de recomendação treinado a partir do app.state."""
    motor = getattr(request.app.state, "motor", None)
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
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Repositório de persistência de feedbacks não inicializado."
        )
    return repo
