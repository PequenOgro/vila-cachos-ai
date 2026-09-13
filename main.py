"""
main.py
Script de Demonstração e Validação do Motor de Recomendação da Vila Cachos.

Executa:
1. Carregamento / Treinamento com Dataset Causal Sintético
2. Exibição das Métricas Acadêmicas de Clusterização (Silhouette Score)
3. Interpretação Semântica das Personas (Clusters)
4. Simulação de 4 Cenários Clínicos no Totem do Salão
5. Demonstração Prática do Feedback Loop (Aprendizado Contínuo com Notas 1 a 5)
"""

import os
import pandas as pd
from generate_dataset import gerar_dataset_causal
from recommender_engine import VilaCachosRecommender

def main():
    print("=" * 80)
    print(" SISTEMA DE RECOMENDAÇÃO INTELIGENTE VILA CACHOS (MOTOR HÍBRIDO)")
    print(" Trabalho de Conclusão de Curso (TCC) - Sistemas de Informação")
    print("=" * 80)

    # 1. Preparação dos Dados Sintéticos com Causalidade
    csv_path = "dataset_historico_vila_cachos.csv"
    if not os.path.exists(csv_path):
        print("\n[*] Gerando base histórica causal (1000 atendimentos)...")
        df_historico = gerar_dataset_causal(num_clientes=1000, seed=42)
        df_historico.to_csv(csv_path, index=False, encoding="utf-8")
    else:
        print(f"\n[*] Carregando base histórica existente: '{csv_path}'...")
        df_historico = pd.read_csv(csv_path)

    # 2. Inicialização e Treinamento do Motor Híbrido
    print("[*] Inicializando e treinando o motor (KMeans Normalizado + StandardScaler)...")
    motor = VilaCachosRecommender(n_clusters=4, random_state=42)
    motor.fit(df_historico)

    # 3. Métricas Acadêmicas de Validação
    metricas = motor.avaliar_qualidade_clusters()
    print("\n" + "-" * 50)
    print(" MÉTRICAS DE AVALIAÇÃO DOS CLUSTERS (VALIDAÇÃO CIENTÍFICA)")
    print("-" * 50)
    print(f" - Quantidade de Clusters (Personas): {metricas['num_clusters']}")
    print(f" - Coeficiente Silhouette: {metricas['silhouette_score']:.4f}")
    print(f" - Inércia Intra-cluster: {metricas['inercia_intra_cluster']:.2f}")

    print("\n" + "-" * 50)
    print(" PERSONAS (CLUSTERS) IDENTIFICADAS NO SALÃO")
    print("-" * 50)
    for cluster_id, desc in motor.persona_descriptions.items():
        total_membros = len(motor.df_historico[motor.df_historico['cluster'] == cluster_id])
        print(f" [{total_membros:3d} clientes] {desc}")

    # 4. Simulação de Cenários no Totem
    cenarios = [
        {
            "titulo": "Cenário 1: Cliente Ondulada (2), Raiz Oleosa / Couro Sensível, Sem Química",
            "perfil": {
                "curvatura": 2, "porosidade": 1, "dano_quimico": 0,
                "ressecamento_opacidade": 0, "alta_porosidade_quimica": 0,
                "frizz_falta_definicao": 0, "transicao_capilar": 0,
                "couro_sensivel_oleoso": 1
            }
        },
        {
            "titulo": "Cenário 2: Cliente Cacheada (3), Cabelo Descolorido com Alta Porosidade e Fios Elásticos",
            "perfil": {
                "curvatura": 3, "porosidade": 3, "dano_quimico": 1,
                "ressecamento_opacidade": 0, "alta_porosidade_quimica": 1,
                "frizz_falta_definicao": 0, "transicao_capilar": 0,
                "couro_sensivel_oleoso": 0
            }
        },
        {
            "titulo": "Cenário 3: Cliente Crespa (4), Fios Muito Ressecados e Opacos (Sem química)",
            "perfil": {
                "curvatura": 4, "porosidade": 2, "dano_quimico": 0,
                "ressecamento_opacidade": 1, "alta_porosidade_quimica": 0,
                "frizz_falta_definicao": 1, "transicao_capilar": 0,
                "couro_sensivel_oleoso": 0
            }
        },
        {
            "titulo": "Cenário 4: Cliente em Transição Capilar (Duas texturas, Frizz e Química Antiga)",
            "perfil": {
                "curvatura": 3, "porosidade": 2, "dano_quimico": 1,
                "ressecamento_opacidade": 0, "alta_porosidade_quimica": 0,
                "frizz_falta_definicao": 1, "transicao_capilar": 1,
                "couro_sensivel_oleoso": 0
            }
        }
    ]

    print("\n" + "=" * 80)
    print(" SIMULAÇÃO DE ATENDIMENTO NO TOTEM DA VILA CACHOS")
    print("=" * 80)

    for c in cenarios:
        print(f"\n>> {c['titulo']}")
        resp = motor.recomendar(c['perfil'], top_k=2)
        print(f"   [Cluster Atribuído]: {resp['descricao_persona']}")
        print(f"   [Pesos Atuais]: Regras/Conteúdo={resp['peso_conhecimento_vs_feedback']['peso_regras_conteudo']*100:.0f}% | "
              f"Feedback Histórico={resp['peso_conhecimento_vs_feedback']['peso_feedback_historico']*100:.0f}%")
        
        print("   --- Recomendações Top 2 ---")
        for rank, rec in enumerate(resp['recomendacoes'], start=1):
            print(f"   #{rank}: {rec['nome']}")
            print(f"       Score Híbrido: {rec['score_final']} | Estrelas Estimadas: {rec['estrelas_estimadas']} estrelas")
            print(f"       Justificativa: {rec['motivo']}")

    # 5. Demonstração Prática do Feedback Loop
    print("\n" + "=" * 80)
    print(" DEMONSTRAÇÃO DO FEEDBACK LOOP (CALIBRAÇÃO BAYESIANA ORGÂNICA)")
    print("=" * 80)
    print("Vamos simular uma cliente do Cenário 2 (Alta Porosidade e Química) avaliando o produto recebido.")
    
    perfil_c2 = cenarios[1]["perfil"]
    rec_antes = motor.recomendar(perfil_c2, top_k=1)["recomendacoes"][0]
    print(f"\n-> Antes do novo feedback: {rec_antes['nome']} (Score: {rec_antes['score_final']}, Estrelas: {rec_antes['estrelas_estimadas']})")
    
    # Registrando avaliações excelentes na prática
    print("[+] Inserindo 5 novas avaliações de clientes reais com Nota 5 para o ACID-C...")
    for _ in range(5):
        motor.registrar_feedback(perfil_c2, "Curly Care ACID-C (Acidificante Antiporosidade)", nota=5)
        
    rec_depois = motor.recomendar(perfil_c2, top_k=1)["recomendacoes"][0]
    print(f"-> Depois do feedback loop: {rec_depois['nome']} (Score: {rec_depois['score_final']}, Estrelas: {rec_depois['estrelas_estimadas']})")
    print("-> Observe como a Média Bayesiana aumentou a confiança e o score do produto dentro do cluster de forma orgânica!")

    print("\n" + "=" * 80)
    print(" SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)

if __name__ == "__main__":
    main()
