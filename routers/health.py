"""
routers/health.py
Rotas de status raiz e verificação de integridade operacional do motor.
"""

from fastapi import APIRouter, Request, HTTPException, status
from schemas.health import HealthResponse

router = APIRouter(tags=["Monitoramento"])


@router.get("/", tags=["Geral"])
def root():
    """Rota raiz com status da API e link para a documentação interativa (Swagger)."""
    return {
        "status": "online",
        "api": "Vila Cachos - Recommender API",
        "versao": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthResponse)
def check_health(request: Request):
    """Verifica se a API e o motor de recomendação estão operacionais e retorna métricas do modelo."""
    motor = getattr(request.app.state, "motor", None)
    repo = getattr(request.app.state, "repo", None)

    if motor is None or not getattr(motor, "is_fitted", False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Motor de recomendação não carregado."
        )

    metricas = motor.avaliar_qualidade_clusters()
    total_clientes = repo.obter_total_avaliacoes() if repo else len(motor.df_historico)

    return HealthResponse(
        status="operacional",
        motor_carregado=True,
        total_clientes_historico=total_clientes,
        media_satisfacao_global=round(motor.media_global_salao, 2),
        num_clusters=metricas["num_clusters"],
        silhouette_score=metricas["silhouette_score"]
    )
