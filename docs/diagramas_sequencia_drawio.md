# Diagramas de Sequência do Sistema Vila Cachos AI

Este documento contém os **Diagramas de Sequência UML em Mermaid.js** modelados especificamente para atender à documentação da disciplina de **Análise 2**. Cada diagrama foi projetado para modelar com fidelidade os fluxos principais, fluxos alternativos, regras de negócio (RN) e requisitos funcionais (RF/RNF) do projeto, além de ser **100% compatível com importação direta no draw.io** (`Arrange/Insert > Advanced > Mermaid`).

---

## 📋 Tabela de Correlação dos Diagramas

| Diagrama | Caso de Uso | Atores Envolvidos | Requisitos Funcionais | Regras de Negócio |
| :--- | :--- | :--- | :--- | :--- |
| **Diagrama 1** | **UC-02**: Preencher anamnese capilar | Cliente do salão / Profissional | RF-01, RF-02, RF-03, RF-19, RF-21 | RN-01, RN-02, RN-03, RN-04, RN-05 |
| **Diagrama 2** | **UC-03**: Gerar recomendação híbrida | Cliente do salão / Profissional | RF-04 a RF-11, RF-22 | RN-01 a RN-12, RN-14 |
| **Diagrama 3** | **UC-04**: Visualizar diagnóstico e recomendações | Cliente do salão / Profissional | RF-10, RF-11, RF-12, RF-19 | RN-11, RN-12, RN-14 |
| **Diagrama 4** | **UC-05**: Registrar feedback de produto | Cliente do salão | RF-13 a RF-16, RF-22 | RN-13, RN-15, RNF-03 |
| **Diagrama 5** | **UC-06**: Consultar catálogo | Gestor / responsável técnico | RF-17, RNF-11 | RN-06, RN-07 |
| **Diagrama 6** | **UC-07**: Monitorar saúde e métricas | Gestor / responsável técnico | RF-18, RNF-08, RNF-12 | RN-09, RNF-08 |

---

