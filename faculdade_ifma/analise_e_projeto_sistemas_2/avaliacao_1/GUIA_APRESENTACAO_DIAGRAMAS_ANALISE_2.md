# Guia Completo de Apresentação dos Diagramas de Sequência — Análise 2
## Sistema Vila Cachos AI — Totem de Diagnóstico Capilar & Recomendação Híbrida

> **Público-alvo:** Alunos e avaliadores da disciplina de **Análise 2** (Engenharia de Software / Análise e Projeto de Sistemas).  
> **Arquivo draw.io correspondente:** `diagramas/sequencias.drawio` (6 páginas nativas).  
> **Documento PDF compilado:** `diagramas/diagramas_sequencia_drawio_completo.pdf`.

---

## 🏛️ 1. Fundamentação Arquitetural dos Diagramas

Todos os diagramas de sequência foram modelados seguindo o consagrado padrão **BCE (Boundary-Controller-Entity)** e princípios de **Separação de Responsabilidades (SoC)**:

```
[ Ator Humano ]  <--->  [ Fronteira (Boundary) ]  <--->  [ Controlador (Controller) ]  <--->  [ Domínio / Entidade (Entity) ]
 Cliente/Gestor              Interface Web (Totem)            RecommenderAPI (FastAPI)           VilaCachosRecommender / CSV
```

### Linhas de Vida (Lifelines) Padronizadas:
1. **`Cliente do salão` / `Gestor`**: Atores humanos primários do sistema.
2. **`Interface Web` (Boundary)**: Totem touch-screen em React/TanStack Router, responsável pela máquina de estados do formulário e validações client-side.
3. **`RecommenderAPI` (Controller)**: Gateway REST em FastAPI com tipagem estrita via Pydantic, Rate Limiting e tratamento HTTP padronizado.
4. **`VilaCachosRecommender` (Service/Domain)**: Núcleo de Machine Learning (K-Means + Scoring Híbrido Convexo + Média Bayesiana).
5. **`ProdutoCatalogo` & `RegistroHistorico` (Entity/Persistence)**: Matriz tricológica oficial e base histórica persistida em CSV.

---

## 📋 2. Matriz de Rastreabilidade (Casos de Uso vs. Requisitos)

| Página / Diagrama | Caso de Uso | Atores | Requisitos Funcionais (RF) | Regras de Negócio (RN) | Requisitos Não Funcionais (RNF) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Pág. 1** | **UC-02**: Preencher Anamnese Capilar | Cliente do Salão | RF-01, RF-02, RF-03, RF-19, RF-21 | RN-01, RN-02, RN-03, RN-04, RN-05 | RNF-06 (Timeout 15 min) |
| **Pág. 2** | **UC-03**: Gerar Recomendação Híbrida | Cliente do Salão | RF-04 a RF-11, RF-22 | RN-01 a RN-12, RN-14 | RNF-03 (Rate Limit), RNF-08 |
| **Pág. 3** | **UC-04**: Visualizar Diagnóstico e Recomendações | Cliente do Salão | RF-10, RF-11, RF-12, RF-19 | RN-11, RN-12, RN-14 | RNF-01 (Tempo resposta < 2s) |
| **Pág. 4** | **UC-05**: Registrar Feedback de Produto | Cliente do Salão | RF-13 a RF-16, RF-22 | RN-13, RN-15 | RNF-03 (Rate Limit) |
| **Pág. 5** | **UC-06**: Consultar Catálogo | Gestor do Salão | RF-17 | RN-06, RN-07 | RNF-11 (Auditoria de catálogo) |
| **Pág. 6** | **UC-07**: Monitorar Saúde e Métricas de IA | Gestor do Salão | RF-18 | RN-09 | RNF-08 (Disponibilidade), RNF-12 (Silhouette) |

---

## 🎙️ 3. Roteiro de Apresentação Página por Página (O que Falar para o Professor)

---

### 📄 Página 1: UC-02 — Preencher Anamnese Capilar
* **Objetivo:** Capturar de forma guiada os atributos da cliente para consolidar o vetor de 8 variáveis que alimenta a IA.

