"""
generate_dataset.py
Gerador de Dataset Sintético com Causalidade para a Vila Cachos.

Diferente de um sorteio puramente aleatório, este gerador simula relações causais reais:
1. Demografia capilar baseada na realidade de um salão de cachos.
2. Correlação entre dano químico e porosidade alta.
3. Notas de satisfação (1 a 5) decorrentes da compatibilidade cosmética/terapêutica real
   entre as dores da cliente e a formulação do produto aplicado.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from catalog import CATALOGO_PRODUTOS, TAXONOMIA_QUEIXAS

def gerar_dataset_causal(num_clientes: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    
    registros = []
    nomes_produtos = [p["nome"] for p in CATALOGO_PRODUTOS]
    
    for i in range(num_clientes):
        # 1. Demografia de Curvatura (15% Ondulado 2, 55% Cacheado 3, 30% Crespo 4)
        curvatura = int(np.random.choice([2, 3, 4], p=[0.15, 0.55, 0.30]))
        
        # 2. Histórico de Dano Químico (descoloração, alisamentos antigos, etc.)
        dano_quimico = int(np.random.choice([0, 1], p=[0.55, 0.45]))
        
        # 3. Porosidade condicionada ao dano químico
        if dano_quimico == 1:
            porosidade = int(np.random.choice([1, 2, 3], p=[0.10, 0.25, 0.65]))  # Predomínio de alta porosidade
        else:
            porosidade = int(np.random.choice([1, 2, 3], p=[0.40, 0.45, 0.15]))  # Predomínio de baixa/média
            
        # 4. Geração probabilística das queixas baseada nas características capilares
        # - Ressecamento: mais severo em crespos (tipo 4) e cabelos com dano
        prob_ressecamento = 0.85 if curvatura == 4 else (0.70 if dano_quimico == 1 else 0.40)
        queixa_ressecamento = int(np.random.rand() < prob_ressecamento)
        
        # - Alta porosidade / Fios elásticos: fortemente associada a dano químico e porosidade alta
        prob_porosidade_queixa = 0.90 if (dano_quimico == 1 and porosidade == 3) else (0.40 if porosidade == 3 else 0.10)
        queixa_porosidade = int(np.random.rand() < prob_porosidade_queixa)
        
        # - Frizz e Falta de Definição: muito comum em curvaturas 2 e 3
        prob_frizz = 0.70 if curvatura in [2, 3] else 0.55
        queixa_frizz = int(np.random.rand() < prob_frizz)
        
        # - Transição Capilar: ~20% do público do salão
        prob_transicao = 0.25 if dano_quimico == 1 else 0.10
        queixa_transicao = int(np.random.rand() < prob_transicao)
        
        # - Couro Cabeludo Oleoso / Sensível: mais frequente em curvaturas 2 e 3
        prob_couro = 0.35 if curvatura == 2 else 0.20
        queixa_couro = int(np.random.rand() < prob_couro)
        
        # Garante que a cliente tenha ao menos 1 queixa (ninguém vai ao salão sem queixas)
        if sum([queixa_ressecamento, queixa_porosidade, queixa_frizz, queixa_transicao, queixa_couro]) == 0:
            queixa_frizz = 1
            
        vetor_queixas_cliente = {
            "ressecamento_opacidade": queixa_ressecamento,
            "alta_porosidade_quimica": queixa_porosidade,
            "frizz_falta_definicao": queixa_frizz,
            "transicao_capilar": queixa_transicao,
            "couro_sensivel_oleoso": queixa_couro
        }
        
        # 5. Atribuição de Produto Histórico (Simula rotina do salão)
        # O salão acerta na maioria das vezes, mas há experimentações e recomendações imperfeitas
        produto_escolhido = np.random.choice(CATALOGO_PRODUTOS)
        
        # 6. Cálculo CAUSAL da Nota de Satisfação (Ground Truth)
        # A) Match de Curvatura e Peso
        match_curvatura = 1.0 if curvatura in produto_escolhido["curvaturas_indicadas"] else -1.0
        # Penalidade específica: manteiga pesada em cabelo ondulado tipo 2 fino
        if curvatura == 2 and produto_escolhido["peso_fio"] == "pesado":
            match_curvatura = -1.8
            
        # B) Match Terapêutico (Afinidade entre as dores ativas e a fórmula do produto)
        queixas_ativas = [k for k, v in vetor_queixas_cliente.items() if v == 1]
        afinidades_atingidas = [produto_escolhido["afinidade_queixas"][q] for q in queixas_ativas]
        score_terapeutico = np.mean(afinidades_atingidas) if afinidades_atingidas else 0.5
        
        # C) Nota Bruta Contínua (escala base de 1 a 5)
        # Se score_terapeutico for alto (ex: 1.0) e curvatura compatível -> nota ~ 4.7
        # Se score_terapeutico for baixo (ex: 0.2) -> nota ~ 2.0
        nota_esperada = 1.5 + (score_terapeutico * 2.8) + (0.4 * match_curvatura)
        
        # D) Ruído Gaussiano Natural (percepção humana de atendimento e cheiro)
        ruido = np.random.normal(loc=0.0, scale=0.35)
        nota_final = nota_esperada + ruido
        
        # E) Simulação de 5% de Outliers Humanos (ex: dia ruim do cliente ou expectativa irrealista)
        if np.random.rand() < 0.05:
            nota_final = np.random.choice([1, 2, 5])
            
        # Limita entre 1 e 5 e arredonda para número inteiro
        nota_discreta = int(np.clip(np.round(nota_final), 1, 5))
        
        registros.append({
            "cliente_id": f"CLI_{i+1:04d}",
            "curvatura": curvatura,
            "porosidade": porosidade,
            "dano_quimico": dano_quimico,
            "ressecamento_opacidade": queixa_ressecamento,
            "alta_porosidade_quimica": queixa_porosidade,
            "frizz_falta_definicao": queixa_frizz,
            "transicao_capilar": queixa_transicao,
            "couro_sensivel_oleoso": queixa_couro,
            "produto_usado": produto_escolhido["nome"],
            "score_terapeutico_real": round(float(score_terapeutico), 3),
            "nota_satisfacao": nota_discreta
        })
        
    df = pd.DataFrame(registros)
    return df

if __name__ == "__main__":
    print("=== GERANDO DATASET SINTÉTICO COM CAUSALIDADE (VILA CACHOS) ===")
    df_sintetico = gerar_dataset_causal(num_clientes=1000, seed=42)
    
    arquivo_saida = "dataset_historico_vila_cachos.csv"
    df_sintetico.to_csv(arquivo_saida, index=False, encoding="utf-8")
    
    print(f"-> Sucesso! {len(df_sintetico)} registros exportados para '{arquivo_saida}'.\n")
    print("--- AMOSTRA DOS DADOS GERADOS ---")
    print(df_sintetico[['curvatura', 'porosidade', 'dano_quimico', 'ressecamento_opacidade', 'alta_porosidade_quimica', 'produto_usado', 'nota_satisfacao']].head(5))
    
    print("\n--- ESTATÍSTICAS DE SATISFAÇÃO POR PRODUTO ---")
    resumo_satisfacao = df_sintetico.groupby('produto_usado')['nota_satisfacao'].agg(['count', 'mean', 'std']).reset_index()
    resumo_satisfacao.columns = ['Produto', 'Total Avaliações', 'Média de Satisfação', 'Desvio Padrão']
    print(resumo_satisfacao.to_string(index=False))
