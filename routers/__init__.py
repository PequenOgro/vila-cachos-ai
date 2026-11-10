"""
Camada de Rotas da API (FastAPI APIRouter).
Decomposição modular por domínio: Saúde, Catálogo, Recomendação e Visão Computacional.
"""

from .health import router as health_router
from .catalog import router as catalog_router
from .recommendation import router as recommendation_router
from .vision import router as vision_router

__all__ = [
    "health_router",
    "catalog_router",
    "recommendation_router",
    "vision_router",
]
