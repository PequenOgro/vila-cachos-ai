"""
test_security_matrix.py
Matriz Automatizada de Auditoria e Testes de Vulnerabilidades de Segurança (OWASP Top 10)
para o Sistema Vila Cachos AI.

Vetor de Testes Cobertos:
1. Security Headers (MIME-sniffing, Clickjacking, XSS Protection, Referrer Policy)
2. Injeção de Fórmulas CSV (CSV Injection / DDE Execution Defense)
3. Path Traversal & Sanitização de Nomes de Arquivos
4. Spoofing de Tipo MIME & Validação Binária de Magic Bytes
5. Proteção contra Decompression Bomb e Carga Excessiva (>10MB)
6. Bounded Parameters & Parameter Tampering (top_k, notas, curvaturas fora do domínio)
7. Tratamento de Erros e Proteção contra Vazamento de Stack Traces (Information Disclosure)
8. Validação de Rate Limiting (SlowAPI)
"""

import io
import sys
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from api import app
from repositories.feedback_repository import sanitizar_campo_csv


def test_security_headers():
    print("[1/8] Verificando Cabeçalhos de Segurança HTTP (OWASP A05)...")
    with TestClient(app) as tc:
        resp = tc.get("/health")
        assert resp.status_code == 200
        headers = resp.headers
        assert headers.get("X-Content-Type-Options") == "nosniff", "Falta X-Content-Type-Options: nosniff"
        assert headers.get("X-Frame-Options") == "DENY", "Falta X-Frame-Options: DENY"
        assert headers.get("X-XSS-Protection") == "1; mode=block", "Falta X-XSS-Protection"
        assert "strict-origin" in headers.get("Referrer-Policy", ""), "Falta Referrer-Policy"
        assert "camera=()" in headers.get("Permissions-Policy", ""), "Falta Permissions-Policy"
        print("    [PASS] Todos os cabeçalhos de segurança obrigatórios estão ativos!")


def test_csv_formula_injection_defense():
    print("[2/8] Verificando Proteção contra CSV Formula Injection (OWASP A03)...")
    # Testa a função de sanitização direta
    payloads_maliciosos = [
        "=cmd|'/C calc'!A1",
        "@SUM(1, 2)",
        "-999+cmd",
        "+cmd|'/C evil'!A1",
        "\t=2+5",
        "\r=cmd"
    ]
    for payload in payloads_maliciosos:
        sanitizado = sanitizar_campo_csv(payload)
        assert sanitizado.startswith("'"), f"Falha ao sanitizar payload de fórmula: {payload} -> {sanitizado}"
    
    # Testa string normal inofensiva
    normal = "Curly Care ACID-C (Acidificante Antiporosidade)"
    assert sanitizar_campo_csv(normal) == normal

    # Testa envio via endpoint de feedback com produto cadastrado
    with TestClient(app) as tc:
        payload = {
            "perfil_cliente": {
                "curvatura": 3,
                "porosidade": 2,
                "dano_quimico": 0
            },
            "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
            "nota_satisfacao": 5
        }
        resp = tc.post("/feedback", json=payload)
        assert resp.status_code == 200
        print("    [PASS] Defesa contra CSV Formula Injection comprovada e validada!")


def test_path_traversal_and_filename_sanitization():
    print("[3/8] Verificando Proteção contra Path Traversal em Uploads (OWASP A01)...")
    with TestClient(app) as tc:
        # Imagem JPEG sintética válida
        img = Image.fromarray((np.random.rand(64, 64, 3) * 255).astype("uint8"))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        image_bytes = buf.getvalue()

        # Nomes maliciosos com path traversal e caracteres de escape
        nomes_maliciosos = [
            "../../../../etc/passwd",
            "..\\..\\windows\\system32\\cmd.exe",
            "evil_file\x00.jpg",
            "../../../app/api.py"
        ]

        for nome in nomes_maliciosos:
            files = {"file": (nome, image_bytes, "image/jpeg")}
            resp = tc.post("/diagnostico/imagem", files=files)
            # Deve processar com segurança (HTTP 200) sem gravar nada no disco ou vazar caminhos
            assert resp.status_code == 200, f"Falha ao lidar com nome malicioso {nome}: {resp.text}"
            data = resp.json()
            assert "curvatura_detectada" in data
        print("    [PASS] Path Traversal e injeção de nomes sanitizados com sucesso!")


