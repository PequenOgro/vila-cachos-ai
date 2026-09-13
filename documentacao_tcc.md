# Documentação Acadêmica — TCC Sistemas de Informação (IFMA)

**Título Proposto:**
> *Sistema Híbrido de Recomendação de Produtos Capilares com Feedback Loop Bayesiano: Uma Solução para o Problema do Cold Start em Salões Especializados*

**Título Alternativo (mais curto):**
> *Recomendação Inteligente de Cosméticos Capilares: Motor Híbrido com Clusterização e Aprendizado Contínuo como Módulo Web Integrado*

---

## 1. Esqueleto de Capítulos e Subcapítulos

```
ELEMENTOS PRÉ-TEXTUAIS
  Capa
  Folha de Rosto
  Folha de Aprovação
  Resumo / Abstract
  Lista de Figuras
  Lista de Tabelas
  Lista de Abreviaturas e Siglas
  Sumário
```

---

### CAPÍTULO 1 — INTRODUÇÃO
- 1.1 Contextualização
- 1.2 Problema de Pesquisa
- 1.3 Justificativa
- 1.4 Objetivos
  - 1.4.1 Objetivo Geral
  - 1.4.2 Objetivos Específicos
- 1.5 Estrutura do Trabalho

### CAPÍTULO 2 — REFERENCIAL TEÓRICO
- 2.1 Sistemas de Recomendação
  - 2.1.1 Filtragem Baseada em Conteúdo (*Content-Based Filtering*)
  - 2.1.2 Filtragem Colaborativa (*Collaborative Filtering*)
  - 2.1.3 Abordagens Híbridas
  - 2.1.4 O Problema do Cold Start
- 2.2 Aprendizado de Máquina Não Supervisionado
  - 2.2.1 Algoritmo K-Means
  - 2.2.2 Normalização e Pré-processamento de Variáveis (StandardScaler)
  - 2.2.3 Métricas de Validação de Clusters (Silhouette Score, Inércia)
- 2.3 Inferência Bayesiana Aplicada
  - 2.3.1 Média Bayesiana Amortecida (*Damped Average*)
  - 2.3.2 Feedback Loop e Aprendizado Contínuo
- 2.4 Explicabilidade em Inteligência Artificial (XAI)
- 2.5 Arquitetura de Software para Sistemas Inteligentes
  - 2.5.1 APIs RESTful e o Padrão Cliente-Servidor
  - 2.5.2 Validação de Dados com Schemas Tipados (Pydantic)
- 2.6 Trabalhos Correlatos

### CAPÍTULO 3 — METODOLOGIA
- 3.1 Classificação da Pesquisa
- 3.2 Etapas Metodológicas
  - 3.2.1 Levantamento de Requisitos com o Salão Vila Cachos
  - 3.2.2 Modelagem do Domínio Capilar (Taxonomia de Queixas e Catálogo)
  - 3.2.3 Geração de Dados Sintéticos com Causalidade
  - 3.2.4 Projeto e Implementação do Motor Híbrido
  - 3.2.5 Construção da API e Interface do Web App de Diagnóstico (Módulo Web)
  - 3.2.6 Validação e Testes
- 3.3 Ferramentas e Tecnologias Utilizadas

### CAPÍTULO 4 — DESENVOLVIMENTO DO SISTEMA
- 4.1 Modelagem de Domínio
  - 4.1.1 Perfil da Cliente: Variáveis Estruturais e Vetor de Queixas
  - 4.1.2 Catálogo de Produtos e Matriz de Afinidade Terapêutica
- 4.2 Geração do Dataset Sintético Causal
  - 4.2.1 Regras de Probabilidade Condicional
  - 4.2.2 Distribuição Demográfica e Ruído Gaussiano Controlado
- 4.3 Motor Híbrido de Recomendação
  - 4.3.1 Camada 1: Pontuação Baseada em Conhecimento (*Knowledge-Based*)
  - 4.3.2 Camada 2: Segmentação de Personas via K-Means (8 dimensões)
  - 4.3.3 Camada 3: Calibração por Média Bayesiana Amortecida
  - 4.3.4 Função de Mistura Convexa e Ponderação Dinâmica (α)
  - 4.3.5 Módulo de Explicabilidade (XAI)
- 4.4 Arquitetura de Software
  - 4.4.1 API RESTful com FastAPI (Rotas, Schemas, CORS)
  - 4.4.2 Web App de Diagnóstico — Módulo Web (React, Vite, Tailwind CSS, hospedagem Vercel)
  - 4.4.3 Diagrama de Arquitetura Geral

### CAPÍTULO 5 — RESULTADOS E DISCUSSÃO
- 5.1 Análise Estatística do Dataset Gerado
- 5.2 Avaliação da Qualidade dos Clusters
  - 5.2.1 Coeficiente Silhouette e Inércia Intra-Cluster
  - 5.2.2 Método do Cotovelo para Escolha de *k*
  - 5.2.3 Interpretação Semântica das Personas Identificadas
