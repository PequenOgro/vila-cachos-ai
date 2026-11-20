"""
Tier 4 — Real-World End-to-End Browser + Backend Application Scenarios (>= 6 scenarios).
"""

from __future__ import annotations

import time
import unittest

import httpx

from tests.e2e.infra import (
    CSV_PATH,
    FIXTURE_HAIR_TIPO3,
    IsolatedFeedbackApiEnv,
    ReadOnlySuiteEnv,
    ViteDevServer,
    make_non_hair_skin_jpeg,
    write_temp_file,
)


class TestT4RealWorldScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def test_t4_s1_kiosk_photo_ai_and_5star_feedback_persistence(self) -> None:
        iso_env = IsolatedFeedbackApiEnv()
        iso_api = iso_env.start()
        iso_ui = ViteDevServer(api_url=iso_api.base_url).start()
        try:
            lines_before = len(CSV_PATH.read_text(encoding="utf-8").splitlines())

            self.browser.navigate(f"{iso_ui.base_url}/")
            self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
            self.browser.click_button("Iniciar Diagnóstico Capilar")
            self.browser.wait_for_text("Passo 1 de 4")

            self.browser.upload_file('input[type="file"]', FIXTURE_HAIR_TIPO3)
            self.browser.wait_for_text("Aplicar diagnóstico", timeout=15.0)
            self.browser.click_button("Aplicar diagnóstico")
            self.browser.click_button("Continuar →")

            self.browser.wait_for_text("Passo 2 de 4")
            self.browser.click_button("Alta")
            self.browser.click_button("Continuar →")

            self.browser.wait_for_text("Passo 3 de 4")
            self.browser.click_button("Danificado")
            self.browser.click_button("Continuar →")

            self.browser.wait_for_text("Passo 4 de 4")
            self.browser.click_button("Ressecamento e pontas secas")
            self.browser.click_button("Ver minha prescrição")

            self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
            body = self.browser.body_text()
            self.assertIn("Cluster Clínico #", body)
            self.assertIn("transparência algorítmica (xai)", body.lower())

            imgs = self.browser.verify_images_loaded("article img", min_count=3)
            self.assertEqual(len(imgs), 3)
            for im in imgs:
                self.assertTrue(im["complete"] and im["naturalWidth"] > 0, f"Broken img: {im}")

            # Click 5-star rating on first product card
            self.browser.click_selector('article button[aria-label="5 estrelas"]')
            self.browser.wait_for(
                "document.body.innerText.includes('recalibrad') || document.body.innerText.includes('Avaliação')",
                timeout=10.0,
            )
            lines_after = len(CSV_PATH.read_text(encoding="utf-8").splitlines())
            self.assertEqual(lines_after, lines_before + 1)
            self.assertEqual(self.browser.page_exceptions, [])
        finally:
            iso_ui.stop()
            iso_env.stop_and_restore()

    def test_t4_s2_non_hair_rejection_and_manual_recovery(self) -> None:
        tmp_skin = write_temp_file(make_non_hair_skin_jpeg(), suffix=".jpg")
        try:
            self.browser.navigate(f"{self.ui.base_url}/")
            self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
            self.browser.click_button("Iniciar Diagnóstico Capilar")
            self.browser.wait_for_text("Passo 1 de 4")

            self.browser.upload_file('input[type="file"]', tmp_skin)
            self.browser.wait_for_text("Nenhum cabelo detectado na foto", timeout=15.0)

            self.browser.click_button("Cacheado")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 2 de 4")
            self.browser.click_button("Média")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 3 de 4")
            self.browser.click_button("100% Natural")
            self.browser.click_button("Continuar →")
            self.browser.wait_for_text("Passo 4 de 4")
            self.browser.click_button("Frizz excessivo")
            self.browser.click_button("Ver minha prescrição")

            self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
            imgs = self.browser.verify_images_loaded("article img", min_count=3)
            self.assertEqual(len(imgs), 3)
            self.assertEqual(self.browser.page_exceptions, [])
        finally:
            tmp_skin.unlink(missing_ok=True)

    def test_t4_s3_type_4c_chemical_repair_acid_c_top1(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.browser.click_button("Crespo")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 2 de 4")
        self.browser.click_button("Alta")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 3 de 4")
        self.browser.click_button("Danificado")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 4 de 4")
        self.browser.click_button("Ressecamento e pontas secas")
        self.browser.click_button("Ver minha prescrição")

        self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
        top1_title = self.browser.eval_js(
            "document.querySelector('article h3') ? document.querySelector('article h3').innerText : ''"
        )
        self.assertEqual(top1_title, "Curly Care ACID-C (Acidificante Antiporosidade)")
        imgs = self.browser.verify_images_loaded("article img", min_count=3)
        self.assertTrue(all(im["complete"] and im["naturalWidth"] > 0 for im in imgs))
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t4_s4_salon_manager_full_admin_audit(self) -> None:
        health = httpx.get(f"{self.api.base_url}/health", timeout=10.0).json()

        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)
        dash_text = self.browser.body_text()
        self.assertNotIn("Modo Resiliente", dash_text)
        self.assertNotIn("Operação Resiliente Local", dash_text)
        self.assertIn(str(health["total_clientes_historico"]), dash_text)
        self.assertIn(f"{health['silhouette_score']:.3f}", dash_text)

        # Tab 2: Telemetria & RNF-12
        self.browser.click_button("2. Telemetria & RNF-12")
        self.browser.wait_for_text("Telemetria Tricológica & Validação Científica (RNF-12)")
        tel_text = self.browser.body_text()
        for pid in range(4):
            self.assertIn(f"Persona {pid}", tel_text)
        self.assertIn(self.api.base_url, tel_text)

        # Tab 3: Catálogo & Fórmulas (all 27 images + PROD_14, PROD_17, PROD_21 modal inspection)
        self.browser.click_button("3. Catálogo & Fórmulas")
        self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")
        all_imgs = self.browser.verify_images_loaded("section img", min_count=27)
        self.assertEqual(len(all_imgs), 27)
        self.assertTrue(all(im["complete"] and im["naturalWidth"] > 0 for im in all_imgs))

        for query, expected_id in (
            ("Mister Jelly", "PROD_14"),
            ("NO SPUME!", "PROD_17"),
            ("FIX U", "PROD_21"),
        ):
            self.browser.set_input_value('input[placeholder*="Buscar por cosmético"]', query)
            self.browser.wait_for_text("Exibindo 1 de 27 cosméticos catalogados")
            self.browser.click_button("Inspecionar Ficha & Afinidades")
            self.browser.wait_for("document.querySelector('[role=\"dialog\"]') !== null")
            modal_txt = self.browser.eval_js("document.querySelector('[role=\"dialog\"]').innerText")
            self.assertIn(expected_id, modal_txt)
            modal_imgs = self.browser.verify_images_loaded('[role="dialog"] img', min_count=1)
            self.assertTrue(modal_imgs[0]["complete"] and modal_imgs[0]["naturalWidth"] > 0)
            self.browser.press_escape()
            self.browser.wait_for("document.querySelector('[role=\"dialog\"]') === null")
        self.browser.click_button("Limpar todos os filtros")

        # Tab 4: Simulador Clínico
        self.browser.click_button("4. Simulador Clínico (XAI)")
        self.browser.wait_for_text("Simulador & Auditoria Tricológica em Tempo Real")
        self.browser.click_button("Disparar Recomendação")
        self.browser.wait_for_text("Top 3 Cosméticos Prescritos", timeout=10.0)
        sim_imgs = self.browser.verify_images_loaded("section img", min_count=3)
        self.assertTrue(all(im["complete"] and im["naturalWidth"] > 0 for im in sim_imgs))
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t4_s5_multi_customer_kiosk_session_reset(self) -> None:
        # Customer A: Crespo + Alta + Danificado
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.browser.click_button("Crespo")
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
        top1_a = self.browser.eval_js("document.querySelector('article h3').innerText")
        persona_a = self.browser.eval_js("document.querySelector('h1').innerText")

        # Reset for Customer B
        self.browser.click_button("Realizar novo diagnóstico")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")

        # Customer B: Ondulado + Baixa + 100% Natural
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.browser.click_button("Ondulado")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 2 de 4")
        self.browser.click_button("Baixa")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 3 de 4")
        self.browser.click_button("100% Natural")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 4 de 4")
        self.browser.click_button("Ver minha prescrição")
        self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
        top1_b = self.browser.eval_js("document.querySelector('article h3').innerText")
        persona_b = self.browser.eval_js("document.querySelector('h1').innerText")

        self.assertTrue(
            top1_a != top1_b or persona_a != persona_b,
            f"Expected distinct prescription after session reset: A=({persona_a}, {top1_a}) B=({persona_b}, {top1_b})",
        )
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t4_s6_mobile_viewport_390x844_end_to_end(self) -> None:
        self.browser.set_viewport(390, 844, mobile=True)
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)

        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)
        self.browser.click_button("Cacheado")
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 2 de 4")
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)
        self.browser.click_button("Média")
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 3 de 4")
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)
        self.browser.click_button("100% Natural")
        self.browser.click_button("Continuar →")

        self.browser.wait_for_text("Passo 4 de 4")
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)
        self.browser.click_button("Ver minha prescrição")

        self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)
        self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)

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
            self.assertLessEqual(self.browser.horizontal_overflow_px(), 1)
        self.assertEqual(self.browser.page_exceptions, [])
        self.assertEqual(self.browser.console_errors, [])
