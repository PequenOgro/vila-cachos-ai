"""
recommender_engine.py
Motor de Recomendação Híbrido e Clusterização Normalizada para a Vila Cachos.

Arquitetura:
1. Normalização via StandardScaler (evita que curvatura domine variáveis binárias).
2. Segmentação de Personas via KMeans em espaço de 8 dimensões.
3. Scoring Híbrido:
   - Componente Knowledge-Based (Afinidade Terapêutica a Frio)
   - Componente Colaborativo Bayesiano (Média amortecida por feedback real do cluster)
4. Explicabilidade (XAI) do motivo de cada recomendação.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from catalog import CATALOGO_PRODUTOS, TAXONOMIA_QUEIXAS, obter_produto_por_nome

class VilaCachosRecommender:
    def __init__(self, n_clusters: int = 4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        
        # Colunas que formam o vetor de características do cliente (8 dimensões)
        self.feature_cols = [
            'curvatura',
            'porosidade',
            'dano_quimico',
            'ressecamento_opacidade',
            'alta_porosidade_quimica',
            'frizz_falta_definicao',
            'transicao_capilar',
            'couro_sensivel_oleoso'
        ]
        
        self.df_historico: pd.DataFrame = pd.DataFrame()
        self.is_fitted: bool = False
        self.persona_descriptions: Dict[int, str] = {}
        self.media_global_salao: float = 3.5
        self.confianca_bayesiana_C: float = 5.0  # Peso a priori da média global
        
    def fit(self, df_historico: pd.DataFrame) -> "VilaCachosRecommender":
        """
        Treina o scaler e o modelo de clusterização com o histórico de clientes normalizado.
        """
        self.df_historico = df_historico.copy()
        
        # 1. Normalização das 8 variáveis
        X = self.df_historico[self.feature_cols]
        X_scaled = self.scaler.fit_transform(X)
        
        # 2. Treinamento do KMeans
        self.df_historico['cluster'] = self.kmeans.fit_predict(X_scaled)
        self.is_fitted = True
        
        # 3. Calcula a média global de satisfação do salão
        if 'nota_satisfacao' in self.df_historico.columns:
            self.media_global_salao = float(self.df_historico['nota_satisfacao'].mean())
            
        # 4. Gera a interpretação semântica de cada Persona (Cluster)
        self._mapear_personas()
        
        return self

    def avaliar_qualidade_clusters(self) -> Dict[str, float]:
        """
        Calcula métricas formais de validação do agrupamento (exigência acadêmica de TCC).
        """
        if not self.is_fitted:
            raise ValueError("O modelo precisa ser treinado antes de calcular métricas.")
            
        X_scaled = self.scaler.transform(self.df_historico[self.feature_cols])
        sil_score = silhouette_score(X_scaled, self.df_historico['cluster'])
        inertia = float(self.kmeans.inertia_)
        
        return {
            "silhouette_score": round(float(sil_score), 4),
            "inercia_intra_cluster": round(inertia, 2),
            "num_clusters": self.n_clusters
        }

    def _mapear_personas(self):
        """
        Analisa os centróides no espaço original para atribuir uma descrição legível a cada Persona.
        """
        centroides_scaled = self.kmeans.cluster_centers_
        centroides_reais = self.scaler.inverse_transform(centroides_scaled)
        
        for k in range(self.n_clusters):
            row = centroides_reais[k]
            curv = row[0]
            poro = row[1]
            dano = row[2]
            
            tipo_cabelo = "Ondulado (2)" if curv < 2.6 else ("Cacheado (3)" if curv < 3.5 else "Crespo (4)")
            cond_poro = "Baixa" if poro < 1.6 else ("Média" if poro < 2.4 else "Alta")
            tem_quimica = "Com Química" if dano > 0.4 else "Sem Química"
            
            # Identifica as 2 principais queixas do cluster
            queixas_indices = [3, 4, 5, 6, 7]
            nomes_queixas = [
                "Ressecamento",
                "Alta Porosidade/Dano",
                "Frizz/Definição",
                "Transição",
                "Couro Sensível"
            ]
            valores_queixas = [(nomes_queixas[i], row[queixas_indices[i]]) for i in range(len(queixas_indices))]
            valores_queixas.sort(key=lambda x: x[1], reverse=True)
            top_queixas = f"{valores_queixas[0][0]} e {valores_queixas[1][0]}"
            
            self.persona_descriptions[k] = (
                f"Persona {k}: Foco em {tipo_cabelo}, Porosidade {cond_poro}, {tem_quimica}. "
                f"Principais dores: {top_queixas}."
            )

    def prever_cluster(self, perfil_cliente: Dict[str, Any]) -> int:
        """
        Recebe o perfil de uma cliente e retorna o ID do seu cluster (persona).
        """
        vetor = [perfil_cliente[col] for col in self.feature_cols]
        vetor_df = pd.DataFrame([vetor], columns=self.feature_cols)
        vetor_scaled = self.scaler.transform(vetor_df)
        cluster_id = int(self.kmeans.predict(vetor_scaled)[0])
        return cluster_id

    def _calcular_score_conteudo(self, perfil_cliente: Dict[str, Any], produto: Dict[str, Any]) -> Tuple[float, str]:
        """
        Camada 1: Knowledge-Based (Cold Start)
        Calcula a afinidade cosmética direta entre as dores da cliente e a fórmula do produto.
        """
        # 1. Compatibilidade de curvatura
        compativel_curvatura = perfil_cliente["curvatura"] in produto["curvaturas_indicadas"]
        fator_curvatura = 1.0 if compativel_curvatura else 0.4
        
        # Penalidade caso produto pesado em ondulado leve
        if perfil_cliente["curvatura"] == 2 and produto.get("peso_fio") == "pesado":
            fator_curvatura = 0.2
            
        # 2. Match de Queixas Ativas
        queixas_ativas = [q for q in TAXONOMIA_QUEIXAS if perfil_cliente.get(q, 0) == 1]
        if not queixas_ativas:
            score_terapeutico = 0.5
            motivo_dor = "Uso geral de manutenção"
        else:
            afinidades = [produto["afinidade_queixas"].get(q, 0.0) for q in queixas_ativas]
            score_terapeutico = float(np.mean(afinidades))
            # Pega a dor mais atendida
            melhor_idx = int(np.argmax(afinidades))
            dor_destaque = queixas_ativas[melhor_idx].replace('_', ' ').capitalize()
            motivo_dor = f"Alta eficácia contra '{dor_destaque}' ({afinidades[melhor_idx]*100:.0f}%)"
            
        score_conteudo = score_terapeutico * fator_curvatura
        return score_conteudo, motivo_dor

    def _calcular_score_bayesiano(self, cluster_id: int, nome_produto: str) -> Tuple[float, int]:
        """
        Camada 2: Collaborative Feedback
        Calcula a Média Bayesiana Amortecida (Damped Average) para o produto dentro daquele cluster.
        S_bayes = (C * m + soma_notas) / (C + n)
        """
        historico_cluster = self.df_historico[self.df_historico['cluster'] == cluster_id]
        avaliacoes_prod = historico_cluster[historico_cluster['produto_usado'] == nome_produto]['nota_satisfacao']
        
        n = len(avaliacoes_prod)
        soma_notas = float(avaliacoes_prod.sum()) if n > 0 else 0.0
        
        # Fórmula Bayesiana
        c = self.confianca_bayesiana_C
        m = self.media_global_salao
        
        media_amortecida = (c * m + soma_notas) / (c + n)
        
        # Normaliza a média de satisfação de [1, 5] para a escala [0, 1]
        score_bayesiano_norm = (media_amortecida - 1.0) / 4.0
        
        return score_bayesiano_norm, n

    def recomendar(self, perfil_cliente: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        """
        Gera a lista ordenada de recomendações híbridas com justificativa semântica.
        """
        if not self.is_fitted:
            raise ValueError("O modelo precisa ser ajustado com fit() antes de recomendar.")
            
        cluster_cliente = self.prever_cluster(perfil_cliente)
        descricao_persona = self.persona_descriptions.get(cluster_cliente, f"Cluster {cluster_cliente}")
        
        # Determina o peso adaptativo alpha entre Conteúdo e Feedback
        # Se o cluster tiver poucas avaliações, prioriza conhecimento especialista (alpha baixo)
        total_avaliacoes_cluster = len(self.df_historico[self.df_historico['cluster'] == cluster_cliente])
        alpha_feedback = min(0.60, total_avaliacoes_cluster / 100.0)
        peso_conteudo = 1.0 - alpha_feedback
        
        candidatos = []
        for produto in CATALOGO_PRODUTOS:
            nome_p = produto["nome"]
            score_conteudo, motivo_dor = self._calcular_score_conteudo(perfil_cliente, produto)
            score_bayesiano, qtd_avaliacoes = self._calcular_score_bayesiano(cluster_cliente, nome_p)
            
            # Combinação Convexa Híbrida
            score_final = (peso_conteudo * score_conteudo) + (alpha_feedback * score_bayesiano)
            
            # Converte o score final para uma estimativa amigável de estrelas (1 a 5)
            estrelas_estimadas = 1.0 + (score_final * 4.0)
            
            candidatos.append({
                "produto_id": produto["id"],
                "nome": nome_p,
                "categoria": produto["categoria"],
                "score_final": round(score_final, 3),
                "estrelas_estimadas": round(estrelas_estimadas, 2),
                "score_conteudo": round(score_conteudo, 3),
                "score_feedback_bayesiano": round(score_bayesiano, 3),
                "avaliacoes_cluster": qtd_avaliacoes,
                "motivo": motivo_dor,
                "descricao": produto["descricao"]
            })
            
        # Ordena pelo Score Final decrescente
        candidatos.sort(key=lambda x: x["score_final"], reverse=True)
        top_recomendados = candidatos[:top_k]
        
        return {
            "cluster_id": cluster_cliente,
            "descricao_persona": descricao_persona,
            "peso_conhecimento_vs_feedback": {
                "peso_regras_conteudo": round(peso_conteudo, 2),
                "peso_feedback_historico": round(alpha_feedback, 2)
            },
            "recomendacoes": top_recomendados
        }

    def registrar_feedback(self, perfil_cliente: Dict[str, Any], nome_produto: str, nota: int) -> None:
        """
        Feedback Loop: Registra a avaliação da cliente pós-atendimento e atualiza o histórico dinamicamente.
        """
        cluster_cliente = self.prever_cluster(perfil_cliente)
        novo_registro = {
            "cliente_id": f"FEEDBACK_{len(self.df_historico)+1:04d}",
            "curvatura": perfil_cliente["curvatura"],
            "porosidade": perfil_cliente["porosidade"],
            "dano_quimico": perfil_cliente["dano_quimico"],
            "ressecamento_opacidade": perfil_cliente.get("ressecamento_opacidade", 0),
            "alta_porosidade_quimica": perfil_cliente.get("alta_porosidade_quimica", 0),
            "frizz_falta_definicao": perfil_cliente.get("frizz_falta_definicao", 0),
            "transicao_capilar": perfil_cliente.get("transicao_capilar", 0),
            "couro_sensivel_oleoso": perfil_cliente.get("couro_sensivel_oleoso", 0),
            "produto_usado": nome_produto,
            "nota_satisfacao": int(nota),
            "cluster": cluster_cliente
        }
        self.df_historico = pd.concat([self.df_historico, pd.DataFrame([novo_registro])], ignore_index=True)
        # Recalcula a média global
        self.media_global_salao = float(self.df_historico['nota_satisfacao'].mean())
