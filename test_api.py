"""
test_api.py
Testes automatizados para a API FastAPI da Vila Cachos.
"""

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health():
    with TestClient(app) as tc:
        resp = tc.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "operacional"
        assert data["motor_carregado"] is True
        assert data["num_clusters"] == 4
        print("[PASS] Teste GET /health bem-sucedido!")

def test_recommendation_flow():
    with TestClient(app) as tc:
        payload = {
            "curvatura": 3,
            "porosidade": 3,
            "dano_quimico": 1,
            "ressecamento_opacidade": 0,
            "alta_porosidade_quimica": 1,
            "frizz_falta_definicao": 0,
            "transicao_capilar": 0,
            "couro_sensivel_oleoso": 0
        }
        resp = tc.post("/recommend?top_k=3", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "cluster_id" in data
        assert "descricao_persona" in data
        assert len(data["recomendacoes"]) == 3
        
        # Produto número 1 deve ser o ACID-C para alta porosidade e química
        top1 = data["recomendacoes"][0]
        assert "ACID-C" in top1["nome"]
        assert top1["score_final"] > 0
        assert "estrelas_estimadas" in top1
        assert "motivo" in top1
        print(f"[PASS] Teste POST /recommend bem-sucedido! Top 1: {top1['nome']} (Score: {top1['score_final']})")

def test_feedback_flow():
    with TestClient(app) as tc:
        # Pega a recomendação antes
        payload_cliente = {
            "curvatura": 3,
            "porosidade": 3,
            "dano_quimico": 1,
            "ressecamento_opacidade": 0,
            "alta_porosidade_quimica": 1,
            "frizz_falta_definicao": 0,
            "transicao_capilar": 0,
            "couro_sensivel_oleoso": 0
        }
        resp_rec_antes = tc.post("/recommend?top_k=1", json=payload_cliente)
        score_antes = resp_rec_antes.json()["recomendacoes"][0]["score_final"]
        
        # Envia feedback nota 5 para o ACID-C
        payload_feedback = {
            "perfil_cliente": payload_cliente,
            "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
            "nota_satisfacao": 5
        }
        resp_feed = tc.post("/feedback", json=payload_feedback)
        assert resp_feed.status_code == 200
        data_feed = resp_feed.json()
        assert data_feed["status"] == "sucesso"
        assert "recalibrados" in data_feed["mensagem"]
        
        # Verifica se o score do produto foi recalibrado
        resp_rec_depois = tc.post("/recommend?top_k=1", json=payload_cliente)
        score_depois = resp_rec_depois.json()["recomendacoes"][0]["score_final"]
        assert score_depois >= score_antes
        print(f"[PASS] Teste POST /feedback bem-sucedido! Score antes: {score_antes} -> depois: {score_depois}")

def test_validation_errors():
    with TestClient(app) as tc:
        # Curvatura inválida (ex: 5)
        resp_invalid_curv = tc.post("/recommend", json={"curvatura": 5, "porosidade": 1, "dano_quimico": 0})
        assert resp_invalid_curv.status_code == 422
        
        # Nota inválida (ex: 6)
        resp_invalid_nota = tc.post("/feedback", json={
            "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
            "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
            "nota_satisfacao": 6
        })
        assert resp_invalid_nota.status_code == 422
        print("[PASS] Testes de validação Pydantic (HTTP 422) bem-sucedidos!")

def test_image_diagnosis():
    import os
    import io
    import cv2
    import numpy as np
    from PIL import Image

    with TestClient(app) as tc:
        # 1. Teste de Sucesso com Imagem de Mechas de Cabelo Real
        caminho_cabelo_real = "dataset_cachos/train/tipo_2_ondulado/aug_000_base.jpg"
        if os.path.exists(caminho_cabelo_real):
            with open(caminho_cabelo_real, "rb") as f:
                hair_bytes = f.read()
        else:
            # Imagem sintética de mechas com tons naturais de cabelo
            hair_img = np.full((320, 320, 3), [25, 35, 45], dtype=np.uint8)
            for _ in range(120):
                p1 = (int(np.random.randint(0, 320)), int(np.random.randint(0, 320)))
                p2 = (p1[0] + int(np.random.randint(-20, 20)), p1[1] + int(np.random.randint(30, 80)))
                cv2.line(hair_img, p1, p2, (40, 70, 90), 2)
            _, encoded = cv2.imencode(".jpg", hair_img)
            hair_bytes = encoded.tobytes()

        files_hair = {"file": ("cabelo_mecha.jpg", hair_bytes, "image/jpeg")}
        resp_hair = tc.post("/diagnostico/imagem", files=files_hair)
        assert resp_hair.status_code == 200, f"Erro: {resp_hair.text}"
        data_hair = resp_hair.json()
        assert data_hair["cabelo_detectado"] is True, "Cabelo real não foi detectado!"
        assert data_hair["curvatura_detectada"] in [2, 3, 4]
        assert data_hair["sugestao_perfil"] is not None
        print(f"[PASS] Imagem de mecha capilar identificada com sucesso! Curvatura: {data_hair['curvatura_label']}")

        # 2. Teste de Rejeição: Foto Lisa / Couro Cabeludo Calvo / Careca
        skin_img = np.full((320, 320, 3), [180, 200, 240], dtype=np.uint8) # Tom de pele uniforme
        _, encoded_skin = cv2.imencode(".jpg", skin_img)
        files_skin = {"file": ("careca_ou_pele.jpg", encoded_skin.tobytes(), "image/jpeg")}
        resp_skin = tc.post("/diagnostico/imagem", files=files_skin)
        assert resp_skin.status_code == 200
        data_skin = resp_skin.json()
        assert data_skin["cabelo_detectado"] is False, "Pele lisa/careca não deveria acusar cabelo!"
        assert data_skin["curvatura_detectada"] is None
        assert "mensagem_alerta" in data_skin and data_skin["mensagem_alerta"] is not None
        print(f"[PASS] Superfície lisa/careca rejeitada com aviso: {data_skin['mensagem_alerta']}")

        # 3. Teste de Rejeição: Banner / Anúncio Gráfico com Texto (Caso do usuário)
        banner_img = np.full((320, 320, 3), [120, 30, 20], dtype=np.uint8) # Azul elétrico artificial
        cv2.putText(banner_img, "MERECE SABER", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.line(banner_img, (50, 280), (160, 100), (220, 220, 255), 2)
        _, encoded_banner = cv2.imencode(".jpg", banner_img)
        files_banner = {"file": ("banner_anuncio.jpg", encoded_banner.tobytes(), "image/jpeg")}
        resp_banner = tc.post("/diagnostico/imagem", files=files_banner)
        assert resp_banner.status_code == 200
        data_banner = resp_banner.json()
        assert data_banner["cabelo_detectado"] is False, "Banner/anúncio não deveria acusar cabelo!"
        assert data_banner["curvatura_detectada"] is None
        print(f"[PASS] Banner publicitário rejeitado com aviso: {data_banner['mensagem_alerta']}")

        # 3b. Teste Específico: Homem Careca com Barba (Foto Real do Usuário)
        caminho_careca_real = os.path.join("scratch", "bald_with_beard.jpg")
        if os.path.exists(caminho_careca_real):
            with open(caminho_careca_real, "rb") as f:
                bald_bytes = f.read()
            files_bald = {"file": ("homem_careca_com_barba.jpg", bald_bytes, "image/jpeg")}
            resp_bald = tc.post("/diagnostico/imagem", files=files_bald)
            assert resp_bald.status_code == 200
            data_bald = resp_bald.json()
            assert data_bald["cabelo_detectado"] is False, "Homem careca com barba NÃO PODE ser detectado como cabelo!"
            assert data_bald["curvatura_detectada"] is None
            print(f"[PASS] Homem careca com barba rejeitado com sucesso! Alerta: {data_bald['mensagem_alerta']}")

        # 4. Teste de formato não suportado (HTTP 415)
        files_invalid = {"file": ("documento.pdf", b"%PDF-1.4 dummy", "application/pdf")}
        resp_invalid = tc.post("/diagnostico/imagem", files=files_invalid)
        assert resp_invalid.status_code == 415
        print("[PASS] Teste de formato não suportado (HTTP 415) bem-sucedido!")

        # 5. Teste de imagem corrompida (HTTP 422)
        files_corrupt = {"file": ("corrupt.jpg", b"corrupted bytes content not an image", "image/jpeg")}
        resp_corrupt = tc.post("/diagnostico/imagem", files=files_corrupt)
        assert resp_corrupt.status_code == 422
        print("[PASS] Teste de imagem corrompida (HTTP 422) bem-sucedido!")

if __name__ == "__main__":
    print("=== EXECUTANDO TESTES DE INTEGRAÇÃO DA API FASTAPI ===")
    test_health()
    test_recommendation_flow()
    test_feedback_flow()
    test_validation_errors()
    test_image_diagnosis()
    print("=== TODOS OS TESTES PASSARAM COM SUCESSO! ===")