- 5.3 Validação dos Cenários Clínicos de Recomendação
  - 5.3.1 Cenário 1: Ondulada com Couro Sensível
  - 5.3.2 Cenário 2: Cacheada com Alta Porosidade Química
  - 5.3.3 Cenário 3: Crespa com Ressecamento Severo
  - 5.3.4 Cenário 4: Transição Capilar
- 5.4 Demonstração do Feedback Loop (Convergência Bayesiana)
- 5.5 Testes de Integração da API
- 5.6 Discussão dos Resultados e Limitações

### CAPÍTULO 6 — CONSIDERAÇÕES FINAIS
- 6.1 Conclusões
- 6.2 Contribuições do Trabalho
- 6.3 Trabalhos Futuros (SaaS B2B, CRM, Automações WhatsApp)

### REFERÊNCIAS BIBLIOGRÁFICAS

### APÊNDICES
- Apêndice A — Código-Fonte do Motor de Recomendação
- Apêndice B — Catálogo Completo de Produtos (Matriz de Afinidade)
- Apêndice C — Logs de Execução dos Cenários de Teste

---

## 2. Rascunho da Introdução

### 1.1 Contextualização

O mercado brasileiro de produtos e serviços para cabelos cacheados e crespos vivencia um processo de expansão acelerada, impulsionado pelo movimento de aceitação da textura natural dos fios e pela crescente demanda por atendimento especializado. Nesse contexto, salões como a Vila Cachos — localizada em São Luís do Maranhão e dedicada exclusivamente a cabelos com curvatura (tipos 2, 3 e 4 da escala André Walker) — enfrentam um desafio operacional crítico: a ausência de um histórico digital estruturado de atendimentos e preferências das clientes, condição conhecida na literatura de Sistemas de Recomendação como o problema do *Cold Start* (AGGARWAL, 2016). Sem essa base de dados, as recomendações de produtos e tratamentos permanecem dependentes da experiência individual de cada profissional, gerando inconsistências no atendimento e subutilização do portfólio de cosméticos disponíveis (Arvensis, Curly Care, Deva Curl, entre outros).

### 1.2 Justificativa

A padronização do diagnóstico capilar por meio de Inteligência Artificial representa uma oportunidade concreta de diferenciação competitiva para pequenos e médios salões de beleza especializados. Um sistema inteligente disponibilizado como **Módulo Web de Diagnóstico Integrado** pode (i) reduzir a variabilidade do diagnóstico entre profissionais diferentes, (ii) gerar dados analíticos que alimentem estratégias de estoque e marketing, e (iii) oferecer à cliente uma experiência personalizada e memorável desde o primeiro contato com o salão — mesmo quando ainda não existe nenhum registro histórico sobre ela. Além disso, a capacidade de aprendizado contínuo do sistema, por meio de avaliações pós-atendimento (notas de 1 a 5 estrelas), permite que a qualidade das recomendações evolua organicamente à medida que o salão acumula dados reais, substituindo gradualmente as estimativas iniciais baseadas em conhecimento especialista por evidências empíricas coletivas.

A escolha por uma **arquitetura Web App** — em detrimento de um totem físico de hardware dedicado — foi fundamentada em três critérios arquitetônicos: (1) **Escalabilidade**: o módulo pode ser acessado via link direto integrado ao site oficial do salão (hospedado na Locaweb), eliminando dependências de equipamentos específicos e permitindo acesso tanto no espaço físico do salão quanto de forma remota, por qualquer dispositivo com navegador; (2) **Redução de custos de hardware**: a implantação dispensa investimento em terminais físicos (totens, tablets fixos, cabeamento), reduzindo a barreira financeira de adoção pelo salão; (3) **Manutenibilidade e atualizações contínuas**: evoluções no motor de IA (novas personas, produtos ou pesos) são aplicadas centralmente na API hospedada em nuvem (Render.com), sem necessidade de atualizações em dispositivos físicos distribuídos.

### 1.3 Objetivo Geral

Este trabalho tem como objetivo geral projetar, implementar e validar um Motor Híbrido de Recomendação de produtos e tratamentos capilares que resolva o problema do *Cold Start* em um salão especializado em cabelos cacheados. O sistema combina três camadas complementares: (1) uma camada de **Recomendação Baseada em Conhecimento** (*Knowledge-Based*), fundamentada em uma matriz de afinidade terapêutica entre queixas capilares e formulações cosméticas; (2) uma camada de **Segmentação de Personas** por meio do algoritmo K-Means aplicado a um espaço de 8 variáveis normalizadas; e (3) uma camada de **Aprendizado Contínuo** (*Feedback Loop*) que utiliza Média Bayesiana Amortecida para recalibrar os pesos das recomendações com base na satisfação explícita das clientes, evitando distorções estatísticas causadas por amostras pequenas. O motor é exposto por meio de uma API RESTful (FastAPI) e consumido por um **Web App de Diagnóstico Integrado** (React, hospedado na Vercel e acessível via link no site do salão) que fornece justificativas explicáveis (XAI) para cada recomendação gerada.

