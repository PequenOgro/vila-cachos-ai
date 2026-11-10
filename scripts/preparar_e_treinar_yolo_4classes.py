"""
scripts/preparar_e_treinar_yolo_4classes.py
Script de Preparação, Particionamento (200 Treino / 100 Validação) e Treinamento
do Modelo YOLOv8-cls com 4 Classes (Ondulado, Cacheado, Crespo, Careca/Sem Cabelo).

Atende rigorosamente à metodologia solicitada pelo coorientador:
- Amostra controlada de 300 imagens com Ground Truth conhecido.
- 200 imagens para treino (50 por classe).
- 100 imagens para validação cega com gabarito comprovado (25 por classe).
- Rejeição nativa de casos extremos (carecas, peles lisas, sem cabelo) via classe negativa.
- Não fragmenta em 7 sub-classes, estabilizando a inferência em 3 macro-classes tricológicas + 1 classe de rejeição.
"""

import os
import shutil
import random
import argparse
from typing import Dict, List, Tuple

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


CLASSES_ALVO = [
    "tipo_2_ondulado",
    "tipo_3_cacheado",
    "tipo_4_crespo",
    "careca_sem_cabelo"
]


def estruturar_diretorios(base_dir: str = "dataset_cachos_4classes") -> Tuple[str, str]:
    """Cria a estrutura de pastas padrão Ultralytics para classificação."""
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "val")

    for split_dir in [train_dir, val_dir]:
        for classe in CLASSES_ALVO:
            os.makedirs(os.path.join(split_dir, classe), exist_ok=True)

    return train_dir, val_dir


def gerar_amostras_sinteticas_careca_se_necessario(destino_train: str, destino_val: str):
    """
    Garante que a classe 'careca_sem_cabelo' tenha amostras representativas
    de superfícies lisas, peles calvas e ausência de mechas capilares.
    Gera imagens base caso o download externo do Kaggle ainda não tenha sido acoplado.
    """
    import numpy as np
    from PIL import Image

    train_careca = os.path.join(destino_train, "careca_sem_cabelo")
    val_careca = os.path.join(destino_val, "careca_sem_cabelo")

    # Se já houver arquivos reais suficientes, não substitui
    qtd_train = len([f for f in os.listdir(train_careca) if f.endswith(('.jpg', '.png'))])
    qtd_val = len([f for f in os.listdir(val_careca) if f.endswith(('.jpg', '.png'))])

    if qtd_train >= 50 and qtd_val >= 25:
        print(f"[*] Classe 'careca_sem_cabelo' já populada ({qtd_train} treino, {qtd_val} val).")
        return

    print("[*] Gerando amostras sintéticas de controle para superfícies calvas/sem mechas (Caso Base)...")
    # Tons de pele / couro cabeludo liso sem mechas
    paletas_pele = [
        (235, 200, 175),  # Tom claro
        (210, 160, 130),  # Tom médio
        (160, 110, 80),   # Tom pardo
        (90, 55, 40),     # Tom escuro
        (240, 240, 240)   # Fundo neutro
    ]

    total_necessario_train = max(0, 50 - qtd_train)
    total_necessario_val = max(0, 25 - qtd_val)

    # Preenche treino
    for i in range(total_necessario_train):
        cor_base = paletas_pele[i % len(paletas_pele)]
        # Adiciona ruído leve de textura de pele sem fibras
        ruido = np.random.normal(0, 6, (224, 224, 3)).astype(np.int16)
        base = np.full((224, 224, 3), cor_base, dtype=np.int16)
        img_arr = np.clip(base + ruido, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_arr)
        img.save(os.path.join(train_careca, f"amostra_calva_train_{i+1:03d}.jpg"))

    # Preenche validação
    for i in range(total_necessario_val):
        cor_base = paletas_pele[(i + 2) % len(paletas_pele)]
        ruido = np.random.normal(0, 5, (224, 224, 3)).astype(np.int16)
        base = np.full((224, 224, 3), cor_base, dtype=np.int16)
        img_arr = np.clip(base + ruido, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_arr)
        img.save(os.path.join(val_careca, f"amostra_calva_val_{i+1:03d}.jpg"))

    print(f"[+] Amostras de controle para 'careca_sem_cabelo' criadas com sucesso!")


