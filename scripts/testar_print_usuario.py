import requests
import pandas as pd
from recommender_engine import VilaCachosRecommender

def main():
    print("=================================================================")
    print("[*] PROCESSANDO O PRINT DO INSTAGRAM DA VILA CACHOS NA GPU")
    print("=================================================================")

    # 1. Envio do recorte do print para a GPU no Google Colab
    colab_url = "https://gossip-aberdeen-memories-hint.trycloudflare.com/diagnostico/imagem"
    with open("print_depois_cabelo.jpg", "rb") as f:
        resp = requests.post(colab_url, files={"file": ("cabelo.jpg", f, "image/jpeg")}, timeout=10)
    
    if resp.status_code != 200:
        print("[!] Erro na chamada:", resp.status_code, resp.text)
        return
        
    diag = resp.json()

    print("\n--- 1. DIAGNÓSTICO DE VISÃO COMPUTACIONAL (YOLOv8 + OpenCV na GPU T4) ---")
    print(f"[*] Curvatura Capilar Detectada: {diag['curvatura_label']}")
    print(f"[*] Grau de Certeza do Modelo:  {diag['confianca_curvatura']*100:.1f}%")
    print(f"[*] Frizz / Dispersão de Fios:   {'Frizz Presente' if diag['frizz_detectado'] == 1 else 'Alinhado'}")
    print(f"[*] Porosidade Aparente:        Nível {diag['porosidade_aparente']} (Média/Equilibrada)")
    print(f"[*] Desvio Padrão Morfológico:  {diag['detalhes_morfologicos']['desvio_padrao']}")
    print(f"[*] Tempo de Inferência na GPU:  {diag['tempo_inferencia_ms']} ms")

    # 2. Atribuição ao Perfil do Totem e Motor Híbrido
    perfil = dict(diag["sugestao_perfil"])
    perfil.update({
        "dano_quimico": 0,
        "alta_porosidade_quimica": 0,
        "transicao_capilar": 0,
        "couro_sensivel_oleoso": 0
    })

    df = pd.read_csv("dataset_historico_vila_cachos.csv")
    recommender = VilaCachosRecommender().fit(df)
    rec = recommender.recomendar(perfil, top_k=3)

    print("\n--- 2. PRESCRIÇÃO COSMÉTICA PERSONALIZADA (TOTEM VILA CACHOS) ---")
    print(f"[*] Persona / Cluster Atribuído: {rec['descricao_persona']}")
    print(f"[*] Equilíbrio do Score: {rec['peso_conhecimento_vs_feedback']['peso_regras_conteudo']*100:.0f}% Regras Tricológicas + {rec['peso_conhecimento_vs_feedback']['peso_feedback_historico']*100:.0f}% Avaliações de Clientes Reais")
    print("\nPRODUTOS DO SALAO RECOMENDADOS:")
    for i, p in enumerate(rec["recomendacoes"], 1):
        print(f"\n  #{i} -> {p['nome']}")
        print(f"       Score: {p['score_final']} | Avaliacao Media Estimada: {p['estrelas_estimadas']} estrelas")
        print(f"       Justificativa Tricologica: {p['motivo']}")

    print("\n=================================================================")
    print("[+] DEMONSTRACAO DO FLUXO COMPLETO EXECUTADA COM SUCESSO!")
    print("=================================================================")

if __name__ == "__main__":
    main()
