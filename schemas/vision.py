"""
schemas/vision.py
Modelos Pydantic para diagnóstico e inferência visual de curvatura/frizz.
"""

from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel


class VisionPerfilSugestao(BaseModel):
    curvatura: Literal[2, 3, 4]
    porosidade: Literal[1, 2, 3]
    frizz_falta_definicao: Literal[0, 1]
    ressecamento_opacidade: Literal[0, 1]


class VisionDiagnosisResponse(BaseModel):
    cabelo_detectado: bool = True
    mensagem_alerta: Optional[str] = None
    curvatura_detectada: Optional[Literal[2, 3, 4]] = None
    curvatura_label: str
    confianca_curvatura: float = 0.0
    frizz_detectado: Optional[Literal[0, 1]] = None
    confianca_frizz: float = 0.0
    porosidade_aparente: Optional[Literal[1, 2, 3]] = None
    confianca_porosidade: float = 0.0
    sugestao_perfil: Optional[VisionPerfilSugestao] = None
    requer_confirmacao_humana: bool = True
    tempo_inferencia_ms: float
    modelo_utilizado: str
    detalhes_morfologicos: Dict[str, Any]
