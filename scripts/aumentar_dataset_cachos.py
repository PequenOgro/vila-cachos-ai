"""
aumentar_dataset_cachos.py
Script de Aumento de Dados (Data Augmentation) para o Dataset de Curvatura Capilar YOLO.

Transforma as fotos reais coletadas do salão em centenas de amostras de treinamento
através de transformações invariantes (espelhamento, zoom em texturas de mechas,
variações de iluminação e rotações sutis), eliminando a necessidade de coletar
manualmente centenas de fotos.
"""

import os
import shutil
import zipfile
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_cachos")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
ZIP_OUTPUT = os.path.join(BASE_DIR, "dataset_cachos.zip")

CLASSES = ["tipo_2_ondulado", "tipo_3_cacheado", "tipo_4_crespo"]


def processar_e_aumentar_imagem(caminho_img: str, pasta_saida: str, prefixo: str):
    """
    Carrega uma foto original e gera 8 variações enriquecidas para a rede neural.
    """
    try:
        with Image.open(caminho_img) as img:
            # Converte RGBA para RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            w, h = img.size
            
            # 1. Imagem Base Redimensionada para 640x640 (padrão YOLO)
            base = img.resize((640, 640), Image.Resampling.LANCZOS)
            base.save(os.path.join(pasta_saida, f"{prefixo}_base.jpg"), quality=92)
            
            # 2. Espelhamento Horizontal (Flip)
            flip = base.transpose(Image.FLIP_LEFT_RIGHT)
            flip.save(os.path.join(pasta_saida, f"{prefixo}_flip.jpg"), quality=92)
            
            # 3. Zoom Central na Mecha (Crop 80% do centro para focar na curvatura)
            crop_margin_w = int(w * 0.1)
            crop_margin_h = int(h * 0.1)
            crop_central = img.crop((crop_margin_w, crop_margin_h, w - crop_margin_w, h - crop_margin_h))
            crop_central = crop_central.resize((640, 640), Image.Resampling.LANCZOS)
            crop_central.save(os.path.join(pasta_saida, f"{prefixo}_crop.jpg"), quality=92)
            
            # 4. Zoom Central Espelhado
            crop_flip = crop_central.transpose(Image.FLIP_LEFT_RIGHT)
            crop_flip.save(os.path.join(pasta_saida, f"{prefixo}_crop_flip.jpg"), quality=92)
            
            # 5. Variação de Iluminação (+20% mais claro - luz direta de salão)
            enhancer_brilho = ImageEnhance.Brightness(base)
            brilho_alto = enhancer_brilho.enhance(1.2)
            brilho_alto.save(os.path.join(pasta_saida, f"{prefixo}_bright.jpg"), quality=92)
            
            # 6. Variação de Iluminação (-15% mais escuro - luz ambiente)
            brilho_baixo = enhancer_brilho.enhance(0.85)
            brilho_baixo.save(os.path.join(pasta_saida, f"{prefixo}_shadow.jpg"), quality=92)
            
            # 7. Realce de Contraste / Nitidez das Espirais dos Cachos
            enhancer_contraste = ImageEnhance.Contrast(base)
            contraste_alto = enhancer_contraste.enhance(1.25)
            contraste_alto.save(os.path.join(pasta_saida, f"{prefixo}_contrast.jpg"), quality=92)
            
            # 8. Rotação Leve (+7 graus - variação de ângulo de foto com celular)
            rot = base.rotate(7, resample=Image.Resampling.BICUBIC, fillcolor=(240, 235, 230))
            rot.save(os.path.join(pasta_saida, f"{prefixo}_rot7.jpg"), quality=92)

    except Exception as e:
        print(f"[!] Erro ao processar '{caminho_img}': {e}")


def executar_aumento():
    print("=== PIPELINE DE DATA AUGMENTATION (TCC VILA CACHOS YOLO) ===")
    
    total_geradas = 0
    
    for split_nome, split_dir in [("train", TRAIN_DIR), ("val", VAL_DIR)]:
        print(f"\n[*] Processando partição '{split_nome}'...")
        for cls in CLASSES:
            dir_cls = os.path.join(split_dir, cls)
            if not os.path.exists(dir_cls):
                continue
                
            # Filtra fotos originais (evita re-aumentar imagens aumentadas)
            arquivos_originais = [
                f for f in os.listdir(dir_cls) 
                if f.endswith(('.png', '.jpg', '.jpeg')) and not f.startswith("aug_")
            ]
            
            print(f"  - Classe '{cls}': {len(arquivos_originais)} fotos originais encontradas.")
            
            for idx, nome_arq in enumerate(arquivos_originais):
                caminho = os.path.join(dir_cls, nome_arq)
                prefixo = f"aug_{idx:03d}"
                processar_e_aumentar_imagem(caminho, dir_cls, prefixo)
                
            qtd_final = len(os.listdir(dir_cls))
            total_geradas += qtd_final
            print(f"    -> Expandido para {qtd_final} amostras de treinamento!")
            
    print("\n--- Estatísticas Finais do Dataset Expandido ---")
    for split_nome, split_dir in [("Treino", TRAIN_DIR), ("Validação", VAL_DIR)]:
        print(f"\n[{split_nome}]:")
        for cls in CLASSES:
            qtd = len(os.listdir(os.path.join(split_dir, cls)))
            print(f"  - {cls}: {qtd} imagens")
            
    # Compacta no dataset_cachos.zip
    print(f"\n[*] Atualizando arquivo compactado '{ZIP_OUTPUT}'...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for root, dirs, files in os.walk(DATASET_DIR):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_rel = os.path.relpath(caminho_completo, BASE_DIR)
                zip_f.write(caminho_completo, caminho_rel)
                
    tamanho_mb = round(os.path.getsize(ZIP_OUTPUT) / (1024 * 1024), 2)
    print(f"[+] 'dataset_cachos.zip' atualizado com sucesso ({tamanho_mb} MB) contendo {total_geradas} amostras!")
    print("[+] Pronto para envio imediato ao Google Colab sem trabalho manual adicional!")


if __name__ == "__main__":
    executar_aumento()
