"""
schemas/health.py
Modelos Pydantic para monitoramento e métricas de integridade da API.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    motor_carregado: bool
    total_clientes_historico: int
    media_satisfacao_global: float
    num_clusters: int
    silhouette_score: float
