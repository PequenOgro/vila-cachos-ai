"""
scripts/keep_alive_render.py
Script utilitário para manter o backend da Vila Cachos ativo no plano gratuito do Render.
Evita o 'cold start' (atraso de ~50s decorrente da hibernação por inatividade de 15 min).

Uso:
    python scripts/keep_alive_render.py
    python scripts/keep_alive_render.py --interval 60
    python scripts/keep_alive_render.py --interval 300 --url https://vila-cachos-ai.onrender.com/
    python scripts/keep_alive_render.py --once
"""

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.request

DEFAULT_URL = "https://vila-cachos-ai.onrender.com/"
HEALTH_URL = "https://vila-cachos-ai.onrender.com/health"


def ping(url: str, timeout: int = 30) -> tuple[bool, int, float, str]:
    """
    Envia uma requisição GET HTTP leve para o endpoint especificado.
    Retorna (sucesso, status_code, tempo_ms, mensagem/resposta).
    """
    t0 = time.time()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "VilaCachos-KeepAlive/1.0 (+https://vila-cachos-ai.vercel.app)",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed_ms = (time.time() - t0) * 1000.0
            data = response.read().decode("utf-8", errors="ignore")
            return True, response.status, elapsed_ms, data
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - t0) * 1000.0
        return False, e.code, elapsed_ms, f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        elapsed_ms = (time.time() - t0) * 1000.0
        return False, 0, elapsed_ms, f"URL Error: {e.reason}"
    except Exception as e:
        elapsed_ms = (time.time() - t0) * 1000.0
        return False, 0, elapsed_ms, f"Falha: {type(e).__name__} - {str(e)}"


def formatar_tempo(segundos: float) -> str:
    m, s = divmod(int(segundos), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


def main():
    parser = argparse.ArgumentParser(
        description="Vila Cachos AI - Keep Alive Daemon para Render Free Tier"
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"URL do endpoint a receber o ping (Padrão: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Intervalo entre pings em segundos (Padrão: 60s)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Tempo limite da requisição em segundos (Padrão: 30s)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Executa apenas um ping de teste e encerra imediatamente com exit code 0",
    )
    args = parser.parse_args()

    # Assegura suporte a UTF-8 no terminal Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 76)
    print(" [*] VILA CACHOS AI - RENDER KEEP-ALIVE DAEMON")
    print("=" * 76)
    print(f" * Alvo Principal:   {args.url}")
    print(f" * Intervalo:        {args.interval} segundos")
    print(f" * Timeout:          {args.timeout} segundos")
    print(f" * Modo Unico (--once): {'SIM' if args.once else 'NAO (Loop continuo)'}")
    print("=" * 76)
    print("Pressione Ctrl+C a qualquer momento para encerrar com o relatorio.\n")

    total_pings = 0
    sucessos = 0
    falhas = 0
    tempos_ms = []
    inicio_geral = time.time()

    try:
        while True:
            total_pings += 1
            agora_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ok, status, tempo_ms, resp_texto = ping(args.url, timeout=args.timeout)

            if ok:
                sucessos += 1
                tempos_ms.append(tempo_ms)
                msg_curta = ""
                try:
                    parsed = json.loads(resp_texto)
                    msg_curta = f" | {parsed.get('status', 'ok')}"
                except Exception:
                    pass

                print(
                    f"[{agora_str}] #{total_pings:04d} -> HTTP {status} OK em {tempo_ms:6.1f} ms{msg_curta} (Ativo)",
                    flush=True,
                )
            else:
                falhas += 1
                print(
                    f"[{agora_str}] #{total_pings:04d} -> [ALERTA] HTTP {status} em {tempo_ms:6.1f} ms - {resp_texto}",
                    flush=True,
                )

            # A cada 10 pings bem-sucedidos em modo contínuo, verifica telemetria avançada
            if not args.once and total_pings % 10 == 0:
                ok_h, st_h, ms_h, txt_h = ping(HEALTH_URL, timeout=args.timeout)
                if ok_h:
                    try:
                        d = json.loads(txt_h)
                        print(
                            f"       -> [TELEMETRIA] Motor: {d.get('status')} | Clientes: {d.get('total_clientes_historico')} | Media: {d.get('media_satisfacao_global')} estrelas",
                            flush=True,
                        )
                    except Exception:
                        pass

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n[!] Interrupcao manual solicitada (Ctrl+C).")

    # Relatório Final
    duracao_total = time.time() - inicio_geral
    taxa_sucesso = (sucessos / total_pings * 100) if total_pings > 0 else 0
    tempo_medio = (sum(tempos_ms) / len(tempos_ms)) if tempos_ms else 0.0

    print("\n" + "=" * 76)
    print(" [*] RESUMO DE EXECUCAO DO KEEP-ALIVE")
    print("=" * 76)
    print(f" * Duracao Total:      {formatar_tempo(duracao_total)}")
    print(f" * Total de Pings:     {total_pings}")
    print(f" * Sucessos (HTTP 200): {sucessos} ({taxa_sucesso:.1f}%)")
    print(f" * Falhas:             {falhas}")
    print(f" * Latencia Media:     {tempo_medio:.1f} ms")
    print("=" * 76)

    sys.exit(0 if falhas == 0 else 1)


if __name__ == "__main__":
    main()
