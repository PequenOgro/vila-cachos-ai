import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# 1. Gerando o Dataset Mockado (Histórico do Salão)
np.random.seed(42)
num_clientes = 500

produtos_catalogo = [
    "Deva Curl Delight (Volume)", 
    "Curly Care ACID-C (Antiporosidade)", 
    "Arvensis Geleia Forte (Fixação)", 
    "Curly Care Manteiga Nutritiva"
]

dados = {
    'curvatura': np.random.choice([2, 3, 4], num_clientes), # 2=Ondulado, 3=Cacheado, 4=Crespo
    'porosidade': np.random.choice([1, 2, 3], num_clientes), # 1=Baixa, 2=Média, 3=Alta
    'dano_quimico': np.random.choice([0, 1], num_clientes), # 0=Não, 1=Sim
    'produto_usado': np.random.choice(produtos_catalogo, num_clientes),
    'nota_satisfacao': np.random.randint(1, 6, num_clientes) # Notas de 1 a 5
}

df_historico = pd.DataFrame(dados)

# 2. Treinando o modelo para agrupar perfis semelhantes (Clusterização)
X = df_historico[['curvatura', 'porosidade', 'dano_quimico']]
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_historico['cluster'] = kmeans.fit_predict(X)

# 3. Função de Recomendação para uma Nova Cliente no Totem
def recomendar_produto(nova_curvatura, nova_porosidade, novo_dano):
    # Encontra a qual cluster a nova cliente pertence
    novo_perfil = pd.DataFrame([[nova_curvatura, nova_porosidade, novo_dano]], 
                               columns=['curvatura', 'porosidade', 'dano_quimico'])
    cluster_cliente = kmeans.predict(novo_perfil)[0]
    
    # Filtra o histórico apenas para clientes do mesmo cluster (mesma "persona")
    clientes_similares = df_historico[df_historico['cluster'] == cluster_cliente]
    
    # Encontra o produto com a maior média de satisfação neste grupo
    melhor_produto = clientes_similares.groupby('produto_usado')['nota_satisfacao'].mean().idxmax()
    media_nota = clientes_similares.groupby('produto_usado')['nota_satisfacao'].mean().max()
    
    return melhor_produto, media_nota, cluster_cliente

# 4. Simulando o uso no Totem da Vila Cachos
cenarios = [
    {"nome": "Cenário 1: Cabelo Ondulado (2), Porosidade Baixa (1), Natural (0)", "c": 2, "p": 1, "d": 0},
    {"nome": "Cenário 2: Cabelo Cacheado (3), Porosidade Média (2), Com Química (1)", "c": 3, "p": 2, "d": 1},
    {"nome": "Cenário 3: Cabelo Crespo (4), Porosidade Alta (3), Com Química (1)", "c": 4, "p": 3, "d": 1},
    {"nome": "Cenário 4: Cabelo Crespo (4), Porosidade Baixa (1), Natural (0)", "c": 4, "p": 1, "d": 0},
]

print("=== INICIANDO SIMULAÇÃO DE RECOMENDAÇÃO (TOTEM VILA CACHOS) ===\n")
for cen in cenarios:
    print(f">> {cen['nome']}")
    produto, confianca, cluster = recomendar_produto(cen['c'], cen['p'], cen['d'])
    print(f"   - Cluster ID: {cluster}")
    print(f"   - Produto Recomendado: {produto}")
    print(f"   - Confiança (Média de Satisfação): {confianca:.2f} estrelas\n")
