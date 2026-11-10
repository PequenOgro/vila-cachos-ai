"""
schemas/recommendation.py
Modelos Pydantic para perfis de clientes, recomendações e feedback.
"""

from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field


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
    perfil_cliente: ClienteProfile = Field(
        ..., 
        alias="perfil", 
        description="Perfil capilar e queixas da cliente atendida"
    )
    nome_produto: str = Field(
        ..., 
        alias="produto_nome", 
        max_length=200,
        description="Nome exato do produto recomendado/utilizado",
        example="Curly Care ACID-C (Acidificante Antiporosidade)"
    )
    nota_satisfacao: int = Field(
        ..., 
        alias="nota", 
        ge=1, 
        le=5, 
        description="Nota explícita de satisfação pós-atendimento (1 a 5)",
        example=5
    )

    model_config = {
        "populate_by_name": True
    }


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
