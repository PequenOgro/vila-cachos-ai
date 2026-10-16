# Modelagem Arquitetural de Dados e Classes (Back-end)
**Projeto:** Web App de Diagnóstico Capilar com IA Híbrida para a Vila Cachos  
**Módulo:** Motor de Recomendação e Interface de Persistência Analítica  
**Notação:** UML (Class Diagram) e MER/ERD em Mermaid.js  

---

## 1. Diagrama de Classes (UML)

O Diagrama de Classes a seguir mapeia a estrutura estática do serviço de *back-end* desenvolvido em Python (FastAPI). Ele exibe os **Contratos de Dados** (Pydantic Schemas) para validação rigorosa das entradas e saídas da API, bem como a classe central analítica do motor híbrido (`VilaCachosRecommender`), que orquestra as bibliotecas de Machine Learning (Scikit-Learn).

```mermaid
classDiagram
    %% ==========================================
    %% SCHEMAS DE ENTRADA (Validadores Pydantic)
    %% ==========================================
    class ClienteProfile {
        <<Pydantic Schema>>
        +int curvatura
        +int porosidade
        +int dano_quimico
        +int ressecamento_opacidade
        +int alta_porosidade_quimica
        +int frizz_falta_definicao
        +int transicao_capilar
        +int couro_sensivel_oleoso
        +to_dict() Dict
    }

    class FeedbackInput {
        <<Pydantic Schema>>
        +ClienteProfile perfil_cliente
        +str nome_produto
        +int nota_satisfacao
    }

    %% ==========================================
    %% SCHEMAS DE SAÍDA (Retorno da API RESTful)
    %% ==========================================
    class RecomendacaoItem {
        <<Pydantic Schema>>
        +str produto_id
        +str nome
        +str categoria
        +float score_final
        +float estrelas_estimadas
        +float score_conteudo
        +float score_feedback_bayesiano
        +int avaliacoes_cluster
        +str motivo
    }

    class RecomendacaoResponse {
        <<Pydantic Schema>>
        +int cluster_id
        +str descricao_persona
        +Dict peso_conhecimento_vs_feedback
        +List~RecomendacaoItem~ recomendacoes
    }

    %% ==========================================
    %% NÚCLEO DO MOTOR HÍBRIDO (Regras de Negócio)
    %% ==========================================
    class VilaCachosRecommender {
        <<Service Engine>>
        -int n_clusters
        -float media_global_salao
        -float confianca_bayesiana_C
        -KMeans kmeans
        -StandardScaler scaler
        -DataFrame df_historico
        +fit(df_historico: DataFrame) self
        +prever_cluster(perfil_cliente: Dict) int
        -_calcular_score_conteudo(perfil, produto) Tuple
        -_calcular_score_bayesiano(cluster_id, nome_produto) Tuple
        +recomendar(perfil_cliente: Dict, top_k: int) Dict
        +registrar_feedback(perfil, nome_produto, nota: int) void
        +avaliar_qualidade_clusters() Dict
    }

    %% ==========================================
    %% RELACIONAMENTOS E DEPENDÊNCIAS
    %% ==========================================
    FeedbackInput *-- ClienteProfile : "Composição (Contém o Perfil)"
    RecomendacaoResponse *-- RecomendacaoItem : "Composição (Lista o Top K)"
    
    VilaCachosRecommender ..> ClienteProfile : "Recebe para Predição"
    VilaCachosRecommender ..> RecomendacaoResponse : "Produz (Instancia)"
    VilaCachosRecommender ..> FeedbackInput : "Desempacota para o Loop"
```

---

## 2. Modelo Entidade-Relacionamento (ERD / MER)

Este diagrama representa o modelo lógico relacional desenhado para suportar e persistir os atendimentos, as inferências algorítmicas e o histórico colaborativo necessário para calcular a *Média Bayesiana Amortecida* e superar progressivamente o *Cold Start*.

```mermaid
erDiagram
    %% Definição das Entidades
    CLUSTER_PERSONA {
        int id_cluster PK "Chave (Centroide 0 a 3)"
        string descricao_semantica "Ex: Cacheadas com Química"
        string perfil_dominante "Atributo predominante"
        float estabilidade_metrica "Inércia / Coesão"
    }

    CLIENTE {
        string id_atendimento PK "UUID gerado ou Hash"
        int id_cluster FK "Atribuído pelo K-Means"
        int curvatura "Escala 2, 3 ou 4"
        int porosidade "1=Baixa, 2=Média, 3=Alta"
        boolean dano_quimico "Presença de Descoloração/Alisamento"
        boolean queixas_ativas "Vetor Binário de Dores"
        timestamp data_triagem "Momento da Anamnese Web"
    }

    PRODUTO {
        string id_produto PK "Código no Catálogo (ex: PROD_01)"
        string nome_comercial "Identidade visual na prateleira"
        string marca_parceira "Arvensis, Curly Care, Deva Curl"
        string categoria_terapeutica "Acidificante, Gelatina, Máscara"
        string peso_fio "Leve, Médio, Pesado"
    }

    AVALIACAO_FEEDBACK {
        string id_feedback PK "Identificador único"
        string id_atendimento FK "Cliente que emitiu o feedback"
        string id_produto FK "Produto consumido/testado"
        int nota_satisfacao "Estrelas (1 a 5)"
        timestamp data_registro "Momento do salvamento"
    }

    %% Definição das Relações (Cardinalidades)
    CLUSTER_PERSONA ||--o{ CLIENTE : "agrupa perfis análogos"
    CLIENTE ||--|{ AVALIACAO_FEEDBACK : "submete (emite nota)"
    PRODUTO ||--o{ AVALIACAO_FEEDBACK : "recebe a avaliação"
```

---

## 3. Dicionário de Dados Resumido

A tabela abaixo especifica o papel semântico de cada uma das quatro entidades que formam a espinha dorsal de persistência do modelo híbrido de recomendação da Vila Cachos.

| Entidade | Papel no Domínio do Salão e no Motor de Recomendação |
| :--- | :--- |
| **`CLUSTER_PERSONA`** | Entidade gerenciada exclusivamente pelo algoritmo K-Means. Armazena a interpretação clínica dos $k=4$ centroides encontrados (as "Personas" do salão). Usada como pivô geográfico para calcular a média colaborativa local sem que misturemos cabelos crespos saudáveis com ondulados danificados. |
| **`CLIENTE`** | Representa a foto do estado biofísico de um atendimento pontual submetido no Web App. Armazena o vetor de 8 dimensões coletado na anamnese e a chave primária que ligará esse quadro capilar único a eventuais feedbacks posteriores. |
| **`PRODUTO`** | Repositório oficial do catálogo (A matriz *Knowledge-Based* a frio). Contém as regras duras de negócio, restrições químicas (não sugerir cremes pesados para fios finos/ondulados), categorias de ação e as *labels* das marcas homologadas pela Vila Cachos. |
| **`AVALIACAO_FEEDBACK`** | O combustível essencial do *Feedback Loop Bayesiano*. Sempre que uma cliente retorna uma nota explícita (1 a 5 estrelas), essa entidade é gravada. O motor de recomendação varre esses registros para recalibrar iterativamente os pesos do algoritmo, reduzindo aos poucos a dependência de palpites humanos iniciais e firmando o modelo estatisticamente sobre dados reais de satisfação. |
