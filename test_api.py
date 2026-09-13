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

if __name__ == "__main__":
    print("=== EXECUTANDO TESTES DE INTEGRAÇÃO DA API FASTAPI ===")
    test_health()
    test_recommendation_flow()
    test_feedback_flow()
    test_validation_errors()
    print("=== TODOS OS TESTES PASSARAM COM SUCESSO! ===")
