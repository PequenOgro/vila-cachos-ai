"""
Tier 1 — Core Single-Feature Positive Behavior E2E Tests (>= 40 tests, >= 5 per F1–F8).

All tests are opaque-box and derived from ORIGINAL_REQUEST.md and PROJECT.md contracts.
"""

from __future__ import annotations

import time
import unittest
from typing import Dict

import httpx

from tests.e2e.infra import (
    CSV_PATH,
    EXPECTED_SECURITY_HEADERS,
    FIXTURE_HAIR_TIPO3,
    IsolatedFeedbackApiEnv,
    ReadOnlySuiteEnv,
    ip_headers,
    load_hair_image_bytes,
)

EXPECTED_BRANDS = {"Arvensis", "Curly Care", "Deva Curl", "Kah-Noa"}
EXPECTED_QUEIXA_KEYS = {
    "ressecamento_opacidade",
    "alta_porosidade_quimica",
    "frizz_falta_definicao",
    "transicao_capilar",
    "couro_sensivel_oleoso",
}


class TestT1F1HealthAndRoot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t1_f1_root_endpoint_schema(self) -> None:
        r = httpx.get(f"{self.api.base_url}/", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("status"), "online")
        self.assertIn("api", data)
        self.assertIn("versao", data)
        self.assertEqual(data.get("docs"), "/docs")
        self.assertEqual(data.get("health"), "/health")

    def test_t1_f1_health_schema_and_operational_status(self) -> None:
        r = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("status"), "operacional")
        self.assertIs(data.get("motor_carregado"), True)
        self.assertEqual(data.get("num_clusters"), 4)

    def test_t1_f1_health_client_count_and_satisfaction_bounds(self) -> None:
        r = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertGreaterEqual(data["total_clientes_historico"], 1000)
        self.assertGreaterEqual(data["media_satisfacao_global"], 1.0)
        self.assertLessEqual(data["media_satisfacao_global"], 5.0)

    def test_t1_f1_health_silhouette_score_valid_range(self) -> None:
        r = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        score = r.json()["silhouette_score"]
        self.assertIsInstance(score, (int, float))
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_t1_f1_health_repeated_calls_consistent(self) -> None:
        r1 = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        r2 = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r1.json()["silhouette_score"], r2.json()["silhouette_score"])
        self.assertEqual(r1.json()["total_clientes_historico"], r2.json()["total_clientes_historico"])


