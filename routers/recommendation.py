"""
routers/recommendation.py
Rotas do motor híbrido de recomendação e do ciclo contínuo de feedback com DIP.
"""

from fastapi import APIRouter, Request, Query, HTTPException, status
from dependencies import limiter, get_motor, get_repository
from schemas.recommendation import (
    ClienteProfile,
    FeedbackInput,
    RecomendacaoResponse,
    FeedbackResponse,
)
from catalog import CATALOGO_PRODUTOS

router = APIRouter(tags=["Recomendação"])


@router.post("/recommend", response_model=RecomendacaoResponse)
@limiter.limit("10/minute")
def recommend_products(
    request: Request, 
    perfil: ClienteProfile, 
    top_k: int = Query(default=3, ge=1, le=50, description="Quantidade de produtos recomendados (1 a 50)")
):
    """
    Recebe o perfil capilar da cliente (Totem/App) e gera o Top K produtos recomendados
    com pontuação híbrida e justificativa explicável (XAI).
    """
    motor = get_motor(request)
    dados_cliente = perfil.to_dict()
    resultado = motor.recomendar(dados_cliente, top_k=top_k)
    return resultado


@router.post("/feedback", response_model=FeedbackResponse, tags=["Feedback Loop"])
@limiter.limit("10/minute")
def register_feedback(request: Request, feedback: FeedbackInput):
    """
    Registra a avaliação pós-atendimento (1 a 5 estrelas) da cliente.
    Atualiza o repositório desacoplado e recalibra a Média Bayesiana do cluster.
    """
    motor = get_motor(request)
    repo = get_repository(request)

    # 1. Valida se o produto existe no catálogo
    nomes_validos = [p["nome"] for p in CATALOGO_PRODUTOS]
    if feedback.nome_produto not in nomes_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Produto '{feedback.nome_produto}' não encontrado no catálogo oficial da Vila Cachos."
        )

    # 2. Registra o feedback no motor em memória
    dados_cliente = feedback.perfil_cliente.to_dict()
    motor.registrar_feedback(dados_cliente, feedback.nome_produto, feedback.nota_satisfacao)

    # 3. Prediz cluster e persiste via Repositório (DIP)
    cluster_id = motor.prever_cluster(dados_cliente)
    repo.salvar_feedback(
        perfil_cliente=dados_cliente,
        nome_produto=feedback.nome_produto,
        nota_satisfacao=feedback.nota_satisfacao,
        cluster_id=cluster_id
    )

    return FeedbackResponse(
        status="sucesso",
        mensagem=f"Avaliação {feedback.nota_satisfacao}★ registrada para o produto '{feedback.nome_produto}'. Pesos do Cluster {cluster_id} recalibrados!",
        cluster_afetado=cluster_id,
        total_avaliacoes_base=repo.obter_total_avaliacoes(),
        media_global_atualizada=round(motor.media_global_salao, 2)
    )
