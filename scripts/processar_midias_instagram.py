"""
processar_midias_instagram.py
Pipeline de Processamento e Extração de Mídias Reais do Instagram da Vila Cachos.

1. Lê as 17 fotos JPG originais do destaque de 'Antes e Depois'.
2. Extrai 3 frames HD nítidos (anti-blur) de cada um dos 48 vídeos MP4 (1280x720).
3. Classifica morfologicamente em:
   - tipo_2_ondulado
   - tipo_3_cacheado
   - tipo_4_crespo
4. Organiza em split balanceado (80% treino / 20% validação).
5. Gera o arquivo final 'dataset_cachos.zip' pronto para o Google Colab.
"""

import os
import glob
import cv2
import zipfile
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTA_DIR = os.path.join(BASE_DIR, "insta viila cheio")
DATASET_DIR = os.path.join(BASE_DIR, "dataset_cachos")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
ZIP_OUTPUT = os.path.join(BASE_DIR, "dataset_cachos.zip")

CLASSES = ["tipo_2_ondulado", "tipo_3_cacheado", "tipo_4_crespo"]


def classificar_curvatura(img_np: np.ndarray) -> str:
    """
    Classifica a curvatura capilar utilizando métricas morfológicas de gradiente e densidade.
    """
    if len(img_np.shape) == 3:
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_np
        
    edges = cv2.Canny(gray, threshold1=40, threshold2=120)
    densidade = float(np.sum(edges > 0) / edges.size)
    
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    energia = float(np.mean(np.sqrt(sobelx**2 + sobely**2)))
    
    if densidade > 0.11 or energia > 40.0:
        return "tipo_4_crespo"
    elif densidade > 0.05 or energia > 22.0:
        return "tipo_3_cacheado"
    else:
        return "tipo_2_ondulado"


def extrair_frames_video(caminho_video: str, n_frames: int = 3) -> list:
    """
    Extrai n_frames nítidos (sem desfoque de movimento) ao longo do vídeo.
    """
    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        return []
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 10:
        cap.release()
        return []
        
    frames_selecionados = []
    # Pontos de amostragem no vídeo (ex: 20%, 50%, 80%)
    posicoes = [int(total_frames * p) for p in np.linspace(0.2, 0.8, n_frames)]
    
    for pos in posicoes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if ret and frame is not None:
            # Converte BGR para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Checa nitidez com a variância do Laplaciano (descarta frames muito borrados)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            nitidez = cv2.Laplacian(gray, cv2.CV_64F).var()
            if nitidez > 60.0:  # Limiar anti-blur
                frames_selecionados.append(frame_rgb)
                
    cap.release()
    return frames_selecionados


def processar_todas_as_midias():
    print("=== INICIANDO PROCESSAMENTO DE MÍDIAS DO INSTAGRAM VILA CACHOS ===")
    
    # Prepara diretórios
    for split_dir in [TRAIN_DIR, VAL_DIR]:
        for cls in CLASSES:
            os.makedirs(os.path.join(split_dir, cls), exist_ok=True)
            
    fotos_jpg = glob.glob(os.path.join(INSTA_DIR, "*.jpg"))
    videos_mp4 = glob.glob(os.path.join(INSTA_DIR, "*.mp4"))
    
    print(f"[*] Fotos encontradas: {len(fotos_jpg)}")
    print(f"[*] Vídeos encontrados: {len(videos_mp4)}")
    
    contador = {"tipo_2_ondulado": 0, "tipo_3_cacheado": 0, "tipo_4_crespo": 0}
    total_salvas = 0
    
    # 1. Processa fotos JPG
    print("\n[*] Processando fotos JPG em alta resolução...")
    for idx, caminho in enumerate(fotos_jpg):
        try:
            with Image.open(caminho) as img:
                img_rgb = img.convert('RGB')
                img_np = np.array(img_rgb)
                
                # Classifica
                cls = classificar_curvatura(img_np)
                contador[cls] += 1
                
                # Split 80/20
                split = "val" if (contador[cls] % 5 == 0) else "train"
                
                # Redimensiona para 640x640 com crop central se necessário
                img_resized = img_rgb.resize((640, 640), Image.Resampling.LANCZOS)
                
                nome_base = f"insta_foto_{idx:03d}_{cls}.jpg"
                caminho_dest = os.path.join(DATASET_DIR, split, cls, nome_base)
                img_resized.save(caminho_dest, quality=92)
                total_salvas += 1
                
                # Adiciona variação espelhada (Data Augmentation)
                flip = img_resized.transpose(Image.FLIP_LEFT_RIGHT)
                flip.save(os.path.join(DATASET_DIR, split, cls, f"insta_foto_{idx:03d}_{cls}_flip.jpg"), quality=90)
                total_salvas += 1
        except Exception as e:
            print(f"[!] Falha na foto '{caminho}': {e}")
            
    # 2. Processa vídeos MP4
    print("\n[*] Extraindo frames nítidos dos vídeos MP4 de Antes e Depois...")
    for v_idx, caminho in enumerate(videos_mp4):
        try:
            frames = extrair_frames_video(caminho, n_frames=3)
            for f_idx, frame_np in enumerate(frames):
                cls = classificar_curvatura(frame_np)
                contador[cls] += 1
                
                split = "val" if (contador[cls] % 5 == 0) else "train"
                
                img_pil = Image.fromarray(frame_np)
                
                # Crop central quadrado para focar no cabelo (1280x720 -> 720x720)
                w, h = img_pil.size
                if h > w:
                    crop_box = (0, int((h - w) / 2), w, int((h + w) / 2))
                else:
                    crop_box = (int((w - h) / 2), 0, int((w + h) / 2), h)
                    
                img_cropped = img_pil.crop(crop_box).resize((640, 640), Image.Resampling.LANCZOS)
                
                nome_base = f"insta_video_{v_idx:03d}_f{f_idx}_{cls}.jpg"
                caminho_dest = os.path.join(DATASET_DIR, split, cls, nome_base)
                img_cropped.save(caminho_dest, quality=92)
                total_salvas += 1
        except Exception as e:
            print(f"[!] Falha no vídeo '{caminho}': {e}")
            
    print(f"\n[+] Total de novas amostras extraídas do Instagram: {total_salvas}!")
    
    # 3. Estatísticas finais do dataset
    print("\n--- Estatísticas Totais do Dataset Consolidado ---")
    total_geral = 0
    for split_nome, split_dir in [("Treino (Train)", TRAIN_DIR), ("Validação (Val)", VAL_DIR)]:
        print(f"\n[{split_nome}]:")
        for cls in CLASSES:
            qtd = len(os.listdir(os.path.join(split_dir, cls)))
            total_geral += qtd
            print(f"  - {cls}: {qtd} imagens")
            
    # 4. Atualiza o ZIP
    print(f"\n[*] Compactando todas as amostras em '{ZIP_OUTPUT}'...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for root, dirs, files in os.walk(DATASET_DIR):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_rel = os.path.relpath(caminho_completo, BASE_DIR)
                zip_f.write(caminho_completo, caminho_rel)
                
    tamanho_mb = round(os.path.getsize(ZIP_OUTPUT) / (1024 * 1024), 2)
    print(f"[+] '{os.path.basename(ZIP_OUTPUT)}' finalizado com sucesso ({tamanho_mb} MB)!")
    print(f"[+] Total geral no dataset pronto para o Colab: {total_geral} imagens!")


if __name__ == "__main__":
    processar_todas_as_midias()