#### Passo a Passo para Narrar:
1. **Abertura:** *"O cliente toca em 'Iniciar Diagnóstico'. A Interface Web inicializa o estado local da anamnese e renderiza o primeiro passo (Curvatura: 2-Ondulado, 3-Cacheado ou 4-Crespo)."*
2. **Navegação Não-Destrutiva (`opt` Fluxo Alternativo A1):** *"Adicionamos o operador `opt` para o fluxo de 'Voltar'. Caso a cliente queira rever sua escolha anterior, o estado não é apagado; ela pode alterar a opção e prosseguir normalmente."*
3. **Passos 2 e 3:** *"A interface coleta o Nível de Porosidade (1-Baixa, 2-Média, 3-Alta) e a presença de Dano Químico (0 ou 1)."*
4. **Tratamento de Queixas (`alt` Fluxo Alternativo A3):**
   * *Se a cliente marca queixas:* O vetor ativa as flags correspondentes (`frizz`, `ressecamento`, `couro`, `quebra`).
   * *Se nenhuma queixa for selecionada:* Modela a **RN-04 / RN-05**. A interface zera as flags, direcionando a IA para aplicar score base de 0.5 e acionar a rotina de Manutenção Geral Preventiva.
5. **Segurança no Totem Físico (`opt` Exceção E1 - RNF-06):** *"Como o totem fica em espaço público, se houver inatividade por 15 minutos, a sessão é destruída por segurança e o sistema retorna à tela inicial."*
6. **Fechamento:** *"Ao clicar em 'Gerar Recomendação', a interface consolida o payload `ClienteProfile` com as 8 variáveis e dispara o UC-03."*

---

### 📄 Página 2: UC-03 — Gerar Recomendação Híbrida (Coração da IA)
* **Objetivo:** Executar o pipeline de inteligência artificial combinando K-Means, filtragem baseada em regras químicas e média ponderada bayesiana.

#### Passo a Passo para Narrar:
1. **Controle de Exceções HTTP no Gateway (`alt`):**
   * `HTTP 429`: Limite de 10 requisições/minuto excedido (Rate Limiting RNF-03 contra ataques de negação de serviço).
   * `HTTP 422`: Falha de validação estrutural Pydantic (ex: valores fora dos limites permitidos).
   * `HTTP 503`: Motor de IA indisponível ou ainda não ajustado (`is_fitted == False`).
2. **Normalização e Predição do Cluster K-Means (Passo 1):**
   * O vetor de 8 variáveis é padronizado pelo `StandardScaler.transform()`.
   * O método `kmeans.predict()` infere o `cluster_id` correspondente à persona clínica da cliente.
3. **Cálculo dos Pesos Adaptativos (Passo 2 / RN-10):**
   * O motor consulta a quantidade de avaliações históricas registradas naquele cluster.
   * Aplica a fórmula convexa adaptativa:
     $$\alpha = \min\left(0.60, \frac{\text{total\_avaliacoes\_cluster}}{100}\right)$$
     $$Peso_{\text{conteudo}} = 1.0 - \alpha$$
   * *Explicação para o professor:* *"Quando o cluster é novo, confiamos 100% na ciência dos cosméticos. Conforme o salão acumula clientes reais, o feedback coletivo passa a ter até 60% de peso na decisão."*
4. **Scoring Híbrido em Laço (`loop` para cada produto do catálogo):**
   * **Score de Conteúdo (Knowledge-Based / RN-06 a RN-08):** Cruza a compatibilidade de curvatura (fator redutor para produtos pesados em fios tipo 2) com a necessidade de nutrição, hidratação ou reconstrução.
   * **Score Colaborativo Bayesiano (RN-09):** Busca as notas das clientes do mesmo cluster e aplica suavização de Laplace para amortecer itens com poucas avaliações:
     $$\text{Média Amortecida} = \frac{5 \cdot \mu_{\text{global}} + \sum \text{notas}}{5 + n}$$
   * **Combinação Convexa Final (RN-11 / RN-12):**
     $$Score_{\text{final}} = (Peso_{\text{conteudo}} \cdot Score_{\text{conteudo}}) + (\alpha \cdot Score_{\text{bayesiano}})$$
     $$\text{Estrelas Estimadas} = 1.0 + (Score_{\text{final}} \cdot 4.0)$$
5. **Explicabilidade Semântica (XAI) & Top 3:**
   * O sistema gera a justificativa clínica em linguagem natural (*"Por que para você?"*).
   * Ordena por score decrescente e retorna os 3 melhores produtos no `HTTP 200 OK`.

---

### 📄 Página 3: UC-04 — Visualizar Diagnóstico e Recomendações
* **Objetivo:** Exibir a prescrição cosmética e prover explicabilidade transparente (XAI) ao usuário final.

