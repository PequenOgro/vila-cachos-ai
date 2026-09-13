"""
catalog.py
Catálogo de Produtos e Matriz Terapêutica da Vila Cachos.
Define os produtos reais do salão, suas funções cosméticas e afinidades com as queixas capilares.
"""

from typing import Dict, List, Any

# Lista canônica de queixas suportadas pelo sistema (Taxonomia Inicial)
TAXONOMIA_QUEIXAS = [
    "ressecamento_opacidade",     # Exige nutrição / óleos vegetais
    "alta_porosidade_quimica",    # Exige acidificação (ACID-C) e reconstrução
    "frizz_falta_definicao",      # Exige fixação forte (geleias/gelatinas)
    "transicao_capilar",          # Exige fixação extra e texturização
    "couro_sensivel_oleoso"       # Exige higienização suave (co-wash/sem sulfato)
]

# Catálogo fundamentado nos produtos reais utilizados na Vila Cachos (Arvensis, Curly Care, Deva Curl)
CATALOGO_PRODUTOS: List[Dict[str, Any]] = [
    {
        "id": "PROD_01",
        "nome": "Curly Care ACID-C (Acidificante Antiporosidade)",
        "marca": "Curly Care",
        "categoria": "Tratamento Acidificante",
        "curvaturas_indicadas": [2, 3, 4],
        "peso_fio": "leve",  # Não pesa em nenhum tipo de cabelo
        "afinidade_queixas": {
            "ressecamento_opacidade": 0.5,
            "alta_porosidade_quimica": 1.0,  # Solução primária para cutículas abertas e dano
            "frizz_falta_definicao": 0.6,
            "transicao_capilar": 0.5,
            "couro_sensivel_oleoso": 0.2
        },
        "descricao": "Regulador de pH intensivo que sela as cutículas, combate a porosidade e devolve a elasticidade natural."
    },
    {
        "id": "PROD_02",
        "nome": "Curly Care Manteiga Nutritiva",
        "marca": "Curly Care",
        "categoria": "Máscara de Nutrição",
        "curvaturas_indicadas": [3, 4],  # Ideal para 3 e 4; pode pesar em ondulado 2 fino
        "peso_fio": "pesado",
        "afinidade_queixas": {
            "ressecamento_opacidade": 1.0,  # Solução de ouro para repor lipídios
            "alta_porosidade_quimica": 0.6,
            "frizz_falta_definicao": 0.4,
            "transicao_capilar": 0.4,
            "couro_sensivel_oleoso": 0.0
        },
        "descricao": "Rica em óleos vegetais nobres para restaurar a lubricidade e o brilho de fios ressecados."
    },
    {
        "id": "PROD_03",
        "nome": "Arvensis Geleia Forte Fixação",
        "marca": "Arvensis",
        "categoria": "Finalizador Fixação",
        "curvaturas_indicadas": [2, 3, 4],
        "peso_fio": "medio",
        "afinidade_queixas": {
            "ressecamento_opacidade": 0.2,
            "alta_porosidade_quimica": 0.3,
            "frizz_falta_definicao": 1.0,  # Solução primária para memória de cachos
            "transicao_capilar": 0.9,      # Fundamental para segurar texturas diferentes
            "couro_sensivel_oleoso": 0.1
        },
        "descricao": "Proporciona alta fixação com efeito memória, blindando o fio contra umidade e eliminando o frizz."
    },
    {
        "id": "PROD_04",
        "nome": "Arvensis Ativador de Cachos e Crespos",
        "marca": "Arvensis",
        "categoria": "Finalizador Definição",
        "curvaturas_indicadas": [3, 4],
        "peso_fio": "medio",
        "afinidade_queixas": {
            "ressecamento_opacidade": 0.7,
            "alta_porosidade_quimica": 0.4,
            "frizz_falta_definicao": 0.8,
            "transicao_capilar": 0.7,
            "couro_sensivel_oleoso": 0.1
        },
        "descricao": "Ativa a curvatura natural com hidratação equilibrada e proteção solar."
    },
    {
        "id": "PROD_05",
        "nome": "Arvensis Co-Wash Suave Cachos Naturais",
        "marca": "Arvensis",
        "categoria": "Higienizador Condicionante",
        "curvaturas_indicadas": [2, 3, 4],
        "peso_fio": "leve",
        "afinidade_queixas": {
            "ressecamento_opacidade": 0.6,
            "alta_porosidade_quimica": 0.4,
            "frizz_falta_definicao": 0.2,
            "transicao_capilar": 0.3,
            "couro_sensivel_oleoso": 1.0  # Limpeza sem agredir a barreira lipídica
        },
        "descricao": "Higienização 100% livre de sulfatos e tensoativos agressivos para couros sensíveis ou ressecados."
    },
    {
        "id": "PROD_06",
        "nome": "Deva Curl Delight (Volume e Leveza)",
        "marca": "Deva Curl",
        "categoria": "Finalizador Leve",
        "curvaturas_indicadas": [2, 3],
        "peso_fio": "leve",
        "afinidade_queixas": {
            "ressecamento_opacidade": 0.3,
            "alta_porosidade_quimica": 0.2,
            "frizz_falta_definicao": 0.6,
            "transicao_capilar": 0.3,
            "couro_sensivel_oleoso": 0.4
        },
        "descricao": "Fórmula ultraleve para onduladas e cacheadas que buscam movimento e volume sem pesar os fios."
    }
]

def obter_catalogo() -> List[Dict[str, Any]]:
    return CATALOGO_PRODUTOS

def obter_produto_por_nome(nome: str) -> Dict[str, Any]:
    for p in CATALOGO_PRODUTOS:
        if p["nome"] == nome:
            return p
    raise ValueError(f"Produto '{nome}' não encontrado no catálogo.")
