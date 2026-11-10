"""
routers/catalog.py
Rotas para consulta ao catálogo oficial de cosméticos e tratamentos.
"""

from fastapi import APIRouter
from catalog import CATALOGO_PRODUTOS

router = APIRouter(tags=["Catálogo"])


@router.get("/catalogo")
def list_catalogo():
    """Retorna o catálogo completo de produtos disponíveis na Vila Cachos."""
    return CATALOGO_PRODUTOS