---

## 3. Roteiro Estratégico da Apresentação de Defesa (5 Slides-Chave)

> Os itens abaixo são os **5 blocos temáticos** que devem estruturar a apresentação. Cada bloco pode ocupar de 2 a 4 slides na prática (totalizando 12 a 18 slides, duração de ~15 a 20 minutos).

---

### Slide 1 — O Problema e a Oportunidade de Negócio
**O que mostrar:**
- Foto/identidade visual do salão Vila Cachos (humaniza o problema).
- Estatística rápida: "Um salão com 4 profissionais e 30+ produtos pode gerar recomendações inconsistentes dependendo de quem atende."
- Definição acessível de **Cold Start**: "E se a cliente nunca veio ao salão antes? Como recomendar sem dados?"
- Slide de impacto: transição do "achismo" para a inteligência de dados.

**Por que impressiona a banca:** Demonstra que o TCC resolve um problema real de mercado, não é apenas um exercício acadêmico.

---

### Slide 2 — Arquitetura Híbrida do Motor (O Diferencial Técnico)
**O que mostrar:**
- Diagrama visual das 3 camadas: Knowledge-Based → K-Means Clustering → Feedback Bayesiano.
- A fórmula da Mistura Convexa: S_final = (1-α) · S_conteúdo + α · S_bayesiano.
- Destaque que o peso α cresce automaticamente à medida que o cluster acumula avaliações (o sistema "amadurece").
- Slide comparativo: "O que aconteceria com uma média simples vs. a Média Bayesiana Amortecida" (1 avaliação nota 5 vs. 50 avaliações com média 4.8).

**Por que impressiona a banca:** Mostra domínio teórico sólido (Bayes, K-Means, XAI) aplicado a um cenário prático original.

---

### Slide 3 — Demonstração ao Vivo do MVP (Web App + API)
**O que mostrar:**
- Gravação de tela ou demo ao vivo: abrir o **Web App de Diagnóstico** no navegador (link da Vercel integrado ao site da Vila Cachos), preencher o wizard (Curvatura → Porosidade → Química → Queixas) e mostrar o Top 3 com justificativas.
- Mostrar o Swagger UI (/docs) com o contrato da API hospedada no Render.
- Clicar no feedback de 5 estrelas e mostrar que a base foi atualizada em tempo real.
- Destacar a arquitetura sem hardware físico: cliente acessa pelo celular ou computador via link no site da Locaweb.

**Por que impressiona a banca:** Prova que não é só teoria — o sistema funciona de ponta a ponta em produção real (Vercel + Render), do input da cliente até a calibração automática. Defesas com demonstração ao vivo se destacam.

---

### Slide 4 — Resultados Quantitativos e Validação Científica
**O que mostrar:**
- Tabela dos 4 cenários clínicos com os produtos recomendados, scores e justificativas.
- Gráfico do Silhouette Score validando a qualidade da clusterização.
- Curva de convergência do Feedback Loop: score antes vs. depois de N avaliações.
- Métricas formais (se aplicável): Precision@K, MAP simulado.

**Por que impressiona a banca:** Evidências empíricas com métricas reconhecidas pela comunidade de ML. Transforma uma PoC em pesquisa aplicada defensável.

---

### Slide 5 — Contribuições, Limitações e Trabalhos Futuros
**O que mostrar:**
- **Contribuições**: (1) Motor híbrido original para domínio cosmético capilar; (2) Gerador sintético com causalidade para cenários de Cold Start; (3) Feedback Loop com calibração bayesiana integrada.
- **Limitações honestas**: Dados sintéticos (ainda não validados com clientes reais); número fixo de clusters (k=4); catálogo limitado a 6 produtos.
- **Visão de Futuro**: SaaS B2B para outros salões, CRM integrado, automação de WhatsApp para pesquisas de satisfação, incorporação de dados reais.

**Por que impressiona a banca:** Demonstra maturidade acadêmica ao reconhecer limitações e visão de engenharia ao projetar a evolução do sistema.

---

### Dica de Ouro para a Defesa

A banca irá perguntar "Por que K-Means e não DBSCAN?" ou "Por que não usou Redes Neurais?". Prepare respostas claras:

- **K-Means**: Escolhido pela interpretabilidade das personas (centróides legíveis) e pela natureza ordinal/categórica das variáveis com encoding adequado. Em cenário de Cold Start com poucos dados, modelos simples e explicáveis são preferíveis a black-boxes.
- **Média Bayesiana vs. Média Simples**: A média simples é vulnerável a outliers e amostras pequenas. A bayesiana converge para a evidência empírica conforme n cresce, mas protege o sistema no início com uma estimativa conservadora.
