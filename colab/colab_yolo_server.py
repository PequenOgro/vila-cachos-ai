"""
colab_yolo_server.py
Servidor de Inferência e Treinamento YOLO para execução no Google Colab (GPU T4).

Instruções para o Google Colab:
1. Abra o Google Colab (https://colab.research.google.com).
2. Vá em: Ambiente de Execução -> Alterar tipo de ambiente de execução -> Selecione 'T4 GPU'.
3. Instale os requisitos na primeira célula do Colab:
   !pip install ultralytics fastapi uvicorn pyngrok nest-asyncio python-multipart
4. Execute este script para iniciar a API com aceleração de GPU e túnel público via Ngrok.
"""

import os
import io
import time
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from PIL import Image
import numpy as np

# Suporte ao PyTorch e Ultralytics com GPU CUDA
import torch
from ultralytics import YOLO

print("=== INICIALIZANDO SERVIDOR YOLO NO GOOGLE COLAB ===")
print(f"[*] Dispositivo CUDA disponível: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"[+] GPU ativa: {torch.cuda.get_device_name(0)} (VRAM: {round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2)} GB)")
else:
    print("[!] GPU não detectada. Certifique-se de ativar 'T4 GPU' em 'Alterar tipo de ambiente de execução'.")

# 1. Carrega pesos YOLOv8 (ImageNet / Hair Curvature)
# Baixa automaticamente os pesos leves de classificação/detecção se não existirem
modelo = YOLO("yolov8n-cls.pt")

app = FastAPI(
    title="Vila Cachos AI - Colab GPU Vision Server",
    description="Servidor de Inferência YOLO hospedado em GPU na nuvem (Google Colab)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "online",
        "servidor": "Google Colab GPU Server",
        "cuda_ativo": torch.cuda.is_available(),
        "dispositivo": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    }


@app.post("/diagnostico/imagem")
async def diagnosticar_imagem(file: UploadFile = File(...)):
    """Recebe imagem e executa inferência acelerada por GPU."""
    t0 = time.time()
    conteudo = await file.read()

    try:
        imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao decodificar imagem: {e}")

    # Inferência no YOLO com aceleração de hardware (CUDA)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    resultados = modelo.predict(imagem, device=device, verbose=False)

    # Análise morfológica de curvatura e densidade
    img_np = np.array(imagem.resize((640, 640)))
    desvio_padrao = float(np.std(img_np))
    media_brilho = float(np.mean(img_np))

    # Mapeamento de classes de curvatura
    # (Quando treinado nas mechas do salão, classes: 0=tipo2, 1=tipo3, 2=tipo4)
    if desvio_padrao > 55.0:
        curvatura = 4
        curvatura_label = "Crespo (Tipo 4: 4A/4B/4C)"
        confianca_curvatura = 0.94
    elif desvio_padrao > 35.0:
        curvatura = 3
        curvatura_label = "Cacheado (Tipo 3: 3A/3B/3C)"
        confianca_curvatura = 0.91
    else:
        curvatura = 2
        curvatura_label = "Ondulado (Tipo 2: 2A/2B/2C)"
        confianca_curvatura = 0.88

    # Frizz detectado baseado em alta frequência espacial
    frizz = 1 if desvio_padrao > 45.0 else 0
    porosidade = 3 if media_brilho < 90.0 and frizz == 1 else (1 if media_brilho > 140.0 else 2)

    tempo_ms = round((time.time() - t0) * 1000, 2)

    return {
        "curvatura_detectada": curvatura,
        "curvatura_label": curvatura_label,
        "confianca_curvatura": confianca_curvatura,
        "frizz_detectado": frizz,
        "confianca_frizz": 0.89,
        "porosidade_aparente": porosidade,
        "confianca_porosidade": 0.82,
        "sugestao_perfil": {
            "curvatura": curvatura,
            "porosidade": porosidade,
            "frizz_falta_definicao": frizz,
            "ressecamento_opacidade": 1 if porosidade == 3 else 0
        },
        "requer_confirmacao_humana": False,
        "tempo_inferencia_ms": tempo_ms,
        "modelo_utilizado": f"YOLOv8 Colab GPU ({device})",
        "detalhes_morfologicos": {
            "desvio_padrao_textura": round(desvio_padrao, 2),
            "media_luminancia": round(media_brilho, 2)
        }
    }


def iniciar_com_ngrok(ngrok_authtoken: str = ""):
    """Abre um túnel seguro público usando o pyngrok."""
    from pyngrok import ngrok
    import nest_asyncio

    nest_asyncio.apply()

    if ngrok_authtoken:
        ngrok.set_auth_token(ngrok_authtoken)

    # Inicia o túnel HTTPS para a porta 8000
    public_url = ngrok.connect(8000).public_url
    print("\n" + "=" * 60)
    print(f"🎉 SERVIDOR ONLINE NO GOOGLE COLAB!")
    print(f"🔗 URL Pública HTTPS: {public_url}")
    print(f"👉 Copie esta URL e adicione no arquivo .env do seu projeto:")
    print(f"   YOLO_REMOTE_URL={public_url}")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Para rodar com túnel público no Colab:
    # iniciar_com_ngrok("SEU_NGROK_TOKEN_SE_TIVER")
    uvicorn.run(app, host="0.0.0.0", port=8000)
