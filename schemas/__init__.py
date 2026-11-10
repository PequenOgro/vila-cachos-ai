"""
Camada de Schemas Pydantic (Validação e Contratos de Dados).
"""

from .health import HealthResponse
from .recommendation import (
    ClienteProfile,
    FeedbackInput,
    RecomendacaoItem,
    RecomendacaoResponse,
    FeedbackResponse,
)
from .vision import (
    VisionPerfilSugestao,
    VisionDiagnosisResponse,
)

__all__ = [
    "HealthResponse",
    "ClienteProfile",
    "FeedbackInput",
    "RecomendacaoItem",
    "RecomendacaoResponse",
    "FeedbackResponse",
    "VisionPerfilSugestao",
    "VisionDiagnosisResponse",
]
