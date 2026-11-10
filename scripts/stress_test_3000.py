"""
scripts/stress_test_3000.py
Script de Teste de Carga e Estresse Massivo (3.000 requisições concorrentes).

Executa bateria completa de testes no ecossistema Vila Cachos AI:
1. Frontend na Vercel (https://vila-cachos-ai.vercel.app/) - SSR, rotas e assets.
2. Motor de Recomendação (POST /recommend) com permutação exaustiva de perfis capilares.
3. Ciclo de Feedback (POST /feedback) com notas de 1 a 5.
4. Visão Computacional (POST /diagnostico/imagem) com simulação de fotos e morfologia.
5. Catálogo e Monitoramento (GET /catalogo, GET /health).
6. Injeção de Falhas e Casos de Borda (HTTP 422, 415, 400, 404).
"""

import asyncio
import io
import json
import os
import random
import sys
import time
from typing import Dict, Any, List
import httpx
from PIL import Image

# Força codificação UTF-8 no stdout do Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

VERCEL_BASE_URL = "https://vila-cachos-ai.vercel.app"
RENDER_BASE_URL = "https://vila-cachos-ai.onrender.com"

# Catálogo resumido de produtos válidos para testes
PRODUTOS_CATALOGO = [
    "Curly Care ACID-C (Acidificante Antiporosidade)",
    "Curly Care Marshmallow (Máscara Acidificante)",
    "Curly Care Be Strong (Máscara de Reconstrução)",
    "Curly Care Manteiga Nutritiva (Nutrição Profunda)",
    "Curly Care High Condition (Condicionador)",
    "Curly Care Pudding (Creme Definidor)",
    "Curly Care Fix U (Gelatina Modeladora)",
    "Curly Care Spume (Espuma Finalizadora)",
    "Curly Care No Spume (Higienizador sem Espuma)",
    "Curly Care Be Free (Shampoo Hidratante)",
    "Curly Care Ativador de Cachos",
    "Curly Care Mousse Modelador",
    "Arvensis Ativador de Cachos e Crespos",
    "Arvensis Geleia Alta Fixação",
    "Arvensis Cowash Hidratante",
    "Arvensis Shampoo Micelar",
    "Deva Curl No-Poo Original",
    "Deva Curl One Condition Original",
    "Deva Curl Angell Gel",
    "Deva Curl Heaven in Hair",
    "Deva Curl Styling Cream",
    "Deva Curl No-Poo Decadence",
    "Deva Curl One Condition Decadence",
    "Deva Curl Low-Poo Delight",
    "Deva Curl Low-Poo Original"
]

def gerar_imagem_sintetica_bytes(formato="JPEG", largura=64, altura=64) -> bytes:
    """Gera imagem sintética com gradiente de textura capilar simulada."""
    img = Image.new("RGB", (largura, altura), color=(
        random.randint(50, 150),
        random.randint(40, 120),
        random.randint(30, 90)
    ))
    buf = io.BytesIO()
    img.save(buf, format=formato)
    return buf.getvalue()