## 🛠️ Como Importar no draw.io
1. Abra o [draw.io](https://app.diagrams.net/).
2. No menu superior, clique em **+ (Insert)** ou **Arrange** -> **Insert** -> **Advanced** -> **Mermaid**.
3. Copie o bloco de código Mermaid de um dos diagramas abaixo e cole na caixa de texto.
4. Clique em **Insert**. O draw.io converterá automaticamente o código em formas nativas e editáveis.

---

## 1. Diagrama de Sequência: UC-02 - Preencher Anamnese Capilar

### Escopo e Detalhes
* **Caso de Uso:** UC-02 - Preencher anamnese capilar
* **Objetivo:** Coletar, de forma guiada em 4 etapas, as características necessárias para formar o perfil capilar de 8 variáveis.
* **Atores e Participantes:**
  * `Cliente do salão` (ou Profissional do salão)
  * `Interface Web` (Totem UI / Wizard em React)
* **Fluxos Modelados:**
  * Fluxo Principal: 4 passos sequenciais (Curvatura 2/3/4, Porosidade 1/2/3, Dano Químico 0/1 e 5 Queixas).
  * Fluxo Alternativo A1: Voltar etapa sem perda de seleções.
  * Fluxo Alternativo A2: Cancelar e retornar à tela inicial.
  * Fluxo Alternativo A3: Nenhuma queixa selecionada (aplica regra RN-04 / RN-05 de manutenção geral).
  * Exceção E1 (RNF-06): Timeout de inatividade de 15 minutos limpando o estado da sessão.

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente do salão
    participant UI as Interface Web

    Note over C, UI: Início da Jornada no Totem / Web App
    C->>UI: Clica em "Iniciar Diagnóstico"
    activate UI
    UI->>UI: Inicializa estado temporário da anamnese
    UI-->>C: Exibe Etapa 1: Seleção de Curvatura (2 - Ondulado, 3 - Cacheado, 4 - Crespo)
    deactivate UI

    C->>UI: Seleciona curvatura (ex: 3)
    activate UI
    UI->>UI: Salva curvatura no estado local
    UI-->>C: Exibe Etapa 2: Nível de Porosidade (1 - Baixa, 2 - Média, 3 - Alta)
    deactivate UI

    opt Fluxo Alternativo A1: Voltar etapa anterior
        C->>UI: Clica no botão "Voltar"
        activate UI
        UI-->>C: Apresenta Etapa 1 com a opção anterior preservada
        C->>UI: Altera opção e avança novamente
        deactivate UI
    end

    C->>UI: Seleciona porosidade (ex: 3)
    activate UI
    UI->>UI: Salva porosidade no estado local
    UI-->>C: Exibe Etapa 3: Histórico de Dano Químico (0 - Não, 1 - Sim)
    deactivate UI

    C->>UI: Informa presença de dano químico (ex: 1)
    activate UI
    UI->>UI: Salva flag de dano químico
    UI-->>C: Exibe Etapa 4: Seleção das 5 Queixas Capilares Ativas
    deactivate UI

    alt Fluxo Alternativo A3: Nenhuma queixa selecionada (RN-04 / RN-05)
        C->>UI: Deixa as 5 queixas desmarcadas e prossegue
        activate UI
        UI->>UI: Define flags zeradas (Motor aplicara score 0.5 e Manutencao Geral)
        deactivate UI
    else Cliente seleciona uma ou mais queixas
        C->>UI: Marca queixas (ex: alta porosidade quimica e frizz)
        activate UI
        UI->>UI: Atualiza vetor com queixas ativas = 1
        deactivate UI
    end

    opt Excecao E1: Inatividade de 15 minutos (RNF-06)
        Note over UI: Timer de 15 minutos sem interacao expira
        UI->>UI: Limpa estado local da sessao por seguranca
        UI-->>C: Redireciona para tela inicial de acolhimento
    end

    opt Fluxo Alternativo A2: Cancelamento voluntario
        C->>UI: Clica em "Cancelar / Reiniciar"
        activate UI
        UI->>UI: Limpa formulario e descarta dados
        UI-->>C: Retorna a tela inicial
        deactivate UI
    end

    C->>UI: Clica em "Gerar Recomendacao"
    activate UI
    UI->>UI: Consolida payload ClienteProfile com as 8 variaveis
    Note over UI: Inicia execucao do UC-03 (POST /recommend)
    deactivate UI
```

---

## 2. Diagrama de Sequência: UC-03 - Gerar Recomendação Híbrida

### Escopo e Detalhes
* **Caso de Uso:** UC-03 - Gerar recomendação híbrida
* **Objetivo:** Classificar o perfil biofísico capilar com K-Means e gerar ranking personalizado Top-3 combinando afinidade de conteúdo e média bayesiana amortecida.
* **Participantes:**
  * `Interface Web` (Client HTTP)
  * `RecommenderAPI` (FastAPI / Rotas)
  * `VilaCachosRecommender` (Motor de IA e Regras)
  * `ProdutoCatalogo` (Matriz Terapêutica)
  * `RegistroHistorico` (DataFrame / CSV)
* **Regras de Negócio e Fórmulas:**
  * Validação Pydantic (RN-01 a RN-03).
  * Normalização via StandardScaler e predição de cluster (4 personas).
  * Peso adaptativo: $\alpha_{feedback} = \min(0.60, N_{cluster}/100)$ e $peso_{conteudo} = 1.0 - \alpha_{feedback}$.
  * Afinidade de conteúdo (fator de curvatura 1.0 / 0.4 / 0.2 e queixas ativas).
  * Média Bayesiana amortecida: $S = \frac{C \cdot m + \sum notas}{C + n}$ com $C=5$ e $m=\text{média global}$.
  * Estimativa de estrelas: $1 + 4 \cdot score\_final$.
  * Tratamento de exceções HTTP 422, 429 e 503.

```mermaid
sequenceDiagram
    autonumber
    participant UI as Interface Web
    participant API as RecommenderAPI
    participant Motor as VilaCachosRecommender
    participant Catalogo as ProdutoCatalogo
    participant Historico as RegistroHistorico

    UI->>API: POST /recommend?top_k=3 (Payload: ClienteProfile)
    activate API

    alt Excecao E2: Limite de taxa excedido (RNF-03)
        API-->>UI: HTTP 429 Too Many Requests (Limite de 10 req/min)
    else Excecao E1: Perfil capilar invalido (RF-04 / RN-01 a RN-03)
        API-->>UI: HTTP 422 Unprocessable Entity (Validacao Pydantic)
    else Excecao E3: Motor indisponivel / nao treinado (RF-22 / RNF-08)
        API-->>UI: HTTP 503 Service Unavailable (is_fitted == False)
    else Fluxo Principal: Processamento da Recomendacao Hibrida
        API->>Motor: recomendar(perfil_cliente, top_k=3)
        activate Motor

        Note over Motor: 1. Normalizacao e Predicao do Cluster (Persona)
        Motor->>Motor: scaler.transform(vetor_8_variaveis)
        Motor->>Motor: cluster_id = kmeans.predict(vetor_scaled)
        Motor->>Motor: Recupera descricao_persona correspondente

        Note over Motor: 2. Calculo dos Pesos Adaptativos (RN-10)
        Motor->>Historico: Consulta quantidade de registros do cluster
        Historico-->>Motor: total_avaliacoes_cluster
        Motor->>Motor: alpha_feedback = min(0.60, total_avaliacoes_cluster / 100)
        Motor->>Motor: peso_conteudo = 1.0 - alpha_feedback

        Note over Motor, Catalogo: 3. Scoring Hibrido para cada Produto do Catalogo
        loop Para cada produto no catalogo
            Motor->>Catalogo: Obter regras terapeuticas e curvaturas indicadas
            Catalogo-->>Motor: Dados do produto

            Note over Motor: Score de Conteudo (Knowledge-Based / RN-06 a RN-08)
            Motor->>Motor: Calcula fator_curvatura (1.0 normal, 0.4 incompativel, 0.2 pesado em tipo 2)
            Motor->>Motor: Calcula score_terapeutico (media das queixas ou 0.5 se vazio)
            Motor->>Motor: score_conteudo = score_terapeutico * fator_curvatura

            Note over Motor, Historico: Score Colaborativo Bayesiano (RN-09)
            Motor->>Historico: Filtrar notas do produto no cluster_id
            Historico-->>Motor: n avaliacoes e soma das notas
            Motor->>Motor: media_amortecida = (5 * media_global + soma_notas) / (5 + n)
            Motor->>Motor: score_bayesiano = (media_amortecida - 1.0) / 4.0

            Note over Motor: Combinacao Convexa e Estrelas (RN-11 / RN-12)
            Motor->>Motor: score_final = (peso_conteudo * score_conteudo) + (alpha_feedback * score_bayesiano)
            Motor->>Motor: estrelas_estimadas = 1.0 + (score_final * 4.0)
            Motor->>Motor: Gera justificativa explicavel (XAI) do produto
        end

        Motor->>Motor: Ordena candidatos por score_final decrescente
        Motor->>Motor: Seleciona os 3 primeiros colocados (Top K = 3)
        Motor-->>API: Retorna cluster_id, descricao_persona, pesos e Top 3 produtos
        deactivate Motor

        API-->>UI: HTTP 200 OK (RecomendacaoResponse)
    end
    deactivate API
```

---

## 3. Diagrama de Sequência: UC-04 - Visualizar Diagnóstico e Recomendações

### Escopo e Detalhes
* **Caso de Uso:** UC-04 - Visualizar diagnóstico e recomendações
* **Objetivo:** Apresentar o resultado em formato compreensível para apoiar a decisão de compra ou tratamento, exibindo a persona, proporção de pesos, Top 3 ranqueado com estrelas estimadas e justificativas.
* **Atores e Participantes:**
  * `Cliente do salão` (ou Profissional do salão)
  * `Interface Web` (Totem UI em React)
  * `RecommenderAPI` (Provedor de Dados)
* **Regras de Negócio e Funcionalidades:**
  * Exibição de persona identificada e peso adaptativo (regras vs feedback).
  * Destaque visual de 1º lugar (Melhor recomendação).
  * Tratamento de resposta incompleta (Exceção E1).
  * Pontos de extensão: Iniciar novo diagnóstico (RF-19) ou Avaliar produto (UC-05).

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente do salão
    participant UI as Interface Web
    participant API as RecommenderAPI

    Note over UI, API: Retorno do calculo de recomendacao (UC-03)
    API-->>UI: Retorna payload RecomendacaoResponse (HTTP 200)
    activate UI

    alt Excecao E1: Resposta incompleta ou erro de rede
        UI->>UI: Identifica dados ausentes ou falha HTTP
        UI-->>C: Exibe mensagem amigavel orientando refazer a anamnese
    else Fluxo Principal: Apresentacao Completa dos Resultados
        UI->>UI: Renderiza badge da Persona (cluster_id e descricao_persona)
        UI->>UI: Renderiza barra de calibracao de pesos (Conteudo % vs Historico %)
        
        Note over UI: Renderizacao do Top 3 Cosméticos
        UI->>UI: Aplica destaque visual no 1o item (Produto Campeao / Match Principal)
        UI->>UI: Exibe para cada item: nome, marca, categoria e estrelas estimadas
        UI->>UI: Exibe texto de justificativa clinica explicavel (XAI - Motivo)
        UI->>UI: Renderiza botoes de acao (Avaliar Produto / Novo Diagnostico)

        UI-->>C: Apresenta tela de resultados finalizada
        deactivate UI

        opt Acao 1: Reiniciar diagnostico (RF-19)
            C->>UI: Clica em "Novo Diagnostico"
            activate UI
            UI->>UI: Limpa estado e variaveis em memoria
            UI-->>C: Redireciona para tela inicial de acolhimento
            deactivate UI
        end

        opt Acao 2: Avaliar produto (Extensao para UC-05)
            C->>UI: Clica em "Avaliar" em um dos produtos do Top 3
            activate UI
            UI-->>C: Abre modal interativo de avaliacao (estrelas de 1 a 5)
            deactivate UI
        end
    end
```

---

## 4. Diagrama de Sequência: UC-05 - Registrar Feedback de Produto

### Escopo e Detalhes
* **Caso de Uso:** UC-05 - Registrar feedback de produto
* **Objetivo:** Registrar a satisfação observada pós-atendimento (nota de 1 a 5 estrelas) e alimentar a base histórica para recalibrar futuras recomendações bayesianas.
* **Participantes:**
  * `Cliente do salão`
  * `Interface Web`
  * `RecommenderAPI`
  * `VilaCachosRecommender`
  * `ProdutoCatalogo`
  * `RegistroHistorico` (DataFrame / CSV)
* **Regras de Negócio e Validações:**
  * Nota inteira de 1 a 5 (RN-13 / HTTP 422 se inválida).
  * Produto obrigatoriamente pertencente ao catálogo oficial (RF-14 / HTTP 400 se desconhecido).
  * Re-predição do cluster do perfil avaliado para correta amarração do feedback (RF-15).
  * Atualização da média global de satisfação do salão e persistência imediata em CSV (RF-16).
  * Rate limit de proteção contra spam (RNF-03 / HTTP 429).

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente do salão
    participant UI as Interface Web
    participant API as RecommenderAPI
    participant Motor as VilaCachosRecommender
    participant Catalogo as ProdutoCatalogo
    participant Historico as RegistroHistorico

    C->>UI: Seleciona nota de 1 a 5 estrelas e confirma envio
    activate UI
    UI->>API: POST /feedback (Payload: FeedbackInput)
    activate API

    alt Excecao E3: Limite de requisicoes excedido (RNF-03)
        API-->>UI: HTTP 429 Too Many Requests
        UI-->>C: Alerta sobre limite de envios atingido
    else Excecao E1: Nota fora do intervalo 1 a 5 (RF-13 / RN-13)
        API-->>UI: HTTP 422 Unprocessable Entity
        UI-->>C: Alerta que a nota informada e invalida
    else Validacao de Integridade do Catalogo Oficial (RF-14)
        API->>Catalogo: Verifica se nome_produto existe no CATALOGO_PRODUTOS
        Catalogo-->>API: Retorna resultado da busca

        alt Excecao E2: Produto nao cadastrado no catalogo
            API-->>UI: HTTP 400 Bad Request ("Produto nao encontrado no catalogo")
            UI-->>C: Exibe erro informando incompatibilidade de catalogo
        else Fluxo Principal: Produto Valido e Processamento de Feedback
            API->>Motor: registrar_feedback(dados_cliente, nome_produto, nota)
            activate Motor

            Note over Motor: 1. Identificacao do Cluster da Avaliacao (RF-15)
            Motor->>Motor: cluster_id = prever_cluster(dados_cliente)

            Note over Motor: 2. Anexacao do Novo Registro no Historico
            Motor->>Historico: Concatena novo RegistroHistorico (cliente_id, variaveis, nota, cluster)
            Historico-->>Motor: DataFrame atualizado com sucesso

            Note over Motor: 3. Recalculo da Media Global do Salao
            Motor->>Historico: Recalcula media_global_salao = df_historico['nota_satisfacao'].mean()
            Historico-->>Motor: Nova media_global calculada

            Motor-->>API: Feedback registrado com sucesso
            deactivate Motor

            Note over API, Historico: 4. Persistencia Imediata em Disco (RF-16)
            API->>Historico: Salva DataFrame no arquivo CSV (dataset_historico_vila_cachos.csv)
            Historico-->>API: Gravacao confirmada com sucesso

            API->>Motor: prever_cluster(dados_cliente)
            Motor-->>API: Retorna cluster_afetado

            API-->>UI: HTTP 200 OK (FeedbackResponse: status="sucesso", cluster_afetado, media_atualizada)
            deactivate API

            UI->>UI: Substitui componentes de avaliacao por mensagem de sucesso
            UI-->>C: Exibe confirmacao e agradecimento pelo feedback
            deactivate UI
        end
    end
```

---

## 5. Diagrama de Sequência: UC-06 - Consultar Catálogo

### Escopo e Detalhes
* **Caso de Uso:** UC-06 - Consultar catálogo
* **Objetivo:** Obter a lista oficial de produtos, categorias, curvaturas indicadas, pesos de formulação e matriz de afinidades terapêuticas com as queixas capilares.
* **Atores e Participantes:**
  * `Gestor / responsável técnico`
  * `Interface Web` (ou Cliente Técnico / Postman)
  * `RecommenderAPI`
  * `ProdutoCatalogo`
* **Requisitos Relacionados:**
  * RF-17: Disponibilização do catálogo oficial via API.
  * RNF-11: Manutenibilidade e separação estrita de catálogo.

```mermaid
sequenceDiagram
    autonumber
    actor G as Gestor / responsável técnico
    participant UI as Interface Web
    participant API as RecommenderAPI
    participant Catalogo as ProdutoCatalogo

    G->>UI: Acessa rota de consulta de produtos cadastrados
    activate UI
    UI->>API: GET /catalogo
    activate API

    Note over API, Catalogo: Leitura da Matriz Oficial de Cosmeticos
    API->>Catalogo: Obter lista completa CATALOGO_PRODUTOS
    activate Catalogo
    Catalogo-->>API: Retorna lista de entidades ProdutoCatalogo
    deactivate Catalogo

    Note over API: Serializacao dos atributos (id, nome, marca, afinidades, curvaturas)
    API-->>UI: HTTP 200 OK (Array de produtos com regras terapeuticas)
    deactivate API

    UI->>UI: Formata catalogo em tabela / cards com especificacoes tecnicas
    UI-->>G: Exibe produtos oficiais e regras terapeuticas cadastradas
    deactivate UI
```

---

## 6. Diagrama de Sequência: UC-07 - Monitorar Saúde e Métricas

### Escopo e Detalhes
* **Caso de Uso:** UC-07 - Monitorar saúde e métricas
* **Objetivo:** Verificar se o motor de IA está operacional (`is_fitted`) e inspecionar em tempo real o volume de atendimentos históricos, média global de satisfação e qualidade científica da clusterização (Silhouette Score e Inércia).
* **Atores e Participantes:**
  * `Gestor / responsável técnico`
  * `Interface Web` (Dashboard de Telemetria / Swagger)
  * `RecommenderAPI`
  * `VilaCachosRecommender`
  * `RegistroHistorico` (DataFrame)
* **Requisitos Relacionados:**
  * RF-18: Endpoint `/health` com estado do motor e métricas.
  * RNF-08: Rota de monitoramento independente da inferência.
  * RNF-12: Qualidade científica com validação por Silhouette Score.

```mermaid
sequenceDiagram
    autonumber
    actor G as Gestor / responsável técnico
    participant UI as Interface Web
    participant API as RecommenderAPI
    participant Motor as VilaCachosRecommender
    participant Historico as RegistroHistorico

    G->>UI: Acessa dashboard de status ou rota de monitoramento
    activate UI
    UI->>API: GET /health
    activate API

    Note over API, Motor: Verificacao do Estado Operacional
    API->>Motor: Avalia se motor carregado e treinado (motor.is_fitted)

    alt Excecao E1: Motor indisponivel ou nao ajustado (RNF-08)
        API-->>UI: HTTP 503 Service Unavailable ("Motor de recomendacao nao carregado")
        UI-->>G: Exibe alerta critico de indisponibilidade do motor
    else Fluxo Principal: Telemetria e Metricas Academicas
        API->>Historico: Obter len(df_historico) e media_global_salao
        Historico-->>API: total_clientes_historico e media_satisfacao_global

        Note over API, Motor: Calculo Cientifico da Qualidade dos Clusters (RNF-12)
        API->>Motor: avaliar_qualidade_clusters()
        activate Motor
        Motor->>Motor: scaler.transform(df_historico[feature_cols])
        Motor->>Motor: silhouette_score(X_scaled, clusters)
        Motor->>Motor: Extrai inercia_intra_cluster (kmeans.inertia_)
        Motor-->>API: Retorna metricas (silhouette_score, inercia, num_clusters=4)
        deactivate Motor

        Note over API: Montagem do payload HealthResponse
        API-->>UI: HTTP 200 OK (status="operacional", motor_carregado=True, total_clientes, media_satisfacao, num_clusters, silhouette_score)
        deactivate API

        UI->>UI: Renderiza painel com indicadores de saude e score Silhouette
        UI-->>G: Apresenta metricas em tempo real do sistema
        deactivate UI
    end
```

---

## 🎯 Resumo da Conformidade com a Engenharia de Software

1. **Alinhamento com o Diagrama de Classes**: Lifelines exatamente espelhadas em `RecommenderAPI`, `VilaCachosRecommender`, `ClienteProfile`, `ProdutoCatalogo` e `RegistroHistorico`.
2. **Cobertura Completa das Exceções**: Modelados os status codes `HTTP 400` (produto desconhecido), `HTTP 422` (falha de tipagem/domínio), `HTTP 429` (rate limit) e `HTTP 503` (motor não ajustado).
3. **Compatibilidade Draw.io**: Uso exclusivo de sintaxe pura Mermaid, com nomes de setas legíveis, blocos `activate/deactivate` balanceados e sem caracteres incompatíveis.
