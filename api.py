"""
api.py
Camada Principal de API RESTful (FastAPI) para o Sistema de Recomendação Vila Cachos.

Estrutura Refatorada (Clean Architecture):
- Orquestrador desacoplado e enxuto (< 90 linhas).
- Rotas modularizadas via APIRouter em routers/.
- Contratos de dados em schemas/.
- Persistência desacoplada em repositories/ (DIP).
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from dependencies import limiter
from repositories.feedback_repository import CsvFeedbackRepository, FeedbackRepository
from recommender_engine import VilaCachosRecommender
from routers import health_router, catalog_router, recommendation_router, vision_router

# Re-exportações para preservar compatibilidade estrita
from schemas import (
    ClienteProfile,
    FeedbackInput,
    RecomendacaoItem,
    RecomendacaoResponse,
    FeedbackResponse,
    HealthResponse,
    VisionPerfilSugestao,
    VisionDiagnosisResponse,
)

# Instâncias globais de compatibilidade
repo: FeedbackRepository = None
motor: VilaCachosRecommender = None


def carregar_e_treinar_motor(repositorio: FeedbackRepository) -> VilaCachosRecommender:
    """Inicializa ou carrega a base histórica do repositório e treina o motor."""
    df_historico = repositorio.obter_historico()
    rec_motor = VilaCachosRecommender(n_clusters=4, random_state=42)
    rec_motor.fit(df_historico)
    print(f"[+] Motor treinado com sucesso! {len(df_historico)} clientes no histórico.")
    return rec_motor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia a inicialização e encerramento dos recursos da API."""
    global repo, motor
    repo = CsvFeedbackRepository()
    motor = carregar_e_treinar_motor(repo)
    app.state.repo = repo
    app.state.motor = motor
    yield


app = FastAPI(
    title="Vila Cachos - Recommender API",
    description="Motor Inteligente Híbrido de Recomendação de Cosméticos e Tratamentos para Cabelos Cacheados (TCC)",
    version="1.0.0",
    lifespan=lifespan
)

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("vila_cachos.api")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Aplica cabeçalhos de segurança padrão OWASP para proteção contra MIME-sniffing, clickjacking e XSS."""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Evita vazamento de stack traces ou detalhes internos do sistema operacional para o cliente."""
    logger.error(f"[!] Erro não tratado em {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno no servidor ao processar a requisição."}
    )


app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Inclusão modular de roteadores
app.include_router(health_router)
app.include_router(catalog_router)
app.include_router(recommendation_router)
app.include_router(vision_router)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
