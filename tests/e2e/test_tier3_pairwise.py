"""
Tier 3 — Cross-Feature Pairwise Interactions & Cross-Layer Contract E2E Tests (>= 8 tests).
"""

from __future__ import annotations

import time
import unittest

import httpx

from tests.e2e.infra import (
    EXPECTED_SECURITY_HEADERS,
    FIXTURE_HAIR_TIPO3,
    IsolatedFeedbackApiEnv,
    ReadOnlySuiteEnv,
    ip_headers,
    load_hair_image_bytes,
    make_large_uniform_jpeg,
)


class TestT3PairwiseInteractions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def test_t3_p1_recommend_feedback_recommend_recalibration(self) -> None:
        with IsolatedFeedbackApiEnv() as iso_api:
            h_before = httpx.get(f"{iso_api.base_url}/health", timeout=10.0).json()
            profile = {
                "curvatura": 3,
                "porosidade": 3,
                "dano_quimico": 1,
                "alta_porosidade_quimica": 1,
            }
            rec1 = httpx.post(
                f"{iso_api.base_url}/recommend?top_k=3",
                json=profile,
                headers=ip_headers(),
                timeout=10.0,
            ).json()
            top1 = rec1["recomendacoes"][0]
            prod_name = top1["nome"]
            count_before = top1["avaliacoes_cluster"]

            fb = httpx.post(
                f"{iso_api.base_url}/feedback",
                json={
                    "perfil_cliente": profile,
                    "nome_produto": prod_name,
                    "nota_satisfacao": 5,
                },
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(fb.status_code, 200)
            self.assertEqual(fb.json()["cluster_afetado"], rec1["cluster_id"])

            rec2 = httpx.post(
                f"{iso_api.base_url}/recommend?top_k=3",
                json=profile,
                headers=ip_headers(),
                timeout=10.0,
            ).json()
            matched = [x for x in rec2["recomendacoes"] if x["nome"] == prod_name]
            self.assertEqual(len(matched), 1)
            self.assertEqual(matched[0]["avaliacoes_cluster"], count_before + 1)

            h_after = httpx.get(f"{iso_api.base_url}/health", timeout=10.0).json()
            self.assertEqual(h_after["total_clientes_historico"], h_before["total_clientes_historico"] + 1)

    def test_t3_p2_vision_to_recommend_pipeline(self) -> None:
        for curv in (2, 3, 4):
            img_bytes = load_hair_image_bytes(curvature=curv, fmt="JPEG")
            vis = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": (f"tipo_{curv}.jpg", img_bytes, "image/jpeg")},
                headers=ip_headers(),
                timeout=20.0,
            )
            self.assertEqual(vis.status_code, 200)
            vdata = vis.json()
            self.assertIs(vdata["cabelo_detectado"], True)
            sug = vdata["sugestao_perfil"]
            self.assertIsNotNone(sug)

            full_profile = {
                "curvatura": sug["curvatura"],
                "porosidade": sug["porosidade"],
                "dano_quimico": 0,
                "frizz_falta_definicao": sug["frizz_falta_definicao"],
                "ressecamento_opacidade": sug["ressecamento_opacidade"],
            }
            rec = httpx.post(
                f"{self.api.base_url}/recommend?top_k=3",
                json=full_profile,
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(rec.status_code, 200)
            rdata = rec.json()
            self.assertIn(rdata["cluster_id"], {0, 1, 2, 3})
            self.assertEqual(len(rdata["recomendacoes"]), 3)

    def test_t3_p3_browser_vision_apply_to_anamnese_step4(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")

        self.browser.upload_file('input[type="file"]', FIXTURE_HAIR_TIPO3)
        self.browser.wait_for_text("Aplicar diagnóstico", timeout=15.0)
        diag_text = self.browser.body_text()
        frizz_presente = "Frizz presente" in diag_text

        self.browser.click_button("Aplicar diagnóstico")
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 2 de 4")
        # Porosidade was pre-populated by aplicarDiagnosticoIA!
        self.assertFalse(self.browser.is_button_disabled("Continuar →"))
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 3 de 4")
        self.browser.click_button("100% Natural")
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 4 de 4")
        if frizz_presente:
            pressed = self.browser.eval_js(
                """
                (() => {
                    const btn = Array.from(document.querySelectorAll('button'))
                        .find(b => (b.innerText || '').includes('Frizz excessivo'));
                    return btn ? btn.getAttribute('aria-pressed') : null;
                })()
                """
            )
            self.assertEqual(pressed, "true")
        self.browser.click_button("Ver minha prescrição")
        self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t3_p4_admin_filters_view_toggle_and_modal(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)
        self.browser.click_button("3. Catálogo & Fórmulas")
        self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")

        self.browser.click_button("Tipo 4", exact=True)
        self.browser.click_button("Curly Care (")
        self.browser.set_input_value('input[placeholder*="Buscar por cosmético"]', "Manteiga")
        self.browser.wait_for_text("Exibindo 1 de 27 cosméticos catalogados")

        self.browser.click_button("Tabela")
        self.browser.wait_for("document.querySelectorAll('tbody tr').length === 1")
        self.browser.click_button("Ver Detalhes")
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') !== null")
        modal_text = self.browser.eval_js("document.querySelector('[role=\"dialog\"]').innerText")
        self.assertIn("PROD_02", modal_text)
        self.assertIn("Curly Care Manteiga Nutritiva", modal_text)

        self.browser.press_escape()
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') === null")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t3_p5_admin_simulador_live_api_parity(self) -> None:
        expected_profile = {
            "curvatura": 4,
            "porosidade": 3,
            "dano_quimico": 1,
            "transicao_capilar": 0,
            "alta_porosidade_quimica": 1,
            "frizz_falta_definicao": 1,
            "ressecamento_opacidade": 1,
            "couro_sensivel_oleoso": 0,
        }
        api_rec = httpx.post(
            f"{self.api.base_url}/recommend?top_k=3",
            json=expected_profile,
            headers=ip_headers(),
            timeout=10.0,
        ).json()

        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)
        self.browser.click_button("4. Simulador Clínico (XAI)")
        self.browser.wait_for_text("Simulador & Auditoria Tricológica em Tempo Real")

        self.browser.click_button("4 • Crespo")
        self.browser.click_button("Alta", exact=True)
        self.browser.click_button("Com Química")
        self.browser.eval_js(
            """
            (() => {
                const labels = Array.from(document.querySelectorAll('label'));
                const target = labels.find(l => (l.innerText || '').includes('Ressecamento'));
                const cb = target ? target.querySelector('input[type="checkbox"]') : null;
                if (cb && !cb.checked) cb.click();
            })()
            """
        )
        self.browser.click_button("Disparar Recomendação")
        self.browser.wait_for_text(f"Cluster Clínico #{api_rec['cluster_id']}", timeout=10.0)
        body = self.browser.body_text()
        for item in api_rec["recomendacoes"]:
            self.assertIn(item["nome"], body)
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t3_p6_memory_stress_3000x3000_below_512mb(self) -> None:
        large_jpg = make_large_uniform_jpeg(3000, 3000)
        before_stats = self.api.memory_stats_mb()
        for i in range(5):
            rv = httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": (f"stress_{i}.jpg", large_jpg, "image/jpeg")},
                headers=ip_headers(),
                timeout=30.0,
            )
            self.assertEqual(rv.status_code, 200)
            rh = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
            self.assertEqual(rh.status_code, 200)
            rr = httpx.post(
                f"{self.api.base_url}/recommend",
                json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(rr.status_code, 200)

        after_stats = self.api.memory_stats_mb()
        self.assertLess(after_stats["rss_mb"], 512.0, f"RSS >= 512MB: {after_stats}")
        self.assertLess(after_stats["peak_wset_mb"], 512.0, f"Peak WSet >= 512MB: {after_stats}")
        self.assertLess(after_stats["handles"] - before_stats["handles"], 200.0)

    def test_t3_p7_security_headers_and_cors_across_all_endpoints(self) -> None:
        checks = [
            httpx.get(f"{self.api.base_url}/", headers={"Origin": "http://127.0.0.1:5173"}, timeout=10.0),
            httpx.get(f"{self.api.base_url}/health", headers={"Origin": "http://127.0.0.1:5173"}, timeout=10.0),
            httpx.get(f"{self.api.base_url}/catalogo", headers={"Origin": "http://127.0.0.1:5173"}, timeout=10.0),
            httpx.post(
                f"{self.api.base_url}/recommend",
                json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                headers={**ip_headers(), "Origin": "http://127.0.0.1:5173"},
                timeout=10.0,
            ),
            httpx.post(
                f"{self.api.base_url}/recommend",
                json={},
                headers={**ip_headers(), "Origin": "http://127.0.0.1:5173"},
                timeout=10.0,
            ),
            httpx.post(
                f"{self.api.base_url}/diagnostico/imagem",
                files={"file": ("x.txt", b"hello", "text/plain")},
                headers={**ip_headers(), "Origin": "http://127.0.0.1:5173"},
                timeout=10.0,
            ),
        ]
        for resp in checks:
            for hdr, val in EXPECTED_SECURITY_HEADERS.items():
                self.assertEqual(resp.headers.get(hdr), val, f"Missing/wrong {hdr} on {resp.url}")
            self.assertEqual(resp.headers.get("access-control-allow-origin"), "*")

    def test_t3_p8_health_and_catalog_live_admin_sync(self) -> None:
        health = httpx.get(f"{self.api.base_url}/health", timeout=10.0).json()
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)
        body = self.browser.body_text()
        self.assertIn(str(health["total_clientes_historico"]), body)
        self.assertIn(f"{health['silhouette_score']:.3f}", body)

        self.browser.reset_logs()
        self.browser.click_button("Recarregar dados")
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            self.browser.drain_events(0.1)
            urls = [r["url"] for r in self.browser.network_responses if r["status"] == 200]
            if any("/health" in u for u in urls) and any("/catalogo" in u for u in urls):
                break
            time.sleep(0.1)
        urls = [r["url"] for r in self.browser.network_responses if r["status"] == 200]
        self.assertTrue(any("/health" in u for u in urls), f"Missing /health reload: {urls}")
        self.assertTrue(any("/catalogo" in u for u in urls), f"Missing /catalogo reload: {urls}")