class TestT1F2CatalogAndProducts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t1_f2_catalog_returns_exact_27_items(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        items = r.json()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 27)

    def test_t1_f2_catalog_exact_ids_prod01_to_prod27(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        ids = {item["id"] for item in r.json()}
        expected_ids = {f"PROD_{i:02d}" for i in range(1, 28)}
        self.assertEqual(ids, expected_ids)

    def test_t1_f2_catalog_required_keys_and_queixas_taxonomy(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        required = {
            "id",
            "nome",
            "marca",
            "categoria",
            "curvaturas_indicadas",
            "peso_fio",
            "afinidade_queixas",
            "descricao",
        }
        for item in r.json():
            self.assertTrue(required.issubset(item.keys()), f"Missing keys in {item.get('id')}")
            self.assertEqual(set(item["afinidade_queixas"].keys()), EXPECTED_QUEIXA_KEYS)
            for k, val in item["afinidade_queixas"].items():
                self.assertGreaterEqual(val, 0.0, f"{item['id']} {k} < 0")
                self.assertLessEqual(val, 1.0, f"{item['id']} {k} > 1")

    def test_t1_f2_catalog_contains_all_four_brands(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        brands = {item["marca"] for item in r.json()}
        self.assertEqual(brands, EXPECTED_BRANDS)

    def test_t1_f2_catalog_curvatures_and_weights_valid(self) -> None:
        r = httpx.get(f"{self.api.base_url}/catalogo", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        for item in r.json():
            curvs = item["curvaturas_indicadas"]
            self.assertTrue(len(curvs) >= 1)
            self.assertTrue(set(curvs).issubset({2, 3, 4}))
            self.assertIn(item["peso_fio"], {"leve", "medio", "pesado"})


class TestT1F3HybridRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t1_f3_recommend_ondulado_low_porosity_natural(self) -> None:
        payload = {"curvatura": 2, "porosidade": 1, "dano_quimico": 0}
        r = httpx.post(
            f"{self.api.base_url}/recommend?top_k=3",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["recomendacoes"]), 3)
        self.assertTrue(bool(data["descricao_persona"].strip()))

    def test_t1_f3_recommend_cacheado_high_porosity_chemical_acid_c_top1(self) -> None:
        payload = {
            "curvatura": 3,
            "porosidade": 3,
            "dano_quimico": 1,
            "alta_porosidade_quimica": 1,
        }
        r = httpx.post(
            f"{self.api.base_url}/recommend?top_k=3",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        recs = r.json()["recomendacoes"]
        self.assertEqual(len(recs), 3)
        self.assertIn("ACID-C", recs[0]["nome"])
        self.assertEqual(recs[0]["produto_id"], "PROD_01")

    def test_t1_f3_recommend_crespo_dryness_nutritive(self) -> None:
        payload = {
            "curvatura": 4,
            "porosidade": 3,
            "dano_quimico": 0,
            "ressecamento_opacidade": 1,
        }
        r = httpx.post(
            f"{self.api.base_url}/recommend?top_k=3",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        recs = r.json()["recomendacoes"]
        self.assertEqual(len(recs), 3)
        top_names = " ".join(item["nome"] for item in recs)
        self.assertTrue(
            any(kw in top_names for kw in ("Manteiga", "Máscara", "Heaven", "Decadence", "BE FREE")),
            f"Expected nutritive product in top-3 for dry 4C, got: {top_names}",
        )

    def test_t1_f3_recommend_top_k_variants(self) -> None:
        payload = {"curvatura": 3, "porosidade": 2, "dano_quimico": 0, "frizz_falta_definicao": 1}
        for k in (1, 3, 10, 27):
            r = httpx.post(
                f"{self.api.base_url}/recommend?top_k={k}",
                json=payload,
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 200)
            recs = r.json()["recomendacoes"]
            self.assertEqual(len(recs), k)
            ids = [x["produto_id"] for x in recs]
            self.assertEqual(len(ids), len(set(ids)), f"Duplicate produto_id for top_k={k}")

    def test_t1_f3_recommend_schema_weights_and_descending_scores(self) -> None:
        payload = {"curvatura": 3, "porosidade": 2, "dano_quimico": 1, "transicao_capilar": 1}
        r = httpx.post(
            f"{self.api.base_url}/recommend?top_k=5",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn(data["cluster_id"], {0, 1, 2, 3})
        weights = data["peso_conhecimento_vs_feedback"]
        self.assertAlmostEqual(
            weights["peso_regras_conteudo"] + weights["peso_feedback_historico"],
            1.0,
            places=3,
        )
        scores = [item["score_final"] for item in data["recomendacoes"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for item in data["recomendacoes"]:
            self.assertGreaterEqual(item["estrelas_estimadas"], 1.0)
            self.assertLessEqual(item["estrelas_estimadas"], 5.0)
            self.assertTrue(bool(item["motivo"].strip()))


class TestT1F4FeedbackLoop(unittest.TestCase):
    """Isolated `/feedback` positive tests; stops server and restores CSV SHA-256 on teardown."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.iso_env = IsolatedFeedbackApiEnv()
        cls.api = cls.iso_env.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.iso_env.stop_and_restore()

    def test_t1_f4_feedback_canonical_field_names(self) -> None:
        payload = {
            "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
            "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
            "nota_satisfacao": 5,
        }
        r = httpx.post(
            f"{self.api.base_url}/feedback",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["status"], "sucesso")
        self.assertIn("ACID-C", data["mensagem"])

    def test_t1_f4_feedback_alias_field_names(self) -> None:
        payload = {
            "perfil": {"curvatura": 2, "porosidade": 1, "dano_quimico": 0},
            "produto_nome": "Deva Curl Delight (Volume e Leveza)",
            "nota": 4,
        }
        r = httpx.post(
            f"{self.api.base_url}/feedback",
            json=payload,
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "sucesso")

    def test_t1_f4_feedback_increments_total_avaliacoes_base(self) -> None:
        payload = {
            "perfil_cliente": {"curvatura": 4, "porosidade": 3, "dano_quimico": 1},
            "nome_produto": "Curly Care Manteiga Nutritiva",
            "nota_satisfacao": 5,
        }
        r1 = httpx.post(f"{self.api.base_url}/feedback", json=payload, headers=ip_headers(), timeout=10.0)
        r2 = httpx.post(f"{self.api.base_url}/feedback", json=payload, headers=ip_headers(), timeout=10.0)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["total_avaliacoes_base"], r1.json()["total_avaliacoes_base"] + 1)

    def test_t1_f4_feedback_cluster_matches_recommend_cluster(self) -> None:
        profile = {"curvatura": 3, "porosidade": 3, "dano_quimico": 1, "alta_porosidade_quimica": 1}
        rec = httpx.post(f"{self.api.base_url}/recommend", json=profile, headers=ip_headers(), timeout=10.0)
        self.assertEqual(rec.status_code, 200)
        expected_cluster = rec.json()["cluster_id"]

        fb = httpx.post(
            f"{self.api.base_url}/feedback",
            json={
                "perfil_cliente": profile,
                "nome_produto": "Curly Care ACID-C (Acidificante Antiporosidade)",
                "nota_satisfacao": 5,
            },
            headers=ip_headers(),
            timeout=10.0,
        )
        self.assertEqual(fb.status_code, 200)
        self.assertEqual(fb.json()["cluster_afetado"], expected_cluster)

    def test_t1_f4_feedback_min_and_max_ratings_persist_to_csv(self) -> None:
        lines_before = len(CSV_PATH.read_text(encoding="utf-8").splitlines())
        for nota in (1, 5):
            r = httpx.post(
                f"{self.api.base_url}/feedback",
                json={
                    "perfil_cliente": {"curvatura": 2, "porosidade": 2, "dano_quimico": 0},
                    "nome_produto": "Arvensis Geleia Forte Fixação",
                    "nota_satisfacao": nota,
                },
                headers=ip_headers(),
                timeout=10.0,
            )
            self.assertEqual(r.status_code, 200)
            self.assertGreaterEqual(r.json()["media_global_atualizada"], 1.0)
            self.assertLessEqual(r.json()["media_global_atualizada"], 5.0)
        lines_after = len(CSV_PATH.read_text(encoding="utf-8").splitlines())
        self.assertEqual(lines_after, lines_before + 2)


class TestT1F5VisionDiagnosis(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t1_f5_vision_real_jpeg_hair_tipo3(self) -> None:
        img_bytes = load_hair_image_bytes(curvature=3, fmt="JPEG")
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("cacheado.jpg", img_bytes, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIs(data["cabelo_detectado"], True)
        self.assertEqual(data["curvatura_detectada"], 3)
        self.assertTrue(bool(data["curvatura_label"]))

    def test_t1_f5_vision_real_png_hair_format(self) -> None:
        img_bytes = load_hair_image_bytes(curvature=3, fmt="PNG")
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("cacheado.png", img_bytes, "image/png")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIs(data["cabelo_detectado"], True)
        self.assertIn(data["curvatura_detectada"], {2, 3, 4})

    def test_t1_f5_vision_real_webp_hair_format(self) -> None:
        img_bytes = load_hair_image_bytes(curvature=3, fmt="WEBP")
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("cacheado.webp", img_bytes, "image/webp")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIs(data["cabelo_detectado"], True)
        self.assertIn(data["curvatura_detectada"], {2, 3, 4})

    def test_t1_f5_vision_large_1600x1600_hair_preresize(self) -> None:
        img_bytes = load_hair_image_bytes(curvature=3, fmt="JPEG", resize_to=(1600, 1600))
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("large_hair.jpg", img_bytes, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIs(data["cabelo_detectado"], True)
        self.assertIn(data["curvatura_detectada"], {2, 3, 4})

    def test_t1_f5_vision_response_schema_and_morphology(self) -> None:
        img_bytes = load_hair_image_bytes(curvature=2, fmt="JPEG")
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("ondulado.jpg", img_bytes, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIs(data["cabelo_detectado"], True)
        self.assertGreater(data["tempo_inferencia_ms"], 0.0)
        self.assertTrue(bool(data["modelo_utilizado"]))
        self.assertIsInstance(data["detalhes_morfologicos"], dict)
        sug = data["sugestao_perfil"]
        self.assertIsInstance(sug, dict)
        self.assertIn(sug["curvatura"], {2, 3, 4})
        self.assertIn(sug["porosidade"], {1, 2, 3})
        self.assertIn(sug["frizz_falta_definicao"], {0, 1})
        self.assertIn(sug["ressecamento_opacidade"], {0, 1})


class TestT1F6SecurityCorsAndRam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()

    def test_t1_f6_owasp_security_headers_present_on_health(self) -> None:
        r = httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        self.assertEqual(r.status_code, 200)
        for hdr, expected in EXPECTED_SECURITY_HEADERS.items():
            self.assertEqual(r.headers.get(hdr), expected, f"Header mismatch for {hdr}")

    def test_t1_f6_cors_preflight_options_recommend(self) -> None:
        r = httpx.options(
            f"{self.api.base_url}/recommend",
            headers={
                "Origin": "http://127.0.0.1:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
            timeout=10.0,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers.get("access-control-allow-origin"), "*")
        allowed_methods = r.headers.get("access-control-allow-methods", "")
        for m in ("GET", "POST", "OPTIONS"):
            self.assertIn(m, allowed_methods)

    def test_t1_f6_uvicorn_startup_rss_below_512mb(self) -> None:
        stats = self.api.memory_stats_mb()
        self.assertLess(stats["rss_mb"], 512.0, f"RSS exceeded 512MB: {stats}")

    def test_t1_f6_memory_after_recommend_below_512mb(self) -> None:
        httpx.get(f"{self.api.base_url}/health", timeout=10.0)
        httpx.post(
            f"{self.api.base_url}/recommend",
            json={"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
            headers=ip_headers(),
            timeout=10.0,
        )
        stats = self.api.memory_stats_mb()
        self.assertLess(stats["rss_mb"], 512.0)
        self.assertLess(stats["peak_wset_mb"], 512.0)

    def test_t1_f6_memory_after_vision_below_512mb(self) -> None:
        img_bytes = FIXTURE_HAIR_TIPO3.read_bytes()
        r = httpx.post(
            f"{self.api.base_url}/diagnostico/imagem",
            files={"file": ("hair.jpg", img_bytes, "image/jpeg")},
            headers=ip_headers(),
            timeout=20.0,
        )
        self.assertEqual(r.status_code, 200)
        stats = self.api.memory_stats_mb()
        self.assertLess(stats["rss_mb"], 512.0)
        self.assertLess(stats["peak_wset_mb"], 512.0)


class TestT1F7FrontendTotem(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def _run_manual_totem_to_result(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.browser.click_button("Cacheado")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 2 de 4")
        self.browser.click_button("Média")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 3 de 4")
        self.browser.click_button("100% Natural")
        self.browser.click_button("Continuar →")
        self.browser.wait_for_text("Passo 4 de 4")
        self.browser.click_button("Ver minha prescrição")
        self.browser.wait_for_text("Realizar novo diagnóstico", timeout=15.0)

    def test_t1_f7_inicio_renders_hero_and_cta(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        body = self.browser.body_text()
        self.assertIn("Seu cacho tem uma história.", body)
        imgs = self.browser.verify_images_loaded("img", min_count=1)
        self.assertTrue(all(i["complete"] and i["naturalWidth"] > 0 for i in imgs), f"Broken hero img: {imgs}")
        self.assertEqual(self.browser.page_exceptions, [])
        self.assertEqual(self.browser.console_errors, [])

    def test_t1_f7_anamnese_step1_opens_on_cta(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
        self.browser.click_button("Iniciar Diagnóstico Capilar")
        self.browser.wait_for_text("Passo 1 de 4")
        self.assertIn("Qual é a sua curvatura?", self.browser.body_text())
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t1_f7_manual_anamnese_advances_to_step4(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/")
        self.browser.wait_for_text("Iniciar Diagnóstico Capilar")
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
        self.assertIn("O que mais te incomoda no dia a dia?", self.browser.body_text())
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t1_f7_processando_transitions_to_resultado(self) -> None:
        self._run_manual_totem_to_result()
        body = self.browser.body_text()
        self.assertIn("Cluster Clínico #", body)
        card_count = self.browser.eval_js("document.querySelectorAll('article').length")
        self.assertEqual(card_count, 3)
        self.assertEqual(self.browser.page_exceptions, [])
        self.assertEqual(self.browser.console_errors, [])

    def test_t1_f7_resultado_renders_xai_and_valid_images(self) -> None:
        self._run_manual_totem_to_result()
        body = self.browser.body_text()
        self.assertIn("transparência algorítmica (xai)", body.lower())
        imgs = self.browser.verify_images_loaded("article img", min_count=3)
        self.assertEqual(len(imgs), 3)
        for im in imgs:
            self.assertTrue(im["complete"] and im["naturalWidth"] > 0, f"Broken card image: {im}")
        self.assertEqual(self.browser.page_exceptions, [])


class TestT1F8FrontendAdmin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = ReadOnlySuiteEnv.api()
        cls.ui = ReadOnlySuiteEnv.ui()
        cls.browser = ReadOnlySuiteEnv.browser()

    def setUp(self) -> None:
        self.browser.reset_viewport()
        self.browser.reset_logs()

    def _open_admin_live(self) -> None:
        self.browser.navigate(f"{self.ui.base_url}/admin")
        self.browser.wait_for_text("Visão Executiva & Funil de Inteligência Capilar")
        self.browser.wait_for_text("Backend Conectado (Render)", timeout=10.0)

    def test_t1_f8_admin_header_and_live_dashboard_kpis(self) -> None:
        self._open_admin_live()
        body = self.browser.body_text()
        self.assertIn("Painel do Gestor Técnico", body)
        self.assertNotIn("Modo Resiliente", body)
        self.assertNotIn("Operação Resiliente Local", body)
        self.assertIn("27", body)
        self.assertEqual(self.browser.page_exceptions, [])
        self.assertEqual(self.browser.console_errors, [])

    def test_t1_f8_admin_switch_all_four_tabs(self) -> None:
        self._open_admin_live()
        self.browser.click_button("2. Telemetria & RNF-12")
        self.browser.wait_for_text("Telemetria Tricológica & Validação Científica (RNF-12)")
        self.browser.click_button("3. Catálogo & Fórmulas")
        self.browser.wait_for_text("Matriz Canônica de Cosméticos & Fórmulas")
        self.browser.click_button("4. Simulador Clínico (XAI)")
        self.browser.wait_for_text("Simulador & Auditoria Tricológica em Tempo Real")
        self.browser.click_button("1. Visão Geral (Dashboard)")
        self.browser.wait_for_text("Visão Executiva & Funil de Inteligência Capilar")
        self.assertEqual(self.browser.page_exceptions, [])
        self.assertEqual(self.browser.console_errors, [])

    def test_t1_f8_admin_telemetria_displays_4_personas(self) -> None:
        self._open_admin_live()
        self.browser.click_button("2. Telemetria & RNF-12")
        self.browser.wait_for_text("Clusters Clínicos de Anamnese (K-Means)")
        body = self.browser.body_text()
        for pid in range(4):
            self.assertIn(f"Persona {pid}", body)
        self.assertIn("K = 4", body)
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t1_f8_admin_catalogo_renders_all_27_product_images(self) -> None:
        self._open_admin_live()
        self.browser.click_button("3. Catálogo & Fórmulas")
        self.browser.wait_for_text("Exibindo 27 de 27 cosméticos catalogados")
        imgs = self.browser.verify_images_loaded("section img", min_count=27)
        self.assertEqual(len(imgs), 27)
        broken = [im for im in imgs if not (im["complete"] and im["naturalWidth"] > 0)]
        self.assertEqual(broken, [], f"Broken product images in CatalogoTab: {broken}")
        self.assertEqual(self.browser.page_exceptions, [])

    def test_t1_f8_admin_product_detail_modal_opens_from_dashboard(self) -> None:
        self._open_admin_live()
        self.browser.click_button("Inspecionar Ficha")
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') !== null")
        dialog_text = self.browser.eval_js("document.querySelector('[role=\"dialog\"]').innerText")
        self.assertIn("descrição oficial do salão", dialog_text.lower())
        self.assertIn("afinidade terapêutica", dialog_text.lower())
        self.browser.click_button("Fechar Detalhes")
        self.browser.wait_for("document.querySelector('[role=\"dialog\"]') === null")
        self.assertEqual(self.browser.page_exceptions, [])
