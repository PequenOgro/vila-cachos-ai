# Contexto Mestre de Requisitos e Preparação para Modelagem UML
**Projeto:** Web App de Diagnóstico Capilar com IA Híbrida para a Vila Cachos  
**Nível Acadêmico:** Trabalho de Conclusão de Curso (TCC) — Bacharelado em Sistemas de Informação (IFMA)  
**Documento:** Memória Oficial de Requisitos, Atores e Fronteiras do Sistema  
**Status:** Baseline Aprovada para Modelagem UML  

---

## 1. Visão Geral Funcional do Sistema

O **Vila Cachos AI** é uma solução de software concebida na interseção entre **Engenharia de Software** e **Sistemas de Recomendação (Inteligência Artificial)**. O seu propósito primordial é padronizar, agilizar e enriquecer tecnicamente o diagnóstico capilar em salões especializados em cabelos com curvatura (ondulados, cacheados e crespos — tipos 2, 3 e 4 da classificação de André Walker), mitigando o clássico problema do *Cold Start* através de uma arquitetura híbrida de IA.

O sistema opera na modalidade de **Web App responsivo**, acessível universalmente via navegador web (smartphones, tablets ou computadores do salão), dispensando dependências de totens de autoatendimento físicos proprietários ou infraestruturas dedicadas de hardware.

### 1.1 O Macrofluxo Funcional Integrado (End-to-End)

```
[ Início ]
   │
   ▼
[ 1. Anamnese Capilar Web (Wizard Reativo) ]
   │  ↳ Coleta de 8 variáveis padronizadas do fio e queixas clínicas
   ▼
[ 2. Motor de IA Híbrido (FastAPI Back-end) ]
   │  ├─ Normalização com StandardScaler
   │  ├─ Segmentação de Persona via K-Means (k=4)
   │  ├─ Componente Baseado em Conhecimento (Cold Start / Regras Terapêuticas)
   │  └─ Componente Colaborativo Bayesiano (Média Amortecida por Feedback Histórico)
   ▼
[ 3. Apresentação do Diagnóstico e Top 3 Recomendações ]
   │  ↳ Exibição de produtos compatíveis com Justificativa Explicável (XAI)
   ▼
[ 4. Ciclo de Aprendizado Contínuo (Bayesian Feedback Loop) ]
   │  ↳ Registro de nota explícita (1 a 5 estrelas) pós-atendimento
   ▼
[ Recalibração de Pesos do Cluster & Persistência Histórica ]
   │
   ▼
[ Fim / Reset da Sessão ]
```

1. **Anamnese Capilar Web (Wizard Interativo):**  
   A cliente (de forma autônoma ou guiada pelo profissional cabeleireiro) responde a um formulário guiado em etapas, coletando o perfil biofísico do cabelo e as necessidades imediatas em um espaço vetorial de 8 dimensões normalizadas:
   - **Curvatura:** Ondulado (2), Cacheado (3) ou Crespo (4);
   - **Porosidade do Fio:** Baixa (1), Média (2) ou Alta (3);
   - **Histórico de Química Agressiva:** Não (0) ou Sim (1) — envolvendo descoloração ou alisamentos;
   - **Queixas Terapêuticas Binárias (0 ou 1):**
     - *Ressecamento e Opacidade*;
     - *Alta Porosidade Química / Fios Elásticos*;
     - *Frizz e Falta de Definição*;
     - *Transição Capilar (Dupla Textura)*;
     - *Couro Cabeludo Sensível ou Oleoso*.

2. **Inferência no Motor de IA Híbrido:**  
   O perfil estruturado é transmitido via requisição REST (`POST /recommend`) para a API FastAPI:
   - **Segmentação Não-Supervisionada (K-Means, $k=4$):** O vetor é normalizado (`StandardScaler`) e classificado em uma das 4 personas dominantes da Vila Cachos, identificando padrões clínicos correlacionados.
   - **Pontuação Baseada em Conhecimento (*Knowledge-Based*):** Garante assertividade imediata no *Cold Start*, avaliando a compatibilidade mecânica do produto com a curvatura (e peso do cosmético) e a matriz de afinidade terapêutica com as queixas ativas.
   - **Pontuação Colaborativa Amortecida (Média Bayesiana):** Avalia a eficácia histórica do cosmético entre clientes pertencentes à mesma persona ($S_{bayes} = \frac{C \cdot m + \sum \text{notas}}{C + n}$), ancorada em uma constante de confiança $C=5$ e na média global do salão $m$.
   - **Combinação Convexa Adaptativa:** Combina as duas camadas ponderando dinamicamente o volume de avaliações coletadas para aquele cluster ($\alpha_{\text{feedback}} = \min(0.60, \frac{N_{\text{cluster}}}{100})$).

