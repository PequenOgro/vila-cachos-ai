# Modelagem UML: Sistema Híbrido Vila Cachos

Este documento contém a diagramação formal dos fluxos funcionais mapeados no sistema **Vila Cachos AI**, empregando notação UML adaptada para renderização nativa via Mermaid.js.

---

## 1. Diagrama de Casos de Uso (Visão Geral)

O diagrama abaixo delineia a fronteira do sistema (*System Boundary*) e as associações diretas entre os quatro atores principais e os casos de uso de negócio.

```mermaid
flowchart LR
    %% Configuração de Estilo para Atores e Casos de Uso
    classDef actor fill:#f9f9f9,stroke:#333,stroke-width:2px,shape:circle;
    classDef uc fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,shape:stadium,color:#000;
    classDef boundary fill:transparent,stroke:#999,stroke-width:2px,stroke-dasharray: 5 5;

    %% Atores
    Cliente(("👤 Cliente do Salão")):::actor
    Profissional(("✂️ Profissional")):::actor
    Gestor(("📊 Gestor do Salão")):::actor
    MotorIA(("🤖 Motor de IA (FastAPI)")):::actor

    %% Fronteira do Sistema
    subgraph Sistema ["Fronteira do Sistema (Web App Vila Cachos)"]
        direction TB
        UC01(["UC-01: Realizar Anamnese Capilar"]):::uc
        UC02(["UC-02: Gerar Diagnóstico e Recomendação"]):::uc
        UC03(["UC-03: Visualizar Top 3 Produtos e XAI"]):::uc
        UC04(["UC-04: Registrar Avaliação (Feedback)"]):::uc
        UC05(["UC-05: Recalibrar Média Bayesiana"]):::uc
        UC06(["UC-06: Monitorar Métricas e Clusters"]):::uc
        UC07(["UC-07: Consultar Catálogo Oficial"]):::uc
        
        %% Relacionamentos <<include>> e <<extend>>
        UC01 -. "<<include>>" .-> UC02
        UC02 -. "<<include>>" .-> UC03
        UC04 -. "<<include>>" .-> UC05
        UC04 -. "<<extend>>" .-> UC03
    end
    class Sistema boundary

    %% Associações dos Atores (Linhas Sólidas)
    Cliente --- UC01
    Cliente --- UC03
    Cliente --- UC04
    Cliente --- UC07
    
    Profissional --- UC01
    Profissional --- UC03
    Profissional --- UC07
    
    Gestor --- UC06
    
    UC02 --- MotorIA
    UC05 --- MotorIA
    UC06 --- MotorIA
```

---

## 2. Diagrama de Sequência (O Fluxo Crítico de Cold Start)

Este diagrama detalha o processo interativo onde uma cliente (mesmo sem histórico prévio na base do salão) realiza a anamnese, interage com a API e recebe as recomendações derivadas da combinação do aprendizado não-supervisionado com o mapeamento especializado (XAI).

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente do Salão
    participant UI as Interface Web (React)
    participant API as API RESTful (FastAPI)
    participant Motor as Motor Híbrido (K-Means)
    
    C->>UI: Acessa o Web App (QR Code/Link)
    UI-->>C: Apresenta tela de Anamnese (Wizard)
    
    C->>UI: Preenche atributos (curvatura, porosidade, químicas, dores)
    C->>UI: Submete formulário
    UI->>API: POST /recommend (Payload JSON: ClienteProfile)
    
    rect rgb(240, 248, 255)
        Note over API, Motor: Tratamento do Problema de Cold Start
        API->>Motor: prever_cluster(perfil_cliente)
        Motor->>Motor: Aplica scaler (StandardScaler) sobre as 8 dimensões
        Motor-->>API: Retorna ID do Cluster (Persona Dominante)
        
        API->>Motor: calcular_score_hibrido(top_k=3)
        Motor->>Motor: 1. Calcula Afinidade Terapêutica (Knowledge-Based)
        Motor->>Motor: 2. Calcula Média Bayesiana Amortecida (Feedback Colaborativo)
        Motor->>Motor: 3. Aplica Combinação Convexa (Peso α dinâmico)
        Motor->>Motor: 4. Gera strings de justificativa clínica (XAI)
        Motor-->>API: Retorna Lista Top 3 Ordenada
    end
    
    API-->>UI: Resposta 200 OK (JSON com Recomendações e Descrição da Persona)
    UI-->>C: Exibe o Top 3 Cosméticos + Estrelas Estimadas + Justificativa