def particionar_dataset_existente(
    origem_dir: str = "dataset_cachos",
    destino_dir: str = "dataset_cachos_4classes",
    n_train_por_classe: int = 50,
    n_val_por_classe: int = 25
):
    """
    Coleta imagens do dataset atual do salão e particiona rigidamente em
    50 treino / 25 validação para cada uma das 3 classes capilares.
    """
    train_dir, val_dir = estruturar_diretorios(destino_dir)
    print(f"=== PARTICIONANDO DATASET EM {n_train_por_classe} TREINO / {n_val_por_classe} VALIDAÇÃO POR CLASSE ===")

    classes_capilares = ["tipo_2_ondulado", "tipo_3_cacheado", "tipo_4_crespo"]

    for classe in classes_capilares:
        # Coleta todas as imagens disponíveis na origem
        todas_imgs = []
        for split in ["train", "val"]:
            caminho_classe = os.path.join(origem_dir, split, classe)
            if os.path.exists(caminho_classe):
                for f in os.listdir(caminho_classe):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        todas_imgs.append(os.path.join(caminho_classe, f))

        # Remove duplicatas se houver
        todas_imgs = list(set(todas_imgs))
        random.seed(42)  # Garantia de reprodutibilidade científica
        random.shuffle(todas_imgs)

        total_disponivel = len(todas_imgs)
        print(f"[*] Classe {classe}: {total_disponivel} imagens disponíveis.")

        # Seleciona exatamente 50 para treino e 25 para validação
        imgs_train = todas_imgs[:n_train_por_classe]
        imgs_val = todas_imgs[n_train_por_classe:n_train_por_classe + n_val_por_classe]

        # Copia para os destinos
        dest_train_classe = os.path.join(train_dir, classe)
        dest_val_classe = os.path.join(val_dir, classe)

        for i, src in enumerate(imgs_train):
            ext = os.path.splitext(src)[1]
            nome_arq = f"train_{i+1:03d}_{os.path.basename(src)}"
            shutil.copy2(src, os.path.join(dest_train_classe, nome_arq))

        for i, src in enumerate(imgs_val):
            ext = os.path.splitext(src)[1]
            nome_arq = f"val_{i+1:03d}_{os.path.basename(src)}"
            shutil.copy2(src, os.path.join(dest_val_classe, nome_arq))

        print(f"    -> Treino: {len(imgs_train)} copiadas | Validação: {len(imgs_val)} copiadas.")

    # Popula a 4ª classe de controle e casos extremos com imagens reais (carecas, calvos, sem cabelo, fotos aleatórias)
    from scripts.preparar_dataset_negativo_real import gerar_amostras_negativas_reais
    gerar_amostras_negativas_reais(destino_dir)

    print("\n=== RESUMO DO DATASET BALANCEADO (4 CLASSES - TOTAL 300 IMAGENS) ===")
    for split, s_dir in [("TREINO (200 imagens)", train_dir), ("VALIDAÇÃO (100 imagens)", val_dir)]:
        print(f"[{split}]")
        for c in CLASSES_ALVO:
            qtd = len(os.listdir(os.path.join(s_dir, c)))
            print(f"  - {c}: {qtd} imagens")


def treinar_e_avaliar_4classes(
    dataset_dir: str = "dataset_cachos_4classes",
    epochs: int = 15,
    imgsz: int = 224,
    batch: int = 16
):
    """Executa o treinamento e gera a validação formal."""
    if not ULTRALYTICS_AVAILABLE:
        print("[!] Ultralytics indisponível. Instale para executar.")
        return

    modelo_base = "yolov8n-cls.pt"
    if os.path.exists(os.path.join("assets", modelo_base)):
        modelo_base = os.path.join("assets", modelo_base)

    print(f"\n=== EXECUTANDO FINE-TUNING YOLOv8-CLS (4 CLASSES) ===")
    print(f"[*] Modelo Base: {modelo_base}")
    print(f"[*] Épocas: {epochs} | Batch: {batch} | ImgSz: {imgsz}")

    modelo = YOLO(modelo_base)
    resultados = modelo.train(
        data=dataset_dir,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project="runs_cachos_4classes",
        name="experimento_300imgs_4classes",
        verbose=True
    )

    print("\n[+] Treinamento finalizado!")
    print(f"[+] Pesos salvos em runs_cachos_4classes/experimento_300imgs_4classes/weights/best.pt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline 4 Classes YOLO")
    parser.add_argument("--preparar", action="store_true", default=True, help="Particiona dataset em 200/100")
    parser.add_argument("--treinar", action="store_true", help="Dispara o treino YOLO")
    parser.add_argument("--epochs", type=int, default=15, help="Número de épocas")
    args = parser.parse_args()

    if args.preparar:
        particionar_dataset_existente()

    if args.treinar:
        treinar_e_avaliar_4classes(epochs=args.epochs)