3. **Geração do Top 3 Recomendações com XAI:**  
   A interface apresenta os 3 melhores cosméticos/tratamentos, acompanhados de justificativas em linguagem natural (*Explainable AI*), evidenciando a correlação direta entre o cosmético sugerido e a principal dor reportada pela cliente.

4. **Feedback Loop Bayesiano:**  
   Após o procedimento no salão ou teste do produto, registra-se a avaliação real de satisfação (1 a 5 estrelas) através de `POST /feedback`. O motor atualiza dinamicamente o histórico analítico persistente, recalibrando a média bayesiana do cluster para os atendimentos futuros.

---

## 2. Mapeamento de Atores do Sistema (Atores UML)

Para a correta representação nos Diagramas de Casos de Uso e Modelagem Comportamental UML, foram identificados os seguintes atores:

```
                  ┌───────────────────────────────┐
                  │    <<actor>>                  │
                  │    Cliente do Salão           │
                  │    (Ator Primário Humano)     │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
┌─────────────────────────────────┼─────────────────────────────────┐
│                    FRONTEIRA DO WEB APP VILA CACHOS               │
│                                                                   │
│   [UC01 - Responder Anamnese]       [UC02 - Visualizar Diagnóstico]│
│   [UC03 - Consultar Catálogo]       [UC04 - Fornecer Feedback]     │
│                                                                   │
└─────────────────────────────────┬─────────────────────────────────┘
                                  ▲
        ┌─────────────────────────┴─────────────────────────┐
        │                                                   │
┌───────┴───────────────────────┐   ┌───────────────────────┴───────┐
│ <<actor>>                     │   │ <<actor>>                     │
│ Profissional / Cabeleireiro   │   │ Motor de IA / Back-end        │
│ (Ator Secundário Humano)      │   │ (Ator de Suporte / Sistema)   │
└───────────────────────────────┘   └───────────────────────────────┘
```

### Ator 1: Cliente do Salão (Ator Primário — Humano)
*   **Papel no Domínio:** Usuária final interessada no cuidado e tratamento da sua curvatura natural.
*   **Interações com o Sistema:**
    *   Acessa o Web App pelo navegador (via link direto no site do salão ou QR Code).
    *   Preenche o questionário interativo de Anamnese Capilar (curvatura, porosidade, químicas e queixas).
    *   Visualiza o resultado do diagnóstico, o perfil da sua persona e o Top 3 produtos recomendados com justificativas XAI.
    *   Avalia a experiência e o resultado do produto/tratamento com nota explícita de 1 a 5 estrelas pós-atendimento.

### Ator 2: Profissional / Cabeleireiro(a) (Ator Secundário / Especialista — Humano)
*   **Papel no Domínio:** Especialista técnico da Vila Cachos responsável pela avaliação física do fio e aplicação dos tratamentos.
*   **Interações com o Sistema:**
    *   Auxilia a cliente na identificação técnica de atributos complexos (diferenciar grau de porosidade, elasticidade por tração, histórico de químicas incompatíveis).
    *   Utiliza as recomendações e justificativas da IA (XAI) como suporte à decisão clínica na bancada/lavatório.
    *   Consulta o Catálogo Terapêutico completo de cosméticos para conferir ativos, marcas (Arvensis, Curly Care, Deva Curl) e contraindicações de peso do fio.

### Ator 3: Motor de IA / Back-end (Ator Secundário de Suporte — Sistema / Serviço)
*   **Papel no Domínio:** Núcleo analítico computacional construído em FastAPI e Scikit-Learn.
*   **Interações com o Sistema:**
    *   Recebe o perfil submetido, aplica normalização vetorial e executa a inferência de agrupamento via K-Means ($k=4$).
    *   Calcula os scores híbridos combinando heurísticas de catálogo e média bayesiana amortecida.
    *   Gera as justificativas de explicabilidade (XAI) em linguagem natural.
    *   Executa o ciclo de retroalimentação (*Feedback Loop*), recalculando a média global e os pesos amostrais do cluster.
    *   Monitora e expõe métricas de qualidade algorítmica (Silhouette Score, Inércia intra-cluster) e saúde da API.

### Ator 4: Gestor do Salão / Administrador (Ator Secundário — Humano [Extensão Operacional])
*   **Papel no Domínio:** Responsável administrativo pela operação do salão e homologação do sistema.
*   **Interações com o Sistema:**
    *   Consulta o endpoint de telemetria e integridade (`/health`), verificando a quantidade de atendimentos acumulados e a convergência da satisfação.
    *   Verifica a estabilidade estatística do modelo para suporte à tomada de decisões de reposição de estoque de cosméticos.

