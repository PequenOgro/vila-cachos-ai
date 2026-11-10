"""
scripts/preparar_dataset_negativo_real.py
Coleta e organiza imagens reais para a classe 'careca_sem_cabelo' no dataset_cachos_4classes:
- 35 fotos de cabeças raspadas / calvos / carecas reais (com e sem barba)
- 25 fotos de ambientes, objetos e cenas aleatórias cotidianas (não-cabelo)
- 15 texturas de pele / tecido / fundos lisos
Total: 50 imagens no split de treino e 25 no split de validação.
"""

import os
import io
import ssl
import random
import urllib.request
import urllib.parse
import json
import numpy as np
from PIL import Image, ImageEnhance

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'VilaCachosAI/1.0 (academic research; contact@vilacachos.com.br)'}


def download_image(url: str, timeout: int = 7) -> Image.Image:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
        data = resp.read()
        img = Image.open(io.BytesIO(data))
        return img.convert('RGB')


def coletar_imagens_careca_wikimedia() -> list:
    pessoas = [
        'Patrick Stewart', 'Mahatma Gandhi', 'Zinedine Zidane', 'John Malkovich',
        'Dwight D. Eisenhower', 'Telly Savalas', 'Yul Brynner', 'Ben Kingsley',
        'bald man portrait', 'shaved head portrait'
    ]
    urls = []
    for p in pessoas:
        q = urllib.parse.quote(p)
        url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={q}&gsrnamespace=6&gsrlimit=8&prop=imageinfo&iiprop=url&format=json'
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for k, v in data.get('query', {}).get('pages', {}).items():
                    infos = v.get('imageinfo', [])
                    if infos:
                        u = infos[0].get('url', '')
                        clean_u = u.split('?')[0].lower()
                        if clean_u.endswith(('.jpg', '.jpeg', '.png')):
                            title = v.get('title', '').lower()
                            if not any(bad in title for bad in ['penis', 'statue', 'eagle', 'drawing', 'car']):
                                urls.append(u)
        except Exception:
            pass
    return list(set(urls))


def gerar_amostras_negativas_reais(base_dir: str = "dataset_cachos_4classes"):
    train_dir = os.path.join(base_dir, "train", "careca_sem_cabelo")
    val_dir = os.path.join(base_dir, "val", "careca_sem_cabelo")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # Limpa imagens sintéticas anteriores (amostra_calva_*)
    for d in [train_dir, val_dir]:
        for f in os.listdir(d):
            if f.startswith("amostra_calva_") or f.endswith(('.jpg', '.png')):
                os.remove(os.path.join(d, f))

    print("[*] Coletando URLs de carecas reais na Wikimedia...")
    bald_urls = coletar_imagens_careca_wikimedia()
    print(f"[*] Encontradas {len(bald_urls)} URLs candidatas de pessoas calvas/carecas.")

    imgs_careca = []
    
    # 1. Inclui o exemplo real do usuário (homem careca com barba) com variações
    user_bald_path = os.path.join("scratch", "bald_with_beard.jpg")
    if os.path.exists(user_bald_path):
        base_user = Image.open(user_bald_path).convert("RGB")
        imgs_careca.append(base_user)
        imgs_careca.append(base_user.transpose(Image.FLIP_LEFT_RIGHT))
        enh = ImageEnhance.Brightness(base_user)
        imgs_careca.append(enh.enhance(1.15))
        imgs_careca.append(enh.enhance(0.85))
        enh_c = ImageEnhance.Contrast(base_user)
        imgs_careca.append(enh_c.enhance(1.2))

    for u in bald_urls:
        if len(imgs_careca) >= 40:
            break
        try:
            img = download_image(u, timeout=6)
            # Redimensiona mantendo proporção ou centro
            img = img.resize((300, 300))
            imgs_careca.append(img)
            print(f" [+] Careca baixado: {len(imgs_careca)}/40")
        except Exception as e:
            continue

    print(f"[+] Total de fotos de carecas/calvos coletadas: {len(imgs_careca)}")

    # 2. Coleta fotos aleatórias cotidianas (animais, carros, salas, comida, objetos) do Picsum
    imgs_random = []
    print("[*] Coletando fotos aleatórias de objetos/cenas (não-cabelo)...")
    for i in range(1, 40):
        try:
            url_pic = f"https://picsum.photos/300/300?random={i+200}"
            img = download_image(url_pic, timeout=5)
            imgs_random.append(img)
            if len(imgs_random) >= 30:
                break
        except Exception:
            continue
    print(f"[+] Total de fotos aleatórias coletadas: {len(imgs_random)}")

    # 3. Adiciona texturas de pele / scalp lisa / tecidos neutros
    imgs_texturas = []
    paletas_pele = [
        (235, 200, 175), (210, 160, 130), (160, 110, 80), (90, 55, 40), (240, 240, 240)
    ]
    for i, cor in enumerate(paletas_pele):
        ruido = np.random.normal(0, 4, (300, 300, 3)).astype(np.int16)
        base = np.full((300, 300, 3), cor, dtype=np.int16)
        arr = np.clip(base + ruido, 0, 255).astype(np.uint8)
        imgs_texturas.append(Image.fromarray(arr))

    todas_negativas = imgs_careca + imgs_random + imgs_texturas
    random.seed(42)
    random.shuffle(todas_negativas)

    print(f"[*] Total de amostras negativas geradas: {len(todas_negativas)}")
    
    # Precisamos de 50 treino e 25 validação (total 75)
    # Se faltar um pouco, aplica data augmentation (flip horizontal, brilho)
    idx = 0
    while len(todas_negativas) < 75:
        orig = todas_negativas[idx % len(todas_negativas)]
        augmented = orig.transpose(Image.FLIP_LEFT_RIGHT)
        todas_negativas.append(augmented)
        idx += 1

    train_amostras = todas_negativas[:50]
    val_amostras = todas_negativas[50:75]

    for i, img in enumerate(train_amostras):
        salvar_path = os.path.join(train_dir, f"neg_real_train_{i+1:03d}.jpg")
        img.resize((224, 224)).save(salvar_path, "JPEG", quality=90)

    for i, img in enumerate(val_amostras):
        salvar_path = os.path.join(val_dir, f"neg_real_val_{i+1:03d}.jpg")
        img.resize((224, 224)).save(salvar_path, "JPEG", quality=90)

    print(f"[+] Classe 'careca_sem_cabelo' populada com sucesso: {len(train_amostras)} treino, {len(val_amostras)} validação!")


if __name__ == "__main__":
    gerar_amostras_negativas_reais()