class StressTester:
    def __init__(self, total_requests: int = 3000, max_concurrency: int = 50):
        self.total_requests = total_requests
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.results: List[Dict[str, Any]] = []

    async def _fazer_requisicao(
        self,
        client: httpx.AsyncClient,
        req_id: int,
        categoria: str,
        metodo: str,
        url: str,
        headers: Dict[str, str] = None,
        json_data: Any = None,
        files: Any = None,
        expected_status: List[int] = None
    ) -> Dict[str, Any]:
        expected_status = expected_status or [200]
        headers = headers or {}
        t0 = time.perf_counter()
        status_code = 0
        error_msg = None

        async with self.semaphore:
            try:
                resp = await client.request(
                    metodo,
                    url,
                    headers=headers,
                    json=json_data,
                    files=files,
                    timeout=30.0
                )
                status_code = resp.status_code
                latency_ms = (time.perf_counter() - t0) * 1000
                is_success = status_code in expected_status or (status_code == 429)  # 429 = Rate Limiter funcionando
                if not is_success and status_code >= 500:
                    error_msg = f"HTTP {status_code}: {resp.text[:120]}"
            except httpx.TimeoutException:
                latency_ms = (time.perf_counter() - t0) * 1000
                status_code = 504
                error_msg = "Timeout (30s)"
                is_success = False
            except Exception as e:
                latency_ms = (time.perf_counter() - t0) * 1000
                status_code = 599
                error_msg = str(e)[:120]
                is_success = False

        res = {
            "id": req_id,
            "categoria": categoria,
            "metodo": metodo,
            "url": url,
            "status_code": status_code,
            "latency_ms": round(latency_ms, 2),
            "is_success": is_success,
            "is_rate_limited": status_code == 429,
            "error": error_msg
        }
        self.results.append(res)
        if req_id % 250 == 0 or req_id == self.total_requests:
            print(f"[{req_id}/{self.total_requests}] Concluídas | Última: {categoria} -> HTTP {status_code} ({latency_ms:.1f}ms)")
        return res

    async def run(self):
        print(f"\n{'='*70}")
        print(f"[+] INICIANDO TESTE DE ESTRESSE MASSIVO: {self.total_requests} REQUISICOES CONCORRENTES")
        print(f"Alvo Frontend Vercel: {VERCEL_BASE_URL}")
        print(f"Alvo Backend Render: {RENDER_BASE_URL}")
        print(f"{'='*70}\n")

        t_inicio = time.time()
        tasks = []

        limits = httpx.Limits(max_keepalive_connections=100, max_connections=200)
        async with httpx.AsyncClient(limits=limits) as client:
            # Distribuição balanceada das 3.000 requisições:
            # 1. 1000 requisições: Vercel Frontend (SSR, HTML, Static Assets, Cache Headers)
            # 2. 1000 requisições: Recommender Engine (/recommend & /feedback)
            # 3. 500 requisições: Visão Computacional (/diagnostico/imagem)
            # 4. 300 requisições: Catálogo e Monitoramento (/catalogo & /health)
            # 5. 200 requisições: Teste de Resiliência e Casos de Falha/Borda (422, 415, 400, 404)

            for i in range(1, self.total_requests + 1):
                mod = i % 30

                # Categoria 1: Vercel Frontend SSR & Assets (1000 reqs - ~33.3%)
                if mod < 10:
                    sub_mod = i % 3
                    if sub_mod == 0:
                        url = f"{VERCEL_BASE_URL}/"
                    elif sub_mod == 1:
                        url = f"{VERCEL_BASE_URL}/assets/styles-3Gt9rWrG.css"
                    else:
                        url = f"{VERCEL_BASE_URL}/?timestamp={i}"
                    tasks.append(
                        self._fazer_requisicao(
                            client, i, "Vercel Frontend SSR", "GET", url,
                            expected_status=[200, 304]
                        )
                    )

                # Categoria 2: Motor de Recomendação (/recommend) (750 reqs)
                elif mod < 18:
                    curv = random.choice([2, 3, 4])
                    poro = random.choice([1, 2, 3])
                    dano = random.choice([0, 1])
                    payload = {
                        "curvatura": curv,
                        "porosidade": poro,
                        "dano_quimico": dano,
                        "ressecamento_opacidade": random.choice([0, 1]),
                        "alta_porosidade_quimica": random.choice([0, 1]),
                        "frizz_falta_definicao": random.choice([0, 1]),
                        "transicao_capilar": random.choice([0, 1]),
                        "couro_sensivel_oleoso": random.choice([0, 1])
                    }
                    tasks.append(
                        self._fazer_requisicao(
                            client, i, "Recommender (/recommend)", "POST",
                            f"{RENDER_BASE_URL}/recommend?top_k=3",
                            json_data=payload,
                            expected_status=[200]
                        )
                    )

                # Categoria 3: Feedback Loop (/feedback) (250 reqs)
                elif mod < 21:
                    curv = random.choice([2, 3, 4])
                    payload = {
                        "perfil_cliente": {
                            "curvatura": curv,
                            "porosidade": random.choice([1, 2, 3]),
                            "dano_quimico": random.choice([0, 1]),
                            "ressecamento_opacidade": random.choice([0, 1]),
                            "alta_porosidade_quimica": random.choice([0, 1]),
                            "frizz_falta_definicao": random.choice([0, 1]),
                            "transicao_capilar": random.choice([0, 1]),
                            "couro_sensivel_oleoso": random.choice([0, 1])
                        },
                        "nome_produto": random.choice(PRODUTOS_CATALOGO),
                        "nota_satisfacao": random.randint(1, 5)
                    }
                    tasks.append(
                        self._fazer_requisicao(
                            client, i, "Feedback Loop (/feedback)", "POST",
                            f"{RENDER_BASE_URL}/feedback",
                            json_data=payload,
                            expected_status=[200]
                        )
                    )

                # Categoria 4: Visão Computacional (/diagnostico/imagem) (500 reqs)
                elif mod < 26:
                    fmt = random.choice(["JPEG", "PNG", "WEBP"])
                    img_bytes = gerar_imagem_sintetica_bytes(formato=fmt)
                    files = {
                        "file": (f"foto_teste_{i}.{fmt.lower()}", img_bytes, f"image/{fmt.lower()}")
                    }
                    tasks.append(
                        self._fazer_requisicao(
                            client, i, "Visão Computacional (/diagnostico/imagem)", "POST",
                            f"{RENDER_BASE_URL}/diagnostico/imagem",
                            files=files,
                            expected_status=[200]
                        )
                    )

                # Categoria 5: Catálogo & Health (300 reqs)
                elif mod < 29:
                    endpoint = "/health" if i % 2 == 0 else "/catalogo"
                    tasks.append(
                        self._fazer_requisicao(
                            client, i, f"Monitoramento ({endpoint})", "GET",
                            f"{RENDER_BASE_URL}{endpoint}",
                            expected_status=[200]
                        )
                    )

                # Categoria 6: Teste de Resiliência / Casos de Erro Injetados (200 reqs)
                else:
                    tipo_falha = i % 4
                    if tipo_falha == 0:
                        # Erro 422: Curvatura inválida (99)
                        tasks.append(
                            self._fazer_requisicao(
                                client, i, "Resiliência: Erro 422 (Curvatura Inválida)", "POST",
                                f"{RENDER_BASE_URL}/recommend",
                                json_data={"curvatura": 99, "porosidade": 2, "dano_quimico": 0},
                                expected_status=[422]
                            )
                        )
                    elif tipo_falha == 1:
                        # Erro 400: Produto desconhecido no feedback
                        tasks.append(
                            self._fazer_requisicao(
                                client, i, "Resiliência: Erro 400 (Produto Fantasma)", "POST",
                                f"{RENDER_BASE_URL}/feedback",
                                json_data={
                                    "perfil_cliente": {"curvatura": 3, "porosidade": 2, "dano_quimico": 0},
                                    "nome_produto": "Produto Inexistente XYZ 123",
                                    "nota_satisfacao": 5
                                },
                                expected_status=[400]
                            )
                        )
                    elif tipo_falha == 2:
                        # Erro 415: Formato de imagem não suportado (text/plain)
                        files = {"file": ("malicioso.txt", b"arquivo de texto nao imagem", "text/plain")}
                        tasks.append(
                            self._fazer_requisicao(
                                client, i, "Resiliência: Erro 415 (Formato Proibido)", "POST",
                                f"{RENDER_BASE_URL}/diagnostico/imagem",
                                files=files,
                                expected_status=[415]
                            )
                        )
                    else:
                        # Erro 404: Rota inexistente
                        tasks.append(
                            self._fazer_requisicao(
                                client, i, "Resiliência: Erro 404 (Rota Fantasma)", "GET",
                                f"{RENDER_BASE_URL}/api/rota-inexistente-{i}",
                                expected_status=[404]
                            )
                        )

            # Executa todas as 3.000 requisições
            await asyncio.gather(*tasks)

        t_total = time.time() - t_inicio
        self._gerar_relatorio(t_total)

    def _gerar_relatorio(self, t_total: float):
        print(f"\n{'='*70}")
        print(f"[#] RELATORIO CONSOLIDADO DO TESTE DE ESTRESSE (3.000 REQUISICOES)")
        print(f"{'='*70}")

        latencias = [r["latency_ms"] for r in self.results]
        latencias.sort()
        sucessos = sum(1 for r in self.results if r["is_success"])
        rate_limited = sum(1 for r in self.results if r["is_rate_limited"])
        erros_5xx = sum(1 for r in self.results if r["status_code"] >= 500)

        rps = self.total_requests / t_total if t_total > 0 else 0
        min_lat = latencias[0] if latencias else 0
        max_lat = latencias[-1] if latencias else 0
        avg_lat = sum(latencias) / len(latencias) if latencias else 0
        p50 = latencias[int(len(latencias) * 0.50)] if latencias else 0
        p90 = latencias[int(len(latencias) * 0.90)] if latencias else 0
        p95 = latencias[int(len(latencias) * 0.95)] if latencias else 0
        p99 = latencias[int(len(latencias) * 0.99)] if latencias else 0

        # Distribuição por Categoria
        categorias = sorted(list(set(r["categoria"] for r in self.results)))
        relatorio_categorias = {}
        for cat in categorias:
            cat_res = [r for r in self.results if r["categoria"] == cat]
            cat_lats = sorted([r["latency_ms"] for r in cat_res])
            cat_p95 = cat_lats[int(len(cat_lats) * 0.95)] if cat_lats else 0
            cat_status = {}
            for r in cat_res:
                cat_status[r["status_code"]] = cat_status.get(r["status_code"], 0) + 1
            relatorio_categorias[cat] = {
                "total": len(cat_res),
                "avg_lat_ms": round(sum(cat_lats) / len(cat_lats), 2) if cat_lats else 0,
                "p95_lat_ms": round(cat_p95, 2),
                "status_dist": cat_status
            }

        status_geral = {}
        for r in self.results:
            status_geral[r["status_code"]] = status_geral.get(r["status_code"], 0) + 1

        print(f"Tempo Total de Execução: {t_total:.2f} segundos")
        print(f"Throughput Médio: {rps:.2f} requisições/segundo")
        print(f"Total de Requisições: {self.total_requests}")
        print(f"Sucessos Operacionais: {sucessos} ({sucessos/self.total_requests*100:.1f}%)")
        print(f"Ativações de Rate Limiter (HTTP 429): {rate_limited}")
        print(f"Falhas Críticas de Servidor (HTTP 5xx): {erros_5xx}")
        print(f"\n--- Métricas de Latência (ms) ---")
        print(f"Mínima: {min_lat:.2f} ms | Média: {avg_lat:.2f} ms | Máxima: {max_lat:.2f} ms")
        print(f"P50 (Mediana): {p50:.2f} ms | P90: {p90:.2f} ms | P95: {p95:.2f} ms | P99: {p99:.2f} ms")
        print(f"\n--- Distribuição Global de Status HTTP ---")
        for sc, cnt in sorted(status_geral.items()):
            desc = "OK" if sc == 200 else ("Rate Limit (SlowAPI)" if sc == 429 else ("Validação/Falha Esperada" if sc in [400, 415, 422, 404] else "Erro"))
            print(f"  HTTP {sc}: {cnt} requisições ({desc})")

        print(f"\n--- Detalhamento por Categoria ---")
        for cat, dados in relatorio_categorias.items():
            print(f"* {cat}: {dados['total']} reqs | Latência Média: {dados['avg_lat_ms']}ms | P95: {dados['p95_lat_ms']}ms | Status: {dados['status_dist']}")

        # Salva o arquivo de resultados completo
        dados_finais = {
            "total_requests": self.total_requests,
            "tempo_total_segundos": round(t_total, 2),
            "throughput_rps": round(rps, 2),
            "sucessos": sucessos,
            "rate_limited": rate_limited,
            "erros_5xx": erros_5xx,
            "latencia_ms": {
                "min": min_lat,
                "media": round(avg_lat, 2),
                "p50": p50,
                "p90": p90,
                "p95": p95,
                "p99": p99,
                "max": max_lat
            },
            "status_distribuicao": status_geral,
            "categorias": relatorio_categorias
        }

        os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "performance"), exist_ok=True)
        out_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "performance", "stress_test_3000_results.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Resultados salvos com sucesso em: {out_json}")


if __name__ == "__main__":
    total = 3000
    tester = StressTester(total_requests=total, max_concurrency=40)
    asyncio.run(tester.run())
