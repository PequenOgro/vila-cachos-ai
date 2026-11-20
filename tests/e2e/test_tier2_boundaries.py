"""
Tier 2 — Boundary Value Analysis, Invalid Inputs, Error Handling & Security E2E Tests
(>= 41 test methods, >= 5 per F1–F8, >= 6 for F5 Vision rejections).
"""

from __future__ import annotations

import time
import unittest

import httpx

from tests.e2e.infra import (
    CSV_PATH,
    EXPECTED_SECURITY_HEADERS,
    FIXTURE_HAIR_TIPO3,
    CdpBrowser,
    IsolatedFeedbackApiEnv,
    ReadOnlySuiteEnv,
    ViteDevServer,
    get_free_port,
    ip_headers,
    make_large_uniform_jpeg,
    make_non_hair_banner_jpeg,
    make_non_hair_grid_jpeg,
    make_non_hair_skin_jpeg,
    next_client_ip,
    write_temp_file,
)


class TestT2F1HealthRootBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t2_f1_nonexistent_route_404_no_traceback(self) -> None:
        r = httpx.get(f"{self.api.base_url}/nonexistent-route-e2e", timeout=10.0)
        self.assertEqual(r.status_code, 404)
        self.assertNotIn("traceback", r.text.lower())

    def test_t2_f1_post_health_returns_405(self) -> None:
        r = httpx.post(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f1_put_root_returns_405(self) -> None:
        r = httpx.put(f"{self.api.base_url}/", timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f1_delete_health_returns_405(self) -> None:
        r = httpx.delete(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f1_health_ignores_unexpected_query_params(self) -> None:
        r = httpx.get(f"{self.api.base_url}/health?debug=1&unknown=abc", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "operacional")


class TestT2F2CatalogBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t2_f2_post_catalogo_returns_405(self) -> None:
        r = httpx.post(f"{self.api.base_url}/catalogo", json={}, timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f2_delete_catalogo_returns_405(self) -> None:
        r = httpx.delete(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f2_patch_catalogo_returns_405(self) -> None:
        r = httpx.patch(f"{self.api.base_url}/catalogo", json={}, timeout=10.0)
        self.assertEqual(r.status_code, 405)

    def test_t2_f2_catalog_ignores_query_params_and_keeps_27_items(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo?marca=Inexistente&limit=1", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 27)

    def test_t2_f2_catalog_exact_brand_distribution_and_unique_names(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        items = r.json()
        counts = {}
        for item in items:
            counts[item["marca"]] = counts.get(item["marca"], 0) + 1
        self.assertEqual(counts, {"Arvensis": 8, "Curly Care": 8, "Deva Curl": 7, "Kah-Noa": 4})
        names = [item["nome"] for item in items]
        self.assertEqual(len(names), len(set(names)))


class TestT2F3RecommendBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t2_f3_curvatura_out_of_range_returns_422(self) -> None:
        for bad_c in (1, 5, 0, -2):
            r = httpx.post(
                f"{self.api.base_url}/recommend",
                json={"curvatura": bad_c, "porosidade": 2, "dano_quimico": 0},
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 422, f"Expected 422 for curvatura={bad_c}")

    def test_t2_f3_porosidade_out_of_range_returns_422(self) -> None:
        for bad_p in (0, 4, -1):
            r = httpx.post(
                f"{self.api.base_url}/recommend",
                json={"curvatura": 3, "porosidade": bad_p, "dano_quimico": 0},
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 422, f"Expected 422 for porosidade={bad_p}")

    def test_t2_f3_binary_invalid_422_and_extra_fields_ignored_200(self) -> None:
        bad = httpx.post(
            f"{self.api.base_url}/recommend",
            json={"curvatura": 3, "porosidade": 2, "dano_quimico": 2},
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(bad.status_code, 422)

        ok = httpx.post(
            f"{self.api.base_url}/recommend",
            json={
                "curvatura": 3,
                "porosidade": 2,
                "dano_quimico": 0,
                "densidade": 2,
                "espessura": "fina",
            },
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(ok.status_code, 200)

    def test_t2_f3_top_k_boundaries_422_and_50_capped_27(self) -> None:
        profile = {"curvatura": 3, "porosidade": 2, "dano_quimico": 0}
        for bad_k in (0, -1, 51, "abc"):
            r = httpx.post(
                f"{self.api.base_url}/recommend?top_k={bad_k}",
                json=profile,
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 422, f"Expected 422 for top_k={bad_k}")

        r_max = httpx.post(
            f"{self.api.base_url}/recommend?top_k=50",
            json=profile,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_max.status_code, 200)
        self.assertEqual(len(r_max.json()["recomendacoes"]), 27)

    def test_t2_f3_malformed_json_and_missing_required_fields_422(self) -> None:
        r_bad_json = httpx.post(
            f"{self.api.base_url}/recommend",
            content=b"{broken json",
            headers={**ip_headers(), "Content-Type": "application/json"},
            timeout=10.0,
        )
        self.assertEqual(r_bad_json.status_code, 422)

        r_empty = httpx.post(
            f"{self.api.base_url}/recommend",
            json={},
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_empty.status_code, 422)


class TestT2F4FeedbackBoundaries(unittest.TestCase):
    """Isolated `/feedback` boundary & security tests."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.iso_env = IsolatedFeedbackApiEnv()
        cls.api = cls.iso_env.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.iso_env.stop_and_restore()

    def test_t2_f4_unknown_product_and_xss_sqli_returns_400(self) -> None:
        for name in ("Produto Inexistente", "<script>alert('xss')</script>' OR '1'='1"):
            r = httpx.post(
                f"{self.api.base_url}/feedback",
                json={
                    "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                    "nome_produto": name,
                    "nota_satisfacao": 5,
                },
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 400)
            self.assertIn("não encontrado", r.json()["detail"])

    def test_t2_f4_nota_out_of_bounds_0_and_6_returns_422(self) -> None:
        for bad_nota in (0, 6, -1):
            r = httpx.post(
                f"{self.api.base_url}/feedback",
                json={
                    "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                    "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
                    "nota_satisfacao": bad_nota,
                },
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 422)

    def test_t2_f4_nome_produto_max_length_boundary(self) -> None:
        r_201 = httpx.post(
            f"{self.api.base_url}/feedback",
            json={
                "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                "nome_produto": "A" * 201,
                "nota_satisfacao": 4,
            },
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_201.status_code, 422)

        r_200 = httpx.post(
            f"{self.api.base_url}/feedback",
            json={
                "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                "nome_produto": "A" * 200,
                "nota_satisfacao": 4,
            },
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_200.status_code, 400)

    def test_t2_f4_feedback_rate_limit_11th_returns_429_with_headers(self) -> None:
        ip = next_client_ip()
        payload = {
            "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
            "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
            "nota_satisfacao": 5,
        }
        for i in range(10):
            r = httpx.post(
                f"{self.api.base_url}/feedback",
                json=payload,
                headers=ip_headers(ip),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 200, f"Req #{i+1} unexpectedly returned {r.status_code}")

        r11 = httpx.post(
            f"{self.api.base_url}/feedback",
            json=payload,
            headers=ip_headers(ip),
            timeout=10.0,
        )
        self.assertEqual(r11.status_code, 429)
        for hdr, val in EXPECTED_SECURITY_HEADERS.items():
            self.assertEqual(r11.headers.get(hdr), val)

    def test_t2_f4_csv_formula_prefix_rejected_and_csv_intact(self) -> None:
        csv_before = CSV_PATH.read_text(encoding="utf-8")
        for evil in ("=cmd|'/C calc'!A0", "@SUM(1+1)*cmd"):
            r = httpx.post(
                f"{self.api.base_url}/feedback",
                json={
                    "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                    "nome_produto": evil,
                    "nota_satisfacao": 3,
                },
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 400)
        self.assertEqual(CSV_PATH.read_text(encoding="utf-8"), csv_before)


class TestT2F5VisionBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t2_f5_unsupported_mime_returns_415(self) -> None:
        for fname, mime in (
            ("doc.pdf", "application/pdf"),
            ("anim.gif", "image/gif"),
            ("notes.txt", "text/plain"),
        ):
            r = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": (fname, b"%PDF-1.4 fake payload bytes", mime)},
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 415, f"Expected 415 for {mime}")

    def test_t2_f5_spoofed_mime_tiny_bytes_and_missing_file_422(self) -> None:
        r_spoof = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("shell.jpg", b"#!/bin/bash\nrm -rf /", "image/jpeg")},
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_spoof.status_code, 422)

        r_tiny = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("tiny.jpg", b"\xff\xd8\xff\xe0abc", "image/jpeg")},
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_tiny.status_code, 422)

        r_missing = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r_missing.status_code, 422)

    def test_t2_f5_oversized_payload_10mb_plus_1_returns_413(self) -> None:
        ten_mb = 10 * 1024 * 1024
        over = b"\xff\xd8\xff\xe0" + (b"\x00" * (ten_mb + 1 - 4))
        r_over = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("huge.jpg", over, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r_over.status_code, 413)

        exact = b"\xff\xd8\xff\xe0" + (b"\x00" * (ten_mb - 4))
        r_exact = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("exact10mb.jpg", exact, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertNotEqual(r_exact.status_code, 413)
        self.assertEqual(r_exact.status_code, 422)

    def test_t2_f5_corrupt_jpeg_magic_bytes_returns_422(self) -> None:
        corrupt = b"\xff\xd8\xff\xe0" + b"NOT_A_VALID_JPEG_STREAM_1234567890" * 5
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("corrupt.jpg", corrupt, "image/jpeg")},
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 422)

    def test_t2_f5_path_traversal_and_null_byte_filenames_safe(self) -> None:
        real_jpg = FIXTURE_HAIR_TIPO3.read_bytes()
        for bad_name in ("../../../../etc/passwd.jpg", "evil\x00.jpg"):
            r = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": (bad_name, real_jpg, "image/jpeg")},
                headers=ip_headers(),
                timeout=20.0,
            )
            self.assertEqual(r.status_code, 200)
            self.assertIs(r.json()["cabelo_detectado"], True)

    def test_t2_f5_non_hair_rejections_and_5000x5000_bomb_422(self) -> None:
        non_hair_samples = [
            ("skin.jpg", make_non_hair_skin_jpeg()),
            ("banner.jpg", make_non_hair_banner_jpeg()),
            ("grid.jpg", make_non_hair_grid_jpeg()),
        ]
        for fname, data in non_hair_samples:
            r = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": (fname, data, "image/jpeg")},
                headers=ip_headers(),
                timeout=20.0,
            )
            self.assertEqual(r.status_code, 200, f"Unexpected status for {fname}")
            j = r.json()
            self.assertIs(j["cabelo_detectado"], False, f"{fname} falsely detected hair: {j}")
            self.assertIsNone(j["curvatura_detectada"])
            self.assertIsNone(j["sugestao_perfil"])
            self.assertIs(j["requer_confirmacao_humana"], True)
            self.assertTrue(bool(j["mensagem_alerta"]))

        bomb_bytes = make_large_uniform_jpeg(5000, 5000)
        r_bomb = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("bomb_25mp.jpg", bomb_bytes, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r_bomb.status_code, 422)


class TestT2F6SecurityAndRateLimit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t2_f6_recommend_rate_limit_11th_returns_429(self) -> None:
        ip = next_client_ip()
        payload = {"curvatura": 3, "porosidade": 2, "dano_quimico": 0}
        for i in range(10):
            r = httpx.post(
                f"{self.api.base_url}/recommend",
                json=payload,
                headers=ip_headers(ip),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 200, f"Req #{i+1} got {r.status_code}")
        r11 = httpx.post(
            f"{self.api.base_url}/recommend",
            json=payload,
            headers=ip_headers(ip),
            timeout=10.0,
        )
        self.assertEqual(r11.status_code, 429)
        for hdr, val in EXPECTED_SECURITY_HEADERS.items():
            self.assertEqual(r11.headers.get(hdr), val)

    def test_t2_f6_vision_rate_limit_21st_returns_429(self) -> None:
        ip = next_client_ip()
        skin_jpg = make_non_hair_skin_jpeg(160, 160)
        for i in range(20):
            r = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": ("s.jpg", skin_jpg, "image/jpeg")},
                headers=ip_headers(ip),
                timeout=15.0,
            )
            self.assertEqual(r.status_code, 200, f"Vision req #{i+1} got {r.status_code}")
        r21 = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("s.jpg", skin_jpg, "image/jpeg")},
            headers=ip_headers(ip),
            timeout=15.0,
        )
        self.assertEqual(r21.status_code, 429)

    def test_t2_f6_rate_limit_isolated_between_distinct_ips(self) -> None:
        ip_a = next_client_ip()
        ip_b = next_client_ip()
        payload = {"curvatura": 2, "porosidade": 1, "dano_quimico": 0}
        for _ in range(11):
            r_a = httpx.post(f"{self.api.base_url}/recommend", json=payload, headers=ip_headers(ip_a), timeout=10.0)
        self.assertEqual(r_a.status_code, 429)
        r_b = httpx.post(f"{self.api.base_url}/recommend", json=payload, headers=ip_headers(ip_b), timeout=10.0)
        self.assertEqual(r_b.status_code, 200)

    def test_t2_f6_owasp_headers_present_on_404_and_422(self) -> None:
        r_404 = httpx.get(f"{self.api.base_url}/does-not-exist-sec", timeout=10.0)
        self.assertEqual(r_404.status_code, 404)
        for hdr, val in EXPECTED_SECURITY_HEADERS.items():
            self.assertEqual(r_404.headers.get(hdr), val)

        r_422 = httpx.post(f"{self.api.base_url}/recommend", json={}, headers=ip_headers(), timeout=10.0)
        self.assertEqual(r_422.status_code, 422)
        for hdr, val in EXPECTED_SECURITY_HEADERS.items():
            self.assertEqual(r_422.headers.get(hdr), val)

    def test_t2_f6_cors_no_credentials_and_strict_methods(self) -> None:
        r = httpx.options(
            f"{self.api.base_url}/catalogo",
            headers={
                "Origin": "http://127.0.0.1:5173",
                "Access-Control-Request-Method": "GET",
            },
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.headers.get("access-control-allow-credentials"), "true")
        methods = r.headers.get("access-control-allow-methods", "")
        self.assertNotIn("DELETE", methods)
        self.assertNotIn("PUT", methods)


class TestT2F7TotemUiBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def test_t2_f7_continuar_disabled_until_selection_on_steps_1_2_3(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")

        self.browser.wait_for_text("Passo 1 de 4")
        self.assertTrue(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Cacheado")
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 2 de 4")
        self.assertTrue(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Média")
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 3 de 4")
        self.assertTrue(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("100% Natural")
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))

    def test_t2_f7_back_navigation_preserves_step1_and_returns_to_inicio(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.browser.click_button("Crespo")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 2 de 4")

        self.browser.click_button("← Voltar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))

        self.browser.click_button("← Voltar")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f7_passo_curvatura_non_hair_upload_shows_alert(self) -> None:
        tmp_img = write_temp_file(make_non_hair_banner_jpeg(), suffix=".jpg")
        try:
            self.browser.navigate(f"{self.ui.base_url}/")
            self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
            self.browser.click_button("Iniciar Diagnóstico Capilar")
            self.browser.wait_for_text("Passo 1 de 4")
            self.browser.upload_file('input[type="file"]', tmp_img)
            self.browser.wait_for_text("Nenhum cabelo detectado na foto", timeout=15.0)
            body = self.browser.body_text()
            self.assertIn("Tirar outra foto da mecha", body)
            self.assertEqual(self.browser.page_exceptions, [])
        finally:
            tmp_img.unlink(missing_ok=True)

    def test_t2_f7_unknown_frontend_route_renders_404_cleanly(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/rota-inexistente-e2e")
        self.browser.wait_for_text("404", timeout=10.0)
        self.assertIn("Page not found", self.browser.body_text())
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f7_offline_api_fallback_renders_demo_resultado(self) -> None:
        dead_port = get_free_port()
        offline_ui = ViteDevServer(api_url=f"http://127.0.0.1:{dead_port}").start()
        try:
            self.browser.navigate(f"{offline_ui.base_url}/")
            self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
            self.browser.click_button("Iniciar Diagnóstico Capilar")
            self.browser.wait_for_text("Passo 1 de 4")
            self.browser.click_button("Cacheado")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 2 de 4")
            self.browser.click_button("Alta")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 3 de 4")
            self.browser.click_button("Danificado")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 4 de 4")
            self.browser.click_button("Ver minha prescrição")
            self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
            body = self.browser.body_text()
            self.assertIn("Prescrição Personalizada", body)
            self.assertEqual(self.browser.eval_js("document.querySelectorAll('article').length"), 3)
            self.assertEqual(self.browser.page_exceptions, [])
        finally:
            offline_ui.stop()


class TestT2F8AdminUiBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def _open_catalogo(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)
        self.browser.click_button("3. Catálogo & Fórmulas")
        self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")

    def test_t2_f8_catalogo_zero_match_search_and_clear_filters(self) -> None:
        self._open_catalogo()
        self.browser.set_input_value('input[placeholder*="Buscar por cosmético"]', "XYZ_SEM_MATCH_999")
        self.browser.wait_for_text("Exibindo 0 de 27 cosméticos catalogados")
        self.browser.click_button("Limpar todos os filtros")
        self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f8_catalogo_combined_curvature_and_brand_filters(self) -> None:
        catalog = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0).json()
        expected_count = sum(
            1 for p in catalog if p["marca"] == "Kah-Noa" and 4 in p["curvaturas_indicadas"]
        )
        self._open_catalogo()
        self.browser.click_button("Tipo 4", exact=True)
        self.browser.click_button("Kah-Noa (4)")
        self.browser.wait_for_text(f"Exibindo {expected_count} de 27 cosméticos catalogados")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f8_product_modal_closes_via_escape_and_x_button(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Visão Executiva & Funil de Inteligência Capilar")
        self.browser.click_button("Inspecionar Ficha")
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') !== null")
        self.browser.press_escape()
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') === null")

        self.browser.click_button("Inspecionar Ficha")
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') !== null")
        self.browser.click_button("Fechar detalhes", exact=True)
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') === null")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f8_mobile_390x844_admin_zero_horizontal_overflow(self) -> None:
        self.browser.set_viewport(390, 844, mobile=True)
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Visão Executiva & Funil de Inteligência Capilar")
        for tab in (
            "1. Visão Geral (Dashboard)",
            "2. Telemetria & RNF-12",
            "3. Catálogo & Fórmulas",
            "4. Simulador Clínico (XAI)",
        ):
            self.browser.click_button(tab)
            time.sleep(0.2)
            overflow = self.browser.horizontal_overflow_px()
            self.assertLessEqual(overflow, 1, f"Horizontal overflow ({overflow}px) on mobile tab {tab}")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t2_f8_admin_offline_resilient_fallback_mode(self) -> None:
        dead_port = get_free_port()
        offline_ui = ViteDevServer(api_url=f"http://127.0.0.1:{dead_port}").start()
        try:
            self.browser.navigate(f"{offline_ui.base_url}/admin")
            self.browser.wait_for_text("Operação Resiliente Local", timeout=10.0)
            body = self.browser.body_text()
            self.assertIn("resiliente", body.lower())
            self.browser.click_button("3. Catálogo & Fórmulas")
            self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")
            self.assertEqual(self.browser.page_exceptions, [])
        finally:
            offline_ui.stop()
