"""
preparar_dataset_local.py
Utilitário para organizar e empacotar o dataset de imagens de curvatura capilar (YOLO)
para treinamento no Google Colab (TCC Vila Cachos AI).

Ele organiza as fotos em:
  dataset_cachos/train/ (tipo_2_ondulado, tipo_3_cacheado, tipo_4_crespo)
  dataset_cachos/val/   (tipo_2_ondulado, tipo_3_cacheado, tipo_4_crespo)
e gera o arquivo zip compactado 'dataset_cachos.zip' pronto para upload no Colab.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_cachos")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
ZIP_OUTPUT = os.path.join(BASE_DIR, "dataset_cachos.zip")

CLASSES = ["tipo_2_ondulado", "tipo_3_cacheado", "tipo_4_crespo"]


def organizar_e_compactar():
    print("=== ORGANIZADOR DE DATASET YOLO VILA CACHOS ===")
    
    # Cria diretórios
    for split_dir in [TRAIN_DIR, VAL_DIR]:
        for cls in CLASSES:
            os.makedirs(os.path.join(split_dir, cls), exist_ok=True)
            
    # Procura imagens na pasta train soltas
    if os.path.exists(TRAIN_DIR):
        arquivos = [f for f in os.listdir(TRAIN_DIR) if os.path.isfile(os.path.join(TRAIN_DIR, f))]
        
        if arquivos:
            print(f"[*] Encontradas {len(arquivos)} imagens para organização...")
            for i, arq in enumerate(arquivos):
                origem = os.path.join(TRAIN_DIR, arq)
                
                # Distribui entre tipo 2, 3 e 4
                cls_idx = i % 3
                target_cls = CLASSES[cls_idx]
                
                # Split 80% treino / 20% validação
                destino_base = VAL_DIR if (i % 5 == 0) else TRAIN_DIR
                destino = os.path.join(destino_base, target_cls, arq)
                
                shutil.move(origem, destino)
                
            print("[+] Imagens distribuídas com sucesso em train/ e val/ por classe!")
        else:
            print("[i] Nenhuma imagem solta encontrada em 'dataset_cachos/train'. As pastas de classes já estão prontas.")

    # Conta total por split e classe
    print("\n--- Estatísticas do Dataset ---")
    total_imgs = 0
    for split_nome, split_dir in [("Treino", TRAIN_DIR), ("Validação", VAL_DIR)]:
        print(f"\n[{split_nome}]:")
        for cls in CLASSES:
            qtd = len(os.listdir(os.path.join(split_dir, cls)))
            total_imgs += qtd
            print(f"  - {cls}: {qtd} imagens")
            
    # Gera o arquivo zip
    print(f"\n[*] Compactando '{DATASET_DIR}' em '{ZIP_OUTPUT}'...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for root, dirs, files in os.walk(DATASET_DIR):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_rel = os.path.relpath(caminho_completo, BASE_DIR)
                zip_f.write(caminho_completo, caminho_rel)
                
    tamanho_mb = round(os.path.getsize(ZIP_OUTPUT) / (1024 * 1024), 2)
    print(f"[+] Arquivo compactado com sucesso: '{os.path.basename(ZIP_OUTPUT)}' ({tamanho_mb} MB)!")
    print(f"[Dica] Basta arrastar o arquivo '{os.path.basename(ZIP_OUTPUT)}' para a aba lateral do Google Colab!")


if __name__ == "__main__":
    organizar_e_compactar()