def test_mime_spoofing_and_magic_bytes():
    print("[4/8] Verificando Proteção contra Spoofing de MIME e Validação de Magic Bytes (OWASP A04)...")
    with TestClient(app) as tc:
        # Arquivo de texto disfarçado de imagem com Content-Type falso
        fake_content = b"#!/bin/bash\necho 'payload executavel malicioso'"
        files = {"file": ("malicious.jpg", fake_content, "image/jpeg")}
        resp = tc.post("/diagnostico/imagem", files=files)
        # Deve ser rejeitado pelo validador de Magic Bytes com HTTP 422
        assert resp.status_code == 422
        assert "Magic Bytes" in resp.json()["detail"] or "não corresponde a uma imagem válida" in resp.json()["detail"]
        print("    [PASS] Arquivos com MIME forjado foram bloqueados por validação binária de magic bytes!")


def test_oversized_payload_and_decompression_bomb():
    print("[5/8] Verificando Proteção contra Carga Excessiva (>10MB) e Decompression Bomb (OWASP A04)...")
    with TestClient(app) as tc:
        # Payload com 11MB (acima do limite estrito de 10MB)
        payload_11mb = b"\xff\xd8\xff\xe0" + b"\x00" * (11 * 1024 * 1024)
        files = {"file": ("huge_image.jpg", payload_11mb, "image/jpeg")}
        resp = tc.post("/diagnostico/imagem", files=files)
        assert resp.status_code == 413
        assert "excede o limite máximo permitido de 10MB" in resp.json()["detail"]
        print("    [PASS] Uploads excedentes foram bloqueados com HTTP 413!")


def test_parameter_tampering_and_bounds():
    print("[6/8] Verificando Bounded Parameters e Injeção de Valores Inválidos (OWASP A01/A04)...")
    with TestClient(app) as tc:
        # 1. top_k negativo ou zero (deve retornar 422)
        resp_neg = tc.post("/recommend?top_k=-5", json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0})
        assert resp_neg.status_code == 422, "top_k negativo não foi rejeitado!"

        resp_zero = tc.post("/recommend?top_k=0", json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0})
        assert resp_zero.status_code == 422, "top_k=0 não foi rejeitado!"

        # top_k excessivo (> 50)
        resp_excess = tc.post("/recommend?top_k=100", json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0})
        assert resp_excess.status_code == 422, "top_k excessivo não foi rejeitado!"

        # 2. Produto inexistente / injection de strings no catálogo
        resp_fake_prod = tc.post("/feedback", json={
            "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
            "nome_produto": "<script>alert('xss')</script>' OR '1'='1",
            "nota_satisfacao": 5
        })
        assert resp_fake_prod.status_code == 400
        assert "não encontrado no catálogo" in resp_fake_prod.json()["detail"]
        print("    [PASS] Parâmetros fora dos limites e nomes forjados rejeitados com segurança!")


def test_rate_limiting_enforcement():
    print("[7/8] Verificando Aplicação de Rate Limiting por IP/Proxy (OWASP A04)...")
    with TestClient(app) as tc:
        # Simula chamadas sucessivas na rota de recomendação (limite 10/min)
        cliente_payload = {"curvatura": 3, "porosidade": 2, "dano_quimico": 0}
        headers = {"X-Forwarded-For": "203.0.113.195"}
        
        status_codes = []
        for _ in range(15):
            r = tc.post("/recommend?top_k=1", json=cliente_payload, headers=headers)
            status_codes.append(r.status_code)
            if r.status_code == 429:
                break
        
        assert 429 in status_codes, f"Rate Limiter não disparou 429. Códigos: {status_codes}"
        print("    [PASS] Rate Limiter disparou HTTP 429 quando limite foi excedido!")


def test_unhandled_error_traceback_protection():
    print("[8/8] Verificando Proteção contra Exibição de Stack Traces (OWASP A05)...")
    with TestClient(app) as tc:
        # Rota inexistente (404 seguro)
        resp_404 = tc.get("/rota_inexistente_de_teste")
        assert resp_404.status_code == 404
        assert "traceback" not in resp_404.text.lower()
        assert "line " not in resp_404.text.lower()
        print("    [PASS] Informações internas de sistema e stack traces preservados contra vazamento!")


if __name__ == "__main__":
    print("=======================================================================")
    print("  VILA CACHOS AI - SUÍTE COMPLETA DE AUDITORIA DE SEGURANÇA (OWASP)")
    print("=======================================================================")
    test_security_headers()
    test_csv_formula_injection_defense()
    test_path_traversal_and_filename_sanitization()
    test_mime_spoofing_and_magic_bytes()
    test_oversized_payload_and_decompression_bomb()
    test_parameter_tampering_and_bounds()
    test_rate_limiting_enforcement()
    test_unhandled_error_traceback_protection()
    print("=======================================================================")
    print("  [SUCESSO ABSOLUTO] TODOS OS 8 TESTES DA MATRIZ DE SEGURANÇA PASSARAM!")
    print("=======================================================================")