#### Passo a Passo para Narrar:
1. **Tratamento de Falhas (`alt` Exceção E1):** Se a conexão cair ou a resposta vier inconsistente, a interface exibe aviso claro sem travar a aplicação.
2. **Renderização Explicável (XAI):**
   * Renderiza a badge da Persona (*ex: Cluster Clínico #1*).
   * Renderiza a barra proporcional de pesos (*ex: 65% Matriz Especialista vs. 35% Avaliações Reais de Salão*).
3. **Apresentação do Top 3:**
   * Aplica destaque visual no 1º colocado (*Match Principal / Produto Campeão*).
   * Mostra categoria, afinidade, estimativa em estrelas e o motivo tricológico.
4. **Extensões de Ação (`opt`):**
   * `Ação 1`: Reiniciar diagnóstico (RF-19) — limpa o estado e volta ao acolhimento.
   * `Ação 2`: Avaliar produto — abre a oportunidade de feedback imediato, estendendo para o UC-05.

---

### 📄 Página 4: UC-05 — Registrar Feedback de Produto (Active Learning Loop)
* **Objetivo:** Fechar o ciclo de retroalimentação contínua da IA a partir da opinião da cliente pós-uso.

#### Passo a Passo para Narrar:
1. **Validações Iniciais (`alt`):**
   * Verifica limites de requisição (`HTTP 429`).
   * Valida se a nota é inteira de 1 a 5 (`HTTP 422`).
   * **Integridade Referencial (RF-14):** A API checa se o nome do produto existe no `CATALOGO_PRODUTOS`. Se não existir, rejeita com `HTTP 400 Bad Request`.
2. **Processamento em Memória (Caminho Feliz):**
   * Reexecuta o classificador para identificar o cluster da cliente avaliadora.
   * Concatena a nova linha ao DataFrame histórico em memória.
   * Recalcula imediatamente a média global de satisfação do salão.
3. **Persistência Imediata em Disco (RF-16):**
   * Grava imediatamente no arquivo físico `dataset_historico_vila_cachos.csv` para garantir durabilidade e tolerância a quedas de servidor.
4. **Resposta e Confirmação:**
   * Responde com `HTTP 200 OK` informando qual cluster foi recalibrado e a nova média do salão.
   * A interface substitui as estrelas por uma mensagem de sucesso em tempo real.

---

### 📄 Página 5: UC-06 — Consultar Catálogo
* **Objetivo:** Permitir ao gestor do salão auditar as regras e ativos dos cosméticos oficiais.

#### Passo a Passo para Narrar:
1. O gestor acessa a interface de administração.
2. A interface dispara `GET /catalogo` para a `RecommenderAPI`.
3. A API acessa a entidade estática `CATALOGO_PRODUTOS` e serializa todos os atributos (identificador, marca, compatibilidade de curvatura, nível lipídico e proteico).
4. Retorna `HTTP 200 OK` com a lista completa, permitindo exibição tabular técnica.

---

### 📄 Página 6: UC-07 — Monitorar Saúde e Métricas de IA
* **Objetivo:** Prover telemetria científica e auditoria da qualidade dos clusters em tempo de execução.

#### Passo a Passo para Narrar:
1. **Health Check Operacional (`alt`):** Se o motor não estiver instanciado ou treinado, responde `HTTP 503 Service Unavailable`, gerando alerta imediato no dashboard.
2. **Métricas Científicas de IA (RNF-12):**
   * Total de clientes na base e média de satisfação.
   * **Score Silhouette:** Executa o cálculo da métrica de coesão e separação dos clusters no espaço vetorial normalizado:
     $$s = \frac{b - a}{\max(a, b)} \in [-1, 1]$$
   * **Inércia Intra-cluster ($WCSS$):** Extrai `kmeans.inertia_` (soma das distâncias euclidianas quadráticas até o centroide).
3. **Desfecho:** Retorna `HTTP 200 OK` com o diagnóstico de integridade da IA para o painel de monitoramento do salão.

---

## 💡 4. Respostas Prontas para Perguntas Difíceis da Banca

* **Pergunta 1:** *"Por que usar um diagrama de sequência separado para o UC-04 se ele é só tela?"*  
  **Resposta:** *"Porque o UC-04 modela a fronteira de apresentação e o desacoplamento de UI perante exceções de rede, além de orquestrar os pontos de extensão para novos diagnósticos e engajamento com o UC-05."*

* **Pergunta 2:** *"O que acontece se o banco/disco falhar no momento do feedback (UC-05)?"*  
  **Resposta:** *"O diagrama modela a persistência imediata (RF-16) separada da resposta da API. Se a gravação falhar, o status de erro é capturado pela RecommenderAPI e retornado com código de falha apropriado, evitando falso-positivo para a cliente."*

* **Pergunta 3:** *"Por que a recomendação do UC-03 é síncrona em vez de assíncrona?"*  
  **Resposta:** *"Por requisito de negócio (RNF-01). Como a inferência com K-Means e scoring ponderado roda em ~25-40 milissegundos, a requisição síncrona simplifica a arquitetura sem necessidade de filas (RabbitMQ/Celery) e entrega a resposta no totem em tempo real."*