```

---

## 3. Especificação Formal de Casos de Uso

Abaixo encontram-se as descrições de alto rigor da Engenharia de Software para os dois casos de uso arquiteturalmente mais complexos, cobrindo o fluxo principal (happy path) e as exceções.

### UC-01: Geração de Diagnóstico e Recomendação Híbrida

*   **Atores Principais:** Cliente do Salão.
*   **Atores Secundários:** Profissional Cabeleireiro, Motor de IA.
*   **Objetivo:** Processar o quadro biofísico capilar e queixas clínicas informadas para gerar uma indicação algorítmica dos 3 melhores cosméticos do catálogo, mitigando o *Cold Start*.
*   **Pré-condições:** O sistema deve estar operacional, o modelo K-Means deve estar carregado e previamente ajustado (`is_fitted=True`) com a constante bayesiana populada. A interface do usuário não pode estar em estado de timeout.

**Fluxo Principal (Happy Path):**
1. O Cliente seleciona "Iniciar Diagnóstico" no Web App.
2. O sistema exibe o Wizard de 8 variáveis (Curvatura, Porosidade, Danos Químicos, Queixas Ativas).
3. O Cliente (opcionalmente auxiliado pelo Profissional) preenche todos os campos obrigatórios.
4. O Cliente aciona a submissão do formulário.
5. A Interface valida o modelo de dados localmente e dispara uma requisição `POST /recommend`.
6. O Motor de IA recebe o vetor, normaliza os dados com o `StandardScaler` e infere a Persona usando K-Means.
7. O Motor calcula os scores `Knowledge-Based` baseados nas queixas mapeadas e cruza com a Média Bayesiana Amortecida do Cluster.
8. O Motor retorna o array das 3 recomendações de maior pontuação com suas respectivas justificativas (XAI).
9. A Interface renderiza os resultados, destacando a compatibilidade terapêutica para a cliente.

**Fluxos de Exceção:**
*   *FE-01: Inatividade do Cliente (Timeout).* Se o cliente permanecer 15 minutos sem interação durante o preenchimento, o componente React força um reinício global da sessão (limpeza do state). O fluxo é encerrado por questões de privacidade e economia de infraestrutura.
*   *FE-02: Limite de Requisições Atingido (Rate Limit).* Se o mesmo IP disparar o cálculo mais de 10 vezes por minuto, a API aborta a inferência e retorna `HTTP 429 Too Many Requests`. O Web App notifica o cliente para aguardar alguns instantes antes de tentar novamente.
*   *FE-03: Motor Indisponível.* Se o modelo não estiver carregado na memória do servidor, a API retorna `HTTP 503 Service Unavailable`. O sistema orienta contatar a administração do salão.

---

### UC-02: Calibração de Pesos via Feedback Loop Bayesiano

*   **Atores Principais:** Cliente do Salão.
*   **Atores Secundários:** Motor de IA.
*   **Objetivo:** Fechar o ciclo de recomendação capturando a validação empírica pós-atendimento. A nota submetida atuará dinamicamente para ancorar futuras recomendações a dados reais (Collaborative Filtering iterativo).
*   **Pré-condições:** O Cliente deve ter passado por um atendimento e ter ciência do cosmético utilizado. O perfil capilar do cliente (vetor de 8 variáveis) deve estar preservado no estado da requisição.

**Fluxo Principal (Happy Path):**
1. A partir da visualização das recomendações (`UC-03`), o Cliente clica em "Avaliar Resultado".
2. O sistema exibe um modal solicitando a confirmação do nome do produto utilizado e a seleção da nota de satisfação de 1 a 5 estrelas.
3. O Cliente preenche a avaliação e confirma o envio.
4. A Interface dispara uma requisição `POST /feedback` com o pacote `FeedbackInput`.
5. O Motor de IA recebe o payload e verifica a integridade do nome do produto no Catálogo Oficial.
6. O Motor deduz a qual Cluster a avaliação pertence utilizando a mesma inferência do K-Means.
7. O Motor registra a nova nota no banco de dados analítico e atualiza a Média Global do salão em tempo real.
8. A API retorna `HTTP 200 OK` informando que o feedback foi persistido.
9. A Interface agradece a cliente pela colaboração e encerra a jornada ativa.

**Fluxos de Exceção:**
*   *FE-01: Produto Não Reconhecido.* Caso, por injeção ou falha de sincronia, a interface envie um produto ausente no `catalog.py`, o Back-end rejeita o input com `HTTP 400 Bad Request` informando o descompasso de catálogo. O Motor bloqueia a gravação para não corromper o dataset.
*   *FE-02: Rate Limit de Feedback (Abuso/Spam).* Se o IP enviar excesso de formulários num período curto, o mecanismo de SlowAPI barra a requisição (`HTTP 429`) protegendo a Média Bayesiana de poluição maliciosa.
