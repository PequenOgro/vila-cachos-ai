"""
train_yolo.py
Script de Treinamento e Fine-Tuning do Modelo YOLO (Ultralytics)
para Classificação e Detecção de Curvatura Capilar (TCC Vila Cachos AI).

Permite treinar modelos pré-treinados (ex: yolov8n-cls.pt ou yolov8n.pt)
com um dataset anotado de curvaturas capilares (Tipos 2, 3 e 4).
"""

import os
import argparse
from typing import Optional

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


def treinar_modelo_curvatura(
    data_yaml_ou_dir: str = "dataset_cachos",
    model_base: str = "yolov8n-cls.pt",
    epochs: int = 25,
    imgsz: int = 224,
    batch: int = 16,
    project: str = "runs_cachos",
    name: str = "experimento_yolo_curvatura"
) -> Optional[str]:
    """
    Executa o fine-tuning da rede YOLO usando transfer learning.
    """
    if not ULTRALYTICS_AVAILABLE:
        print("[!] Ultralytics não está instalado. Instale com 'pip install ultralytics'.")
        return None

    print(f"=== INICIANDO PIPELINE DE TREINAMENTO YOLO CAPILAR ===")
    print(f"[*] Modelo Base: {model_base}")
    print(f"[*] Dataset: {data_yaml_ou_dir}")
    print(f"[*] Épocas: {epochs} | Batch Size: {batch} | Img Size: {imgsz}")

    # Verifica se os pesos base estão em assets/ se não encontrado na raiz
    if not os.path.exists(model_base) and os.path.exists(os.path.join("assets", model_base)):
        model_base = os.path.join("assets", model_base)

    # Inicializa modelo com pesos pré-treinados (ImageNet transfer learning)
    modelo = YOLO(model_base)

    if not os.path.exists(data_yaml_ou_dir):
        print(f"[!] Diretório de dataset '{data_yaml_ou_dir}' não encontrado.")
        print("[*] Para coletar imagens reais, organize no formato Ultralytics:")
        print("    dataset_cachos/train/ (pastas: tipo_2, tipo_3, tipo_4)")
        print("    dataset_cachos/val/   (pastas: tipo_2, tipo_3, tipo_4)")
        return None

    # Inicia treinamento
    resultados = modelo.train(
        data=data_yaml_ou_dir,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        verbose=True
    )

    caminho_pesos = os.path.join(project, name, "weights", "best.pt")
    print(f"[+] Treinamento concluído com sucesso!")
    print(f"[+] Melhores pesos salvos em: {caminho_pesos}")
    return caminho_pesos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treinamento YOLO Vila Cachos")
    parser.add_argument("--data", default="dataset_cachos", help="Caminho do dataset ou data.yaml")
    parser.add_argument("--model", default="assets/yolov8n-cls.pt", help="Pesos base")
    parser.add_argument("--epochs", type=int, default=20, help="Número de épocas")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=224, help="Tamanho da imagem (224 é o padrão para classificação)")
    args = parser.parse_args()

    treinar_modelo_curvatura(
        data_yaml_ou_dir=args.data,
        model_base=args.model,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz
    )

