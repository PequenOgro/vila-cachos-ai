"""
api.py
Camada de API RESTful (FastAPI) para o Sistema de Recomendação Vila Cachos.

Expõe o motor híbrido de recomendação e o ciclo de feedback com validação estrita (Pydantic).
"""

import os
import pandas as pd
from typing import List, Dict, Any, Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field

from catalog import CATALOGO_PRODUTOS, TAXONOMIA_QUEIXAS
from generate_dataset import gerar_dataset_causal
from recommender_engine import VilaCachosRecommender

# Caminho do banco de dados analítico (CSV) - resolução absoluta para nuvem/Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DATASET_PATH = os.path.join(BASE_DIR, "dataset_historico_vila_cachos.csv")

# Instância global do motor
motor: VilaCachosRecommender = None


def carregar_e_treinar_motor() -> VilaCachosRecommender:
    """Inicializa ou carrega a base histórica e ajusta o motor de recomendação."""
    if not os.path.exists(CSV_DATASET_PATH):
        print(f"[*] Gerando dataset histórico inicial causal...")
        df_inicial = gerar_dataset_causal(num_clientes=1000, seed=42)
        df_inicial.to_csv(CSV_DATASET_PATH, index=False, encoding="utf-8")
    else:
        print(f"[*] Carregando dataset existente de '{CSV_DATASET_PATH}'...")
        df_inicial = pd.read_csv(CSV_DATASET_PATH)

    rec_motor = VilaCachosRecommender(n_clusters=4, random_state=42)
    rec_motor.fit(df_inicial)
    print(f"[+] Motor treinado com sucesso! {len(df_inicial)} clientes no histórico.")
    return rec_motor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia a inicialização e encerramento dos recursos da API."""
    global motor
    motor = carregar_e_treinar_motor()
    yield


# Inicialização do App FastAPI
app = FastAPI(
    title="Vila Cachos - Recommender API",
    description="Motor Inteligente Híbrido de Recomendação de Cosméticos e Tratamentos para Cabelos Cacheados (TCC)",
    version="1.0.0",
    lifespan=lifespan
)

# Inicialização do Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuração de CORS para comunicação com o front-end (Totem UI / Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (Vercel, Totem local, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# SCHEMAS PYDANTIC (VALIDAÇÃO ESTRITA)
# =====================================================================

class ClienteProfile(BaseModel):
    curvatura: Literal[2, 3, 4] = Field(
        ..., 
        description="Tipo de curvatura do fio: 2=Ondulado, 3=Cacheado, 4=Crespo",
        example=3
    )
    porosidade: Literal[1, 2, 3] = Field(
        ..., 
        description="Nível de porosidade capilar: 1=Baixa, 2=Média, 3=Alta",
        example=3
    )
    dano_quimico: Literal[0, 1] = Field(
        ..., 
        description="Presença de química agressiva (descoloração/alisamento): 0=Não, 1=Sim",
        example=1
    )
    ressecamento_opacidade: Literal[0, 1] = Field(
        0, 
        description="Queixa: Fios ressecados, ásperos e sem brilho (0=Não, 1=Sim)"
    )
    alta_porosidade_quimica: Literal[0, 1] = Field(
        0, 
        description="Queixa: Fios porosos, elásticos ou quebradiços pós-química (0=Não, 1=Sim)"
    )
    frizz_falta_definicao: Literal[0, 1] = Field(
        0, 
        description="Queixa: Cachos desmanchando rápido e frizz excessivo (0=Não, 1=Sim)"
    )
    transicao_capilar: Literal[0, 1] = Field(
        0, 
        description="Queixa: Fios em transição com duas texturas (0=Não, 1=Sim)"
    )
    couro_sensivel_oleoso: Literal[0, 1] = Field(
        0, 
        description="Queixa: Raiz oleosa ou couro cabeludo sensibilizado (0=Não, 1=Sim)"
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class FeedbackInput(BaseModel):
    perfil_cliente: ClienteProfile = Field(..., description="Perfil capilar e queixas da cliente atendida")
    nome_produto: str = Field(
        ..., 
        description="Nome exato do produto recomendado/utilizado",
        example="Curly Care ACID-C (Acidificante Antiporosidade)"
    )
    nota_satisfacao: int = Field(
        ..., 
        ge=1, 
        le=5, 
        description="Nota explícita de satisfação pós-atendimento (1 a 5)",
        example=5
    )


class RecomendacaoItem(BaseModel):
    produto_id: str
    nome: str
    categoria: str
    score_final: float
    estrelas_estimadas: float
    score_conteudo: float
    score_feedback_bayesiano: float
    avaliacoes_cluster: int
    motivo: str
    descricao: str


class RecomendacaoResponse(BaseModel):
    cluster_id: int
    descricao_persona: str
    peso_conhecimento_vs_feedback: Dict[str, float]
    recomendacoes: List[RecomendacaoItem]


class FeedbackResponse(BaseModel):
    status: str
    mensagem: str
    cluster_afetado: int
    total_avaliacoes_base: int
    media_global_atualizada: float


class HealthResponse(BaseModel):
    status: str
    motor_carregado: bool
    total_clientes_historico: int
    media_satisfacao_global: float
    num_clusters: int
    silhouette_score: float


# =====================================================================
# ROTAS DA API
# =====================================================================

@app.get("/", tags=["Geral"])
def root():
    """Rota raiz com status da API e link para a documentação interativa (Swagger)."""
    return {
        "status": "online",
        "api": "Vila Cachos - Recommender API",
        "versao": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def check_health():
    """Verifica se a API e o motor de recomendação estão operacionais e retorna métricas do modelo."""
    if motor is None or not motor.is_fitted:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Motor de recomendação não carregado."
        )
    
    metricas = motor.avaliar_qualidade_clusters()
    return HealthResponse(
        status="operacional",
        motor_carregado=True,
        total_clientes_historico=len(motor.df_historico),
        media_satisfacao_global=round(motor.media_global_salao, 2),
        num_clusters=metricas["num_clusters"],
        silhouette_score=metricas["silhouette_score"]
    )


@app.post("/recommend", response_model=RecomendacaoResponse, tags=["Recomendação"])
@limiter.limit("10/minute")
def recommend_products(request: Request, perfil: ClienteProfile, top_k: int = 3):
    """
    Recebe o perfil capilar da cliente (Totem/App) e gera o Top K produtos recomendados
    com pontuação híbrida e justificativa explicável (XAI).
    """
    if motor is None or not motor.is_fitted:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Motor de recomendação ainda não foi treinado."
        )

    dados_cliente = perfil.to_dict()
    resultado = motor.recomendar(dados_cliente, top_k=top_k)
    return resultado


@app.post("/feedback", response_model=FeedbackResponse, tags=["Feedback Loop"])
@limiter.limit("10/minute")
def register_feedback(request: Request, feedback: FeedbackInput):
    """
    Registra a avaliação pós-atendimento (1 a 5 estrelas) da cliente.
    Atualiza o histórico persistente (CSV) e recalibra a Média Bayesiana do cluster.
    """
    if motor is None or not motor.is_fitted:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Motor de recomendação indisponível."
        )

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

    # 3. Persiste a nova avaliação no CSV histórico
    motor.df_historico.to_csv(CSV_DATASET_PATH, index=False, encoding="utf-8")

    cluster_id = motor.prever_cluster(dados_cliente)

    return FeedbackResponse(
        status="sucesso",
        mensagem=f"Avaliação {feedback.nota_satisfacao}★ registrada para o produto '{feedback.nome_produto}'. Pesos do Cluster {cluster_id} recalibrados!",
        cluster_afetado=cluster_id,
        total_avaliacoes_base=len(motor.df_historico),
        media_global_atualizada=round(motor.media_global_salao, 2)
    )


@app.get("/catalogo", tags=["Catálogo"])
def list_catalogo():
    """Retorna o catálogo completo de produtos disponíveis na Vila Cachos."""
    return CATALOGO_PRODUTOS


if __name__ == "__main__":
    import uvicorn
    # Render atribui dinamicamente a variável PORT no ambiente
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
