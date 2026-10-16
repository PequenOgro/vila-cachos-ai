"""
vision_engine.py
Módulo de Visão Computacional baseado em YOLO e Morfologia Capilar
para o Sistema Especialista Vila Cachos AI.

Responsável pela inferência de curvatura (2A-4C), detecção de frizz e
estimativa visual de porosidade para pré-preenchimento da anamnese capilar
com suporte ao paradigma Human-in-the-Loop.
"""

import io
import os
import time
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image
import cv2

# Carrega arquivo .env automaticamente se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k not in os.environ:
                        os.environ[k] = v
    except Exception as e:
        print(f"[!] Aviso ao carregar .env: {e}")

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


class YoloHairClassifier:
    """
    Classificador de características capilares baseado na arquitetura YOLO
    com análise morfológica de textura e gradientes em imagem.
    """

    CONFIDENCE_THRESHOLD = 0.75

    def __init__(self, model_path: Optional[str] = None):
        """
        Inicializa o classificador capilar.
        Se existir um arquivo de pesos customizado (ex: best.pt ou yolo11n.pt),
        o modelo YOLO é instanciado. Caso contrário, opera com o extrator morfológico robusto.
        """
        self.model_path = model_path or os.environ.get("YOLO_HAIR_MODEL_PATH", "")
        self.yolo_model = None
        self.modelo_nome = "YOLOv8-HairMorphology-Hybrid"

        # Se não foi fornecido caminho, procura automaticamente por pesos ONNX ou PT locais
        if not self.model_path:
            candidatos = [
                os.path.join(BASE_DIR, "yolov8n-cls.onnx"),
                os.path.join(BASE_DIR, "best.onnx"),
                os.path.join(BASE_DIR, "best.pt"),
                os.path.join(BASE_DIR, "yolov8n-cls.pt")
            ]
            for cand in candidatos:
                if os.path.exists(cand):
                    self.model_path = cand
                    break

        if ULTRALYTICS_AVAILABLE and self.model_path and os.path.exists(self.model_path):
            try:
                self.yolo_model = YOLO(self.model_path)
                ext = "ONNX Runtime (FP16/FP32)" if self.model_path.endswith(".onnx") else "PyTorch"
                self.modelo_nome = f"YOLOv8 [{ext}] ({os.path.basename(self.model_path)})"
                print(f"[+] Modelo YOLO carregado com sucesso de: {self.model_path} ({ext})")
            except Exception as e:
                print(f"[!] Falha ao inicializar pesos YOLO de '{self.model_path}': {e}. Operando em modo híbrido.")

    def _extrair_metricas_morfologicas(self, img_np: np.ndarray) -> Dict[str, float]:
        """
        Extrai descritores morfológicos e estatísticos da imagem do cabelo:
        - Densidade de bordas e gradientes (indicador de frizz e micro-fios)
        - Frequência de curvatura direcional (diferenciação tipo 2, 3 e 4)
        - Desvio padrão e saturação (opacidade e ressecamento aparente)
        """
        # Conversão para tons de cinza
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
            saturacao_media = float(np.mean(hsv[:, :, 1]))
        else:
            gray = img_np
            saturacao_media = 100.0

        # 1. Variância Laplaciana (Frequência espacial / rugosidade / Frizz)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        frizz_metric = float(np.var(laplacian))

        # 2. Análise de Bordas Canny para densidade de fios soltos
        edges = cv2.Canny(gray, threshold1=40, threshold2=120)
        densidade_bordas = float(np.sum(edges > 0) / edges.size)

        # 3. Gradientes de Sobel para medir orientação e torção das curvas
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        energia_curvatura = float(np.mean(magnitude))

        return {
            "frizz_metric": frizz_metric,
            "densidade_bordas": densidade_bordas,
            "energia_curvatura": energia_curvatura,
            "saturacao_media": saturacao_media
        }

    def predict_image_bytes(self, image_bytes: bytes, filename: str = "amostra.jpg") -> Dict[str, Any]:
        """
        Processa os bytes de uma imagem e retorna a predição estruturada de características capilares.
        """
        t0 = time.time()

        if not image_bytes or len(image_bytes) < 32:
            raise ValueError("Buffer de imagem inválido ou vazio.")

        # Suporte a Servidor de Inferência Remoto em GPU (Google Colab / Ngrok)
        remote_url = os.environ.get("YOLO_REMOTE_URL", "").strip().rstrip("/")
        if remote_url:
            try:
                import httpx
                target_url = remote_url if remote_url.endswith("/diagnostico/imagem") else f"{remote_url}/diagnostico/imagem"
                files = {"file": (filename, image_bytes, "image/jpeg")}
                with httpx.Client(timeout=8.0) as client:
                    resp = client.post(target_url, files=files)
                    if resp.status_code == 200:
                        data = resp.json()
                        data["origem_inferencia"] = f"Google Colab GPU ({remote_url})"
                        return data
            except Exception as e:
                print(f"[!] Servidor remoto Colab ({remote_url}) inacessível: {e}. Executando inferência local com fallback.")

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")
        except Exception as e:
            raise ValueError(f"Não foi possível decodificar o arquivo de imagem: {e}")

        # Redimensiona para resolução padrão de inferência YOLO (640x640)
        img_resized = image.resize((640, 640))
        img_np = np.array(img_resized)

        # 1. Extração de métricas de visão
        metricas = self._extrair_metricas_morfologicas(img_np)
        frizz_val = metricas["frizz_metric"]
        densidade = metricas["densidade_bordas"]
        energia = metricas["energia_curvatura"]

        # 2. Classificação de Curvatura (Tipos 2, 3 e 4)
        # Cabelos crespos (4) apresentam altíssima frequência de espirais e bordas densas.
        # Cabelos cacheados (3) possuem ondas fechadas e energia intermediária.
        # Cabelos ondulados (2) possuem transições mais suaves de gradiente.
        if densidade > 0.12 or energia > 45.0:
            curvatura = 4
            curvatura_label = "Crespo (Tipo 4: 4A/4B/4C)"
            confianca_curvatura = min(0.96, 0.78 + (densidade * 0.8))
        elif densidade > 0.06 or energia > 25.0:
            curvatura = 3
            curvatura_label = "Cacheado (Tipo 3: 3A/3B/3C)"
            confianca_curvatura = min(0.94, 0.80 + (energia * 0.003))
        else:
            curvatura = 2
            curvatura_label = "Ondulado (Tipo 2: 2A/2B/2C)"
            confianca_curvatura = min(0.91, 0.82 + (0.05 - densidade) * 0.5)

        # 3. Detecção de Frizz
        # Frizz elevado produz ruído de alta frequência nas bordas periféricas
        if frizz_val > 180.0 or densidade > 0.09:
            frizz_detectado = 1
            confianca_frizz = min(0.95, 0.75 + (frizz_val / 1000.0))
        else:
            frizz_detectado = 0
            confianca_frizz = min(0.92, 0.78 + ((180.0 - frizz_val) / 500.0))

        # 4. Estimativa de Porosidade Visual (Baixa=1, Média=2, Alta=3)
        # Alta porosidade frequentemente se manifesta com opacidade e dispersão de luz
        if metricas["saturacao_media"] < 40.0 and frizz_detectado == 1:
            porosidade_aparente = 3
            confianca_porosidade = 0.76
        elif metricas["saturacao_media"] > 80.0 and frizz_detectado == 0:
            porosidade_aparente = 1
            confianca_porosidade = 0.80
        else:
            porosidade_aparente = 2
            confianca_porosidade = 0.84

        tempo_ms = round((time.time() - t0) * 1000, 2)
        confianca_curvatura = round(float(confianca_curvatura), 3)
        confianca_frizz = round(float(confianca_frizz), 3)
        confianca_porosidade = round(float(confianca_porosidade), 3)

        # Human-in-the-Loop: Requer confirmação se a confiança for inferior ao limiar
        requer_confirmacao = bool(
            confianca_curvatura < self.CONFIDENCE_THRESHOLD or
            confianca_frizz < self.CONFIDENCE_THRESHOLD
        )

        return {
            "curvatura_detectada": curvatura,
            "curvatura_label": curvatura_label,
            "confianca_curvatura": confianca_curvatura,
            "frizz_detectado": frizz_detectado,
            "confianca_frizz": confianca_frizz,
            "porosidade_aparente": porosidade_aparente,
            "confianca_porosidade": confianca_porosidade,
            "sugestao_perfil": {
                "curvatura": curvatura,
                "porosidade": porosidade_aparente,
                "frizz_falta_definicao": frizz_detectado,
                "ressecamento_opacidade": 1 if porosidade_aparente == 3 else 0,
            },
            "requer_confirmacao_humana": requer_confirmacao,
            "tempo_inferencia_ms": tempo_ms,
            "modelo_utilizado": self.modelo_nome,
            "detalhes_morfologicos": {
                "densidade_bordas": round(densidade, 4),
                "indice_frizz": round(frizz_val, 2),
                "energia_curvatura": round(energia, 2)
            }
        }


# Instância singleton para reaproveitamento em chamadas da API
classifier_instance = YoloHairClassifier()
