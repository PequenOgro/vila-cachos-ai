import os
import re
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status
from dependencies import limiter
from schemas.vision import VisionDiagnosisResponse
from vision_engine import classifier_instance

router = APIRouter(tags=["Visão Computacional (YOLO)"])


def verificar_magic_bytes_imagem(conteudo: bytes) -> bool:
    """Verifica as assinaturas binárias (magic bytes) para garantir integridade do tipo de imagem."""
    if len(conteudo) < 12:
        return False
    # JPEG (FF D8 FF)
    if conteudo.startswith(b"\xff\xd8\xff"):
        return True
    # PNG (89 50 4E 47 0D 0A 1A 0A)
    if conteudo.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    # WebP (RIFF .... WEBP)
    if conteudo.startswith(b"RIFF") and conteudo[8:12] == b"WEBP":
        return True
    return False


@router.post("/diagnostico/imagem", response_model=VisionDiagnosisResponse)
@limiter.limit("20/minute")
async def diagnosticar_imagem_capilar(request: Request, file: UploadFile = File(...)):
    """
    Recebe uma foto do cabelo da cliente (Totem / Web App), executa a inferência
    do modelo YOLO com análise morfológica e infere a curvatura, nível de frizz e
    sugestão de pré-preenchimento das 8 variáveis capilares.
    """
    # 1. Validação de formato MIME declarado
    formatos_permitidos = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in formatos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Formato '{file.content_type}' não suportado. Envie uma imagem JPEG, PNG ou WebP."
        )

    # 2. Leitura com controle de tamanho máximo (10MB)
    conteudo = await file.read()
    if len(conteudo) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="A imagem enviada excede o limite máximo permitido de 10MB."
        )

    # 3. Validação de Magic Bytes (impede arquivos maliciosos com MIME spoofado)
    if not verificar_magic_bytes_imagem(conteudo):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Conteúdo binário não corresponde a uma imagem válida (JPEG, PNG ou WebP)."
        )

    # 4. Sanitização contra Path Traversal no nome do arquivo
    nome_base = os.path.basename(file.filename or "amostra.jpg")
    nome_seguro = re.sub(r"[^a-zA-Z0-9_.-]", "_", nome_base)[:100] or "amostra.jpg"

    try:
        resultado = classifier_instance.predict_image_bytes(conteudo, filename=nome_seguro)
        return resultado
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Falha ao processar arquivo de imagem: {str(ve)}"
        )
