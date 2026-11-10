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
from urllib.parse import urlparse
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image
import cv2

# Mitigação de vulnerabilidade: Proteção contra Decompression Bomb (DoS)
Image.MAX_IMAGE_PIXELS = 10_000_000

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

        # Se não foi fornecido caminho, procura automaticamente por pesos ONNX ou PT locais (raiz ou assets/)
        if not self.model_path:
            candidatos = [
                os.path.join(BASE_DIR, "assets", "best.pt"),
                os.path.join(BASE_DIR, "assets", "yolov8n-cls.pt"),
                os.path.join(BASE_DIR, "assets", "best.onnx"),
                os.path.join(BASE_DIR, "assets", "yolov8n-cls.onnx"),
                os.path.join(BASE_DIR, "best.pt"),
                os.path.join(BASE_DIR, "yolov8n-cls.pt"),
                os.path.join(BASE_DIR, "best.onnx"),
                os.path.join(BASE_DIR, "yolov8n-cls.onnx")
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
        - Coerência de textura capilar (rejeição de superfícies lisas e gráficos artificiais)
        """
        # Conversão para tons de cinza e HSV
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
            saturacao_media = float(np.mean(hsv[:, :, 1]))
            
            # Proporção de tons de pele humana (HSV: H entre 0-25, S moderada, V média/alta)
            skin_mask = cv2.inRange(hsv, np.array([0, 30, 50]), np.array([25, 200, 255]))
            skin_ratio = float(np.sum(skin_mask > 0) / skin_mask.size)

            # Análise de cores não biológicas (Azul/Ciano, Verde Neon, Magenta elétrico)
            blue_cyan = (hsv[:, :, 0] >= 85) & (hsv[:, :, 0] <= 140) & (hsv[:, :, 1] > 50)
            neon_green = (hsv[:, :, 0] >= 45) & (hsv[:, :, 0] <= 80) & (hsv[:, :, 1] > 70)
            magenta = (hsv[:, :, 0] >= 140) & (hsv[:, :, 0] <= 160) & (hsv[:, :, 1] > 70)
            unnatural = blue_cyan | neon_green | magenta
            unnatural_ratio = float(np.sum(unnatural) / unnatural.size)
        else:
            gray = img_np
            saturacao_media = 100.0
            skin_ratio = 0.0
            unnatural_ratio = 0.0

        # 1. Variância Laplaciana (Frequência espacial / rugosidade / Frizz)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        frizz_metric = float(np.var(laplacian))

        # 2. Análise de Bordas Canny para densidade de fios soltos
        edges = cv2.Canny(gray, threshold1=40, threshold2=120)
        densidade_bordas = float(np.sum(edges > 0) / edges.size)

        # Análise regional de bordas (topo/coroa craniana vs base/barba)
        h, _ = gray.shape
        upper_edges = edges[:int(h * 0.40), :]
        upper_density = float(np.sum(upper_edges > 0) / upper_edges.size)

        # 3. Gradientes de Sobel para medir orientação e torção das curvas
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        energia_curvatura = float(np.mean(magnitude))

        # 4. Proporção de áreas planas (flat area ratio) e brancos puros (documentos de texto)
        kernel = np.ones((5, 5), np.float32) / 25
        mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
        sq_mean = cv2.filter2D((gray.astype(np.float32)) ** 2, -1, kernel)
        var = np.maximum(0.0, sq_mean - mean ** 2)
        flat_ratio = float(np.sum(var < 15.0) / var.size)
        white_ratio = float(np.sum(gray > 220) / gray.size)

        return {
            "frizz_metric": frizz_metric,
            "densidade_bordas": densidade_bordas,
            "upper_density": upper_density,
            "energia_curvatura": energia_curvatura,
            "saturacao_media": saturacao_media,
            "skin_ratio": skin_ratio,
            "flat_ratio": flat_ratio,
            "white_ratio": white_ratio,
            "unnatural_ratio": unnatural_ratio
        }

    def _verificar_presenca_mechas(self, metricas: Dict[str, float]) -> tuple[bool, Optional[str]]:
        """
        Verifica a presença de mechas e fibras capilares humanas, rejeitando imagens
        lisas (pele/careca), fotos sem cabelo, gráficos sintéticos ou anúncios comerciais.
        """
        densidade = metricas["densidade_bordas"]
        upper_density = metricas.get("upper_density", densidade)
        frizz = metricas["frizz_metric"]
        skin_ratio = metricas.get("skin_ratio", 0.0)
        flat = metricas.get("flat_ratio", 0.0)
        white_ratio = metricas.get("white_ratio", 0.0)
        saturacao = metricas.get("saturacao_media", 0.0)
        energia = metricas.get("energia_curvatura", 0.0)
        unnatural = metricas.get("unnatural_ratio", 0.0)

        # Caso 1: Superfície lisa sem microfibras ou cabelo ausente
        if densidade < 0.020 or frizz < 18.0:
            return False, "A foto não apresenta mechas ou fios de cabelo visíveis (superfície lisa ou ausência de cabelo)."

        # Caso 2: Calvície / Cabeça careca com ou sem barba (topo craniano liso com alta proporção de pele)
        if skin_ratio > 0.35 and upper_density < 0.028:
            return False, "Identificamos ausência de cabelo no couro cabeludo (foto de pessoa calva ou sem mecha definida). Envie uma foto aproximada de uma mecha do cabelo."

        # Caso 3: Cores não biológicas ou gráficos sintéticos (ex: banners, anúncios, ilustrações saturadas)
        if unnatural > 0.60 or (unnatural > 0.25 and densidade < 0.05):
            return False, "A imagem contém elementos gráficos artificiais ou cores não biológicas, sem mechas capilares válidas."

        # Caso 4: Imagem predominantemente plana com traços esparsos (ex: paredes, papéis, objetos geométricos)
        if flat > 0.78 and densidade < 0.045:
            return False, "A imagem é predominantemente plana e não possui textura de mechas capilares suficientes."

        # Caso 5: Documentos, recibos, folhas impressas (fundo predominantemente branco com texto preto desprovido de cor)
        if saturacao < 12.0 and white_ratio > 0.50:
            return False, "A imagem aparenta ser um documento, texto impresso ou papel, sem mechas capilares válidas."

        # Caso 6: Grades ortogonais artificiais e padrões geométricos sem cor biológica
        if saturacao < 8.0 and skin_ratio < 0.05 and energia > 55.0:
            return False, "Padrão geométrico artificial detectado, sem mechas capilares biológicas."

        # Caso 5: Ruído digital caótico ou artefato de alta frequência sem coerência biológica
        energia = metricas.get("energia_curvatura", 0.0)
        if frizz > 10000.0 or energia > 120.0 or densidade > 0.32:
            return False, "A imagem contém ruído digital ou textura artificial excessiva sem coerência com mechas capilares."

        return True, None

    def predict_image_bytes(self, image_bytes: bytes, filename: str = "amostra.jpg") -> Dict[str, Any]:
        """
        Processa os bytes de uma imagem e retorna a predição estruturada de características capilares.
        """
        t0 = time.time()

        if not image_bytes or len(image_bytes) < 32:
            raise ValueError("Buffer de imagem inválido ou vazio.")

        # Suporte a Servidor de Inferência Remoto em GPU (Google Colab / Ngrok) com proteção contra SSRF
        remote_url = os.environ.get("YOLO_REMOTE_URL", "").strip().rstrip("/")
        if remote_url:
            parsed = urlparse(remote_url)
            # Validação estrita de esquema (apenas HTTP/HTTPS) e bloqueio de IPs de metadados de nuvem (SSRF)
            blocked_hosts = {"169.254.169.254", "metadata.google.internal", "instance-data", "100.100.100.200"}
            if parsed.scheme in ("http", "https") and parsed.hostname and parsed.hostname.lower() not in blocked_hosts:
                try:
                    import httpx
                    target_url = remote_url if remote_url.endswith("/diagnostico/imagem") else f"{remote_url}/diagnostico/imagem"
                    files = {"file": (filename, image_bytes, "image/jpeg")}
                    with httpx.Client(timeout=3.0) as client:
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

        # 2. Verificação de presença real de mechas capilares
        cabelo_detectado, motivo_alerta = self._verificar_presenca_mechas(metricas)
        tempo_ms = round((time.time() - t0) * 1000, 2)

        if not cabelo_detectado:
            return {
                "cabelo_detectado": False,
                "mensagem_alerta": motivo_alerta or "Não identificamos fios ou mechas de cabelo nesta foto. Por favor, envie uma foto nítida da mecha ou selecione sua curvatura manualmente.",
                "curvatura_detectada": None,
                "curvatura_label": "Nenhum cabelo detectado",
                "confianca_curvatura": 0.0,
                "frizz_detectado": None,
                "confianca_frizz": 0.0,
                "porosidade_aparente": None,
                "confianca_porosidade": 0.0,
                "sugestao_perfil": None,
                "requer_confirmacao_humana": True,
                "tempo_inferencia_ms": tempo_ms,
                "modelo_utilizado": self.modelo_nome,
                "detalhes_morfologicos": {
                    "densidade_bordas": round(densidade, 4),
                    "indice_frizz": round(frizz_val, 2),
                    "energia_curvatura": round(energia, 2),
                    "proporcao_cor_artificial": round(metricas.get("unnatural_ratio", 0.0), 3)
                }
            }

        # 3. Classificação de Curvatura (Tipos 2, 3 e 4) + Rejeição Neural (Careca/Sem Cabelo)
        # Se o modelo YOLO estiver carregado, executa a inferência neural
        yolo_curvatura = None
        yolo_conf = 0.0
        p_careca = 0.0
        if self.yolo_model is not None:
            try:
                y_res = self.yolo_model(img_resized, verbose=False)[0]
                top1_idx = int(y_res.probs.top1)
                yolo_conf = float(y_res.probs.top1conf)
                
                # Mapeamento dinâmico baseado nos nomes reais das classes do modelo
                class_names = getattr(self.yolo_model, "names", {})
                detected_class = str(class_names.get(top1_idx, "")).lower()

                # Coleta probabilidade específica da classe negativa (careca/sem cabelo)
                probs_data = y_res.probs.data
                for idx, name in class_names.items():
                    if "careca" in str(name).lower() or "sem_cabelo" in str(name).lower():
                        p_careca = float(probs_data[idx])
                        break

                p_cabelo_total = 1.0 - p_careca

                # Rejeição imediata se:
                # a) A classe top1 for careca/sem_cabelo
                # b) Ou probabilidade da classe careca for relevante (>= 0.20)
                # c) Ou probabilidade acumulada de cabelo for insuficiente (< 0.50)
                if "careca" in detected_class or "sem_cabelo" in detected_class or p_careca >= 0.20 or p_cabelo_total < 0.50:
                    tempo_ms = round((time.time() - t0) * 1000, 2)
                    return {
                        "cabelo_detectado": False,
                        "mensagem_alerta": "Não identificamos fios ou mechas de cabelo visíveis nesta foto (detectada ausência de cabelo ou superfície calva). Por favor, posicione a câmera focando uma mecha do cabelo ou selecione sua curvatura manualmente.",
                        "curvatura_detectada": None,
                        "curvatura_label": "Nenhum cabelo detectado",
                        "confianca_curvatura": 0.0,
                        "frizz_detectado": None,
                        "confianca_frizz": 0.0,
                        "porosidade_aparente": None,
                        "confianca_porosidade": 0.0,
                        "sugestao_perfil": None,
                        "requer_confirmacao_humana": True,
                        "tempo_inferencia_ms": tempo_ms,
                        "modelo_utilizado": self.modelo_nome,
                        "detalhes_morfologicos": {
                            "densidade_bordas": round(densidade, 4),
                            "indice_frizz": round(frizz_val, 2),
                            "energia_curvatura": round(energia, 2),
                            "proporcao_cor_artificial": round(metricas.get("unnatural_ratio", 0.0), 3),
                            "proporcao_pele": round(metricas.get("skin_ratio", 0.0), 3),
                            "probabilidade_careca": round(p_careca, 4)
                        }
                    }
                elif yolo_conf < 0.40 and densidade < 0.05:
                    # Imagem sem padrão capilar definido nem pela rede nem pela morfologia
                    tempo_ms = round((time.time() - t0) * 1000, 2)
                    return {
                        "cabelo_detectado": False,
                        "mensagem_alerta": "Não foi possível reconhecer o padrão capilar com segurança nesta foto (imagem ambígua ou sem foco em mecha). Envie uma foto aproximada dos fios ou selecione abaixo.",
                        "curvatura_detectada": None,
                        "curvatura_label": "Padrão capilar não reconhecido",
                        "confianca_curvatura": round(yolo_conf, 3),
                        "frizz_detectado": None,
                        "confianca_frizz": 0.0,
                        "porosidade_aparente": None,
                        "confianca_porosidade": 0.0,
                        "sugestao_perfil": None,
                        "requer_confirmacao_humana": True,
                        "tempo_inferencia_ms": tempo_ms,
                        "modelo_utilizado": self.modelo_nome,
                        "detalhes_morfologicos": {
                            "densidade_bordas": round(densidade, 4),
                            "indice_frizz": round(frizz_val, 2),
                            "energia_curvatura": round(energia, 2),
                            "proporcao_cor_artificial": round(metricas.get("unnatural_ratio", 0.0), 3),
                            "proporcao_pele": round(metricas.get("skin_ratio", 0.0), 3)
                        }
                    }
                elif "tipo_2" in detected_class or "ondulado" in detected_class:
                    yolo_curvatura = 2
                elif "tipo_3" in detected_class or "cacheado" in detected_class:
                    yolo_curvatura = 3
                elif "tipo_4" in detected_class or "crespo" in detected_class:
                    yolo_curvatura = 4
                else:
                    # Fallback posicional para modelos sem nomes explícitos
                    yolo_curvatura = top1_idx + 2
            except Exception as e:
                print(f"[!] Erro na execução do classificador YOLO: {e}")

        # Combinação Híbrida: YOLO Neural + Morfologia Tricológica
        labels_map = {
            2: "Ondulado (Tipo 2: 2A/2B/2C)",
            3: "Cacheado (Tipo 3: 3A/3B/3C)",
            4: "Crespo (Tipo 4: 4A/4B/4C)"
        }

        if yolo_curvatura is not None and yolo_conf >= 0.35:
            curvatura = yolo_curvatura
            curvatura_label = labels_map[curvatura]
            confianca_curvatura = yolo_conf
        else:
            # Fallback morfológico estrito: se o modelo neural não estiver disponível, exige assinatura de mecha
            if densidade < 0.035 or frizz_val < 30.0:
                tempo_ms = round((time.time() - t0) * 1000, 2)
                return {
                    "cabelo_detectado": False,
                    "mensagem_alerta": "Não foi identificada textura suficiente de mechas capilares nesta foto.",
                    "curvatura_detectada": None,
                    "curvatura_label": "Nenhum cabelo detectado",
                    "confianca_curvatura": 0.0,
                    "frizz_detectado": None,
                    "confianca_frizz": 0.0,
                    "porosidade_aparente": None,
                    "confianca_porosidade": 0.0,
                    "sugestao_perfil": None,
                    "requer_confirmacao_humana": True,
                    "tempo_inferencia_ms": tempo_ms,
                    "modelo_utilizado": self.modelo_nome,
                    "detalhes_morfologicos": {
                        "densidade_bordas": round(densidade, 4),
                        "indice_frizz": round(frizz_val, 2),
                        "energia_curvatura": round(energia, 2),
                        "proporcao_cor_artificial": round(metricas.get("unnatural_ratio", 0.0), 3)
                    }
                }
            if densidade > 0.12 or energia > 45.0:
                curvatura = 4
                curvatura_label = labels_map[4]
                confianca_curvatura = min(0.96, 0.78 + (densidade * 0.8))
            elif densidade > 0.06 or energia > 25.0:
                curvatura = 3
                curvatura_label = labels_map[3]
                confianca_curvatura = min(0.94, 0.80 + (energia * 0.003))
            else:
                curvatura = 2
                curvatura_label = labels_map[2]
                confianca_curvatura = min(0.91, 0.82 + (0.05 - densidade) * 0.5)

        # 4. Detecção de Frizz
        if frizz_val > 180.0 or densidade > 0.09:
            frizz_detectado = 1
            confianca_frizz = min(0.95, 0.75 + (frizz_val / 1000.0))
        else:
            frizz_detectado = 0
            confianca_frizz = min(0.92, 0.78 + ((180.0 - frizz_val) / 500.0))

        # 5. Estimativa de Porosidade Visual (Baixa=1, Média=2, Alta=3)
        if metricas["saturacao_media"] < 40.0 and frizz_detectado == 1:
            porosidade_aparente = 3
            confianca_porosidade = 0.76
        elif metricas["saturacao_media"] > 80.0 and frizz_detectado == 0:
            porosidade_aparente = 1
            confianca_porosidade = 0.80
        else:
            porosidade_aparente = 2
            confianca_porosidade = 0.84

        confianca_curvatura = round(float(confianca_curvatura), 3)
        confianca_frizz = round(float(confianca_frizz), 3)
        confianca_porosidade = round(float(confianca_porosidade), 3)

        # Human-in-the-Loop: Requer confirmação se a confiança for inferior ao limiar
        requer_confirmacao = bool(
            confianca_curvatura < self.CONFIDENCE_THRESHOLD or
            confianca_frizz < self.CONFIDENCE_THRESHOLD
        )

        return {
            "cabelo_detectado": True,
            "mensagem_alerta": None,
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
                "energia_curvatura": round(energia, 2),
                "proporcao_cor_artificial": round(metricas.get("unnatural_ratio", 0.0), 3)
            }
        }


# Instância singleton para reaproveitamento em chamadas da API
classifier_instance = YoloHairClassifier()