---

## 3. Fronteiras do Sistema (System Boundaries & Scope)

Para resguardar o rigor metodológico do TCC e garantir a viabilidade técnica do MVP (Mínimo Produto Viável), o escopo funcional e as fronteiras do sistema são rigorosamente delimitados:

### 3.1 O que o Sistema FAZ (Escopo Funcional / In-Scope)

1. **Anamnese Capilar Estruturada:**
   * Coleta padronizada das 8 variáveis do fio através de interface reativa, limpa e acessível.
   * Validação estrita dos tipos de dados via esquemas Pydantic na API.
2. **Segmentação Não-Supervisionada de Personas (K-Means):**
   * Agrupamento de clientes em 4 personas clínicas baseadas em centróides estatísticos calculados sobre dados normalizados.
3. **Motor Híbrido de Recomendação de Cosméticos:**
   * Tratamento formal do *Cold Start* por meio de regras de afinidade terapêutica (Knowledge-Based).
   * Ponderação colaborativa amortecida por Média Bayesiana ($C=5$).
   * Ordenação e seleção dos Top 3 produtos mais adequados do catálogo da Vila Cachos.
4. **Explicabilidade Algorítmica (XAI):**
   * Emissão de justificativa amigável em linguagem natural explicando explicitamente o porquê da recomendação.
   * Transparência da composição do score final e exibição amigável de estrelas estimadas (1 a 5).
5. **Feedback Loop Contínuo:**
   * Interface de avaliação por estrelas (1 a 5).
   * Persistência histórica e recalibração dinâmica em tempo de execução.
6. **Consulta ao Catálogo Terapêutico:**
   * Exibição das propriedades dos produtos cadastrados (marcas profissionais: Curly Care, Arvensis, Deva Curl, categorias e afinidades).
7. **Requisitos Não-Funcionais Corporativos:**
   * **Segurança e Proteção:** *Rate Limiting* (10 requisições/minuto por IP via SlowAPI com retorno HTTP 429).
   * **Usabilidade:** Suporte completo a *Dark Mode* para redução de fadiga visual em ambientes de salão.
   * **Privacidade de Dados:** *Inactivity Timeout* com reset automático de sessão após 15 minutos de ociosidade.

### 3.2 O que o Sistema NÃO FAZ (Fora de Escopo / Out-of-Scope)

A fim de preservar o foco da pesquisa científica do TCC e evitar dispersão de esforço em funcionalidades acessórias de ERP ou e-commerce:

1. **NÃO é Sistema de Agendamento ou Marcação de Horários:**
   * O sistema não gerencia agenda de clientes, calendários de cabeleireiros, lista de espera ou cancelamentos.
2. **NÃO é E-commerce ou Gateway de Pagamento:**
   * O sistema não possui carrinho de compras, checkout, integração com cartão de crédito, PIX, cálculo de frete ou venda online de cosméticos.
3. **NÃO é ERP de Gestão de Estoque Físico ou Financeiro:**
   * O sistema não controla baixas físicas de almoxarifado, emissão de notas fiscais (NF-e), fluxo de caixa, comissões de profissionais ou contas a pagar/receber.
4. **NÃO realiza Diagnóstico por Processamento de Imagens / Visão Computacional:**
   * O diagnóstico é fundamentado na anamnese clínica declarativa preenchida no wizard (curvatura, porosidade, químicas e queixas); não há upload de fotos ou redes neurais convolucionais (CNNs) para segmentação de imagens de cabelo.
5. **NÃO possui Qualquer Relação com Infraestrutura Hídrica ou Saneamento:**
   * Total isolamento e ausência absoluta de escopo relacionado a CAEMA, controle hidrométrico, abastecimento ou projetos corporativos externos. O escopo é 100% beleza, estética capilar e sistemas de recomendação com IA.

---

## 4. Pacote Preliminar de Casos de Uso (Preparação para Diagramação UML)

Abaixo estruturam-se os casos de uso identificados para subsidiar a elaboração dos diagramas de Casos de Uso, Sequência e Classes:

| Identificador | Caso de Uso | Atores Envolvidos | Descrição Sumária |
| :--- | :--- | :--- | :--- |
| **UC01** | Realizar Anamnese Capilar | Cliente do Salão, Profissional Cabeleireiro | Preenchimento guiado dos atributos biofísicos do cabelo e queixas relatadas. |
| **UC02** | Gerar Recomendações Personalizadas | Motor de IA / Back-end | Processamento das 8 variáveis, agrupamento por persona e cálculo do ranking Top 3 híbrido com XAI. |
| **UC03** | Visualizar Recomendações e Justificativas (XAI) | Cliente do Salão, Profissional Cabeleireiro | Exibição detalhada dos cosméticos sugeridos, score de afinidade e justificativa clínica em linguagem natural. |
| **UC04** | Registrar Avaliação Pós-Atendimento (Feedback) | Cliente do Salão, Motor de IA / Back-end | Submissão da nota de 1 a 5 estrelas e recalibração bayesiana amortecida da média do produto no cluster. |
| **UC05** | Consultar Catálogo de Cosméticos | Cliente do Salão, Profissional Cabeleireiro | Navegação e visualização da lista oficial de cosméticos, categorias e fichas técnicas da Vila Cachos. |
| **UC06** | Monitorar Saúde e Métricas do Motor | Gestor do Salão, Motor de IA / Back-end | Consulta a indicadores do modelo (Silhouette Score, Inércia intra-cluster, total de avaliações e média global). |
| **UC07** | Gerenciar Sessão e Inatividade | Sistema / Interface Web | Reinício automático da interface e limpeza do estado após 15 minutos sem interação da usuária. |

### 4.1 Relações Previstas entre Casos de Uso

*   `UC01 (Realizar Anamnese Capilar)` **<<include>>** `UC02 (Gerar Recomendações Personalizadas)`: Toda anamnese completa culmina obrigatoriamente na chamada ao motor preditivo.
*   `UC02 (Gerar Recomendações Personalizadas)` **<<include>>** `UC03 (Visualizar Recomendações e Justificativas)`: O cálculo algorítmico gera a projeção reativa do Top 3 produtos na interface.
*   `UC04 (Registrar Avaliação)` **<<extend>>** `UC03 (Visualizar Recomendações)`: O registro de nota pode ser disparado a partir da tela de recomendações concluídas.
*   `UC07 (Gerenciar Sessão)` atua transversalmente como regra de negócio e controle de estado em todos os fluxos de interface.

---

## 5. Matriz de Rastreabilidade Preliminar (Requisitos Funcionais)

| Código RF | Descrição do Requisito Funcional | Caso de Uso Associado | Endpoint / Componente |
| :--- | :--- | :--- | :--- |
| **RF01** | Coletar curvatura, porosidade, dano químico e queixas clínicas. | UC01 | `App.jsx` (Wizard Component) |
| **RF02** | Normalizar vetor de características capilares (StandardScaler). | UC02 | `VilaCachosRecommender.prever_cluster` |
| **RF03** | Classificar cliente em cluster de persona via K-Means ($k=4$). | UC02 | `recommender_engine.py` / `api.py` |
| **RF04** | Calcular afinidade de conteúdo (*Cold Start*) por queixas e peso. | UC02 | `_calcular_score_conteudo` |
| **RF05** | Calcular média bayesiana amortecida ($C=5$) das avaliações do cluster. | UC02 | `_calcular_score_bayesiano` |
| **RF06** | Exibir Top 3 recomendações ordenadas por score combinado. | UC03 | `POST /recommend` |
| **RF07** | Exibir justificativa clínica compreensível (XAI) para cada produto. | UC03 | `RecomendacaoItem.motivo` |
| **RF08** | Registrar feedback pós-uso (1 a 5 estrelas) da cliente. | UC04 | `POST /feedback` |
| **RF09** | Recalcular pesos do cluster e persistir novo registro histórico. | UC04 | `VilaCachosRecommender.registrar_feedback` |
| **RF10** | Disponibilizar listagem do catálogo de cosméticos do salão. | UC05 | `GET /catalogo` |
| **RF11** | Disponibilizar telemetria e validação métrica dos clusters. | UC06 | `GET /health` |
| **RF12** | Resetar interface e memória temporária após 15 minutos de inatividade. | UC07 | `useInactivityTimeout` Hook (`App.jsx`) |

---

## 6. Conclusão e Diretriz para as Próximas Etapas

Este documento estabelece o **marco zero** e a **verdade canônica** do escopo funcional do TCC. Toda a subsequente modelagem UML (Diagramas de Caso de Uso em PlantUML/Mermaid, Diagramas de Atividades, Diagramas de Classes e Diagramas de Sequência da API FastAPI) deve rigorosamente derivar dos atores, regras e fronteiras aqui formalizados, mantendo o projeto integralmente aderente ao domínio de **diagnóstico capilar inteligente para o salão Vila Cachos**.
