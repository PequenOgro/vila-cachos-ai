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
- 4.5 Requisitos Não-Funcionais
  - 4.5.1 Segurança e Proteção contra Abusos
  - 4.5.2 Usabilidade e Acessibilidade

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

---

## 2.1 Requisitos Não-Funcionais (Seção 4.5 — Texto Completo)

### 4.5.1 Segurança e Proteção contra Abusos

A exposição pública de uma API RESTful na internet — acessível a qualquer cliente que possua o endereço do *endpoint* — introduz vetores de ataque que, embora não visem à extração de dados sensíveis (o sistema não armazena informações pessoais identificáveis), podem comprometer a **disponibilidade** do serviço e consumir os recursos computacionais limitados da camada de hospedagem gratuita (Render.com, plano *free tier*). Para mitigar esse risco, foi implementado um mecanismo de **Rate Limiting** (limitação de taxa de requisições) por meio da biblioteca *SlowAPI* (wrapper da biblioteca *limits* para FastAPI). As rotas críticas da API — `/recommend` (geração de recomendações) e `/feedback` (registro de avaliações) — foram configuradas com um limite máximo de **10 requisições por minuto por endereço IP**. Requisições excedentes recebem uma resposta padronizada HTTP 429 (*Too Many Requests*), informando o tempo de espera necessário para nova tentativa. Essa medida protege o sistema contra ataques de negação de serviço (*Denial of Service — DoS*) de baixa complexidade e contra usos abusivos automatizados (bots, *web scrapers*) que poderiam esgotar a cota de processamento do servidor.

Adicionalmente, foram adotadas práticas de **sanitização do console do navegador**: mensagens de depuração (*debug logs*), *stack traces* e informações internas da aplicação foram removidas ou suprimidas no ambiente de produção, impedindo que usuários com conhecimento técnico inspecionem detalhes de implementação da lógica de recomendação ou da estrutura interna da API por meio das ferramentas de desenvolvimento do navegador (*DevTools*). A configuração de CORS (*Cross-Origin Resource Sharing*) foi mantida com `allow_origins=["*"]` durante a fase de homologação, com planejamento de restrição para o domínio específico do salão (Locaweb) após a integração definitiva.

### 4.5.2 Usabilidade e Acessibilidade

Dois requisitos não-funcionais de usabilidade foram implementados no front-end para atender às especificidades do contexto de uso — um salão de beleza com múltiplas clientes acessando o sistema de diagnóstico sequencialmente ao longo do dia:

**a) Suporte nativo a Tema Escuro (*Dark Mode*)**

A interface do Web App implementa suporte a duas paletas visuais — clara e escura — alternáveis por meio de um botão de *toggle* posicionado no cabeçalho da aplicação (ícones de Sol/Lua, providos pela biblioteca Lucide React). A implementação utiliza a estratégia `darkMode: 'class'` do Tailwind CSS, na qual a classe `dark` é adicionada ou removida programaticamente do elemento `<html>` via manipulação do DOM (`document.documentElement.classList`). Cada elemento visual da interface possui classes duplicadas — a variante padrão (clara) e sua correspondente prefixada com `dark:` — garantindo uma transição completa e sem inconsistências visuais. A motivação para essa funcionalidade transcende a preferência estética: em ambientes com iluminação controlada (como estações de atendimento em salões), telas com fundo escuro reduzem o ofuscamento e a fadiga visual (LEGGE; BIGELOW, 2011), melhorando a experiência tanto do profissional quanto da cliente durante a interação com o diagnóstico.

**b) Gestão de Sessão Inativa (*Inactivity Timeout*)**

O sistema implementa um mecanismo de *timeout* por inatividade com duração configurada de **15 minutos (900.000 milissegundos)**. A lógica, implementada como um *hook* `useEffect` global no componente raiz da aplicação React, monitora continuamente quatro tipos de eventos de interação do usuário: `click`, `touchstart`, `mousemove` e `keydown`. A cada evento detectado, um temporizador interno (`setTimeout`) é reiniciado. Caso nenhum desses eventos seja disparado dentro da janela de 15 minutos — indicando que a cliente abandonou o formulário ou foi atendida sem finalizar o diagnóstico —, o sistema executa automaticamente a função de *reset* do estado, retornando a aplicação à tela inicial (*welcome*) e limpando todos os dados do formulário preenchido. Essa funcionalidade atende a dois requisitos operacionais: (i) **privacidade**, ao garantir que dados parciais de uma anamnese abandonada não sejam visualizados pela próxima cliente que acessar o sistema; e (ii) **continuidade de atendimento**, ao apresentar sempre uma interface limpa e pronta para um novo diagnóstico, sem necessidade de intervenção manual do profissional.

---

## 2.2 Placeholders de Figuras e Análise Técnica (Capítulo 5 — Resultados)

Os parágrafos a seguir devem ser inseridos no corpo do Capítulo 5 da monografia, nas subseções correspondentes, acompanhados das respectivas figuras geradas pelo script `plot_metrics.py`.

### 5.2.2 — Método do Cotovelo para Escolha de *k*

**[INSERIR AQUI: fig_elbow_method.png]**

> **Figura X** — Método do Cotovelo (*Elbow Method*): Inércia intra-cluster (WCSS) em função do número de clusters (*k*), para *k* ∈ {2, 3, ..., 10}.

A Figura X apresenta a aplicação do Método do Cotovelo (*Elbow Method*) para a determinação do número ótimo de agrupamentos (*k*) no algoritmo K-Means. O eixo vertical representa a Inércia (*Within-Cluster Sum of Squares* — WCSS), definida como o somatório das distâncias euclidianas quadráticas de cada observação ao centróide do cluster ao qual foi atribuída: $W = \sum_{j=1}^{k} \sum_{x_i \in C_j} ||x_i - \mu_j||^2$. Valores elevados de inércia indicam clusters internamente dispersos, ao passo que a redução de $W$ com o incremento de $k$ sinaliza ganhos de coesão interna. O critério do "cotovelo" consiste em identificar o ponto de inflexão da curva — o valor de $k$ a partir do qual incrementos adicionais produzem reduções marginais de inércia, sugerindo que a adição de novos clusters não captura estrutura significativa adicional nos dados. No gráfico obtido, observa-se uma inflexão pronunciada em $k = 4$, que foi adotado como o número de clusters operacionais do motor de recomendação. Esse valor equilibra a granularidade das personas identificadas (suficiente para capturar os principais perfis capilares do salão) com a parcimônia do modelo (evitando *overfitting* a ruído nos dados sintéticos).

### 5.2.1 — Coeficiente Silhouette e Validação Interna

**[INSERIR AQUI: fig_silhouette.png]**

> **Figura Y** — Coeficiente Silhouette por número de clusters (*k*), para *k* ∈ {2, 3, ..., 10}.

A Figura Y apresenta a variação do Coeficiente Silhouette em função do número de clusters. O Coeficiente Silhouette, definido formalmente como $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$ — onde $a(i)$ é a distância média intra-cluster da observação $i$ e $b(i)$ é a distância média ao cluster vizinho mais próximo —, varia no intervalo $[-1, 1]$, sendo que valores próximos de 1 indicam clusters coesos e bem separados, valores próximos de 0 indicam sobreposição entre agrupamentos, e valores negativos indicam atribuições incorretas. O valor obtido para $k = 4$ foi de **0,2185**. Embora esse coeficiente esteja na faixa classificada como "estrutura fraca" pela taxonomia de Kaufman e Rousseeuw (1990), é fundamental contextualizar esse resultado à luz das características do domínio: as variáveis capilares utilizadas (curvatura, porosidade, dano químico e 5 indicadores binários de queixas) são de natureza **ordinal e categórica codificada**, o que introduz uma granularidade discreta que limita naturalmente a separabilidade geométrica dos agrupamentos em espaço euclidiano contínuo. Adicionalmente, a sobreposição entre personas é **esperada clinicamente** — uma cliente cacheada com alta porosidade química pode compartilhar queixas com uma crespa em transição capilar —, o que reforça a validade ecológica do agrupamento obtido. Valores de Silhouette entre 0,15 e 0,30 são reportados com frequência na literatura de clusterização aplicada a dados categóricos de saúde e beleza (TAN; STEINBACH; KUMAR, 2019), confirmando a adequação do modelo para o propósito de segmentação de personas neste domínio.

### 5.4 — Demonstração do Feedback Loop (Convergência Bayesiana)

**[INSERIR AQUI: fig_bayesian_feedback.png]**

> **Figura Z** — Convergência da Média Bayesiana Amortecida vs. Média Simples ao longo de *n* avaliações, para um produto hipotético com nota real convergente de 4,2 e constante de amortecimento $C = 10$.

A Figura Z ilustra o comportamento comparativo da Média Bayesiana Amortecida (*Damped Bayesian Average*) frente à média aritmética simples ao longo de uma sequência crescente de avaliações de satisfação (1 a 5 estrelas). A formulação bayesiana utilizada neste trabalho é dada por: $\bar{x}_{bayes} = \frac{C \cdot \mu_{global} + n \cdot \bar{x}_{local}}{C + n}$, onde $C$ é a constante de amortecimento (definida como $C = 10$ neste sistema), $\mu_{global}$ é a média global de satisfação de todo o salão (calculada sobre o dataset histórico), $n$ é o número de avaliações acumuladas pelo cluster para o produto em questão, e $\bar{x}_{local}$ é a média aritmética simples dessas $n$ avaliações. A principal vantagem dessa formulação é evidente nas fases iniciais do gráfico ($n < C$): enquanto a média simples oscila violentamente com cada nova avaliação (uma única nota 5 geraria uma média de 5,0; seguida de uma nota 1, cairia para 3,0), a média bayesiana permanece ancorada à estimativa conservadora da média global do salão, resistindo a flutuações espúrias. Conforme $n$ cresce e ultrapassa $C$, o peso da evidência empírica local ($\bar{x}_{local}$) supera gradualmente o peso do *prior* bayesiano ($\mu_{global}$), e a curva converge para o valor real de satisfação. Esse mecanismo garante que o motor de recomendação não realize ajustes precipitados em seus *rankings* baseados em amostras insuficientes, preservando a estabilidade e a confiabilidade das sugestões oferecidas às clientes especialmente durante o período de *Cold Start* do sistema.

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

## 2. Texto da Introdução (Capítulo 1)

### 1.1 Contextualização

O setor brasileiro de beleza e cuidados pessoais configura-se, historicamente, como um dos mais expressivos do mundo, ocupando a quarta posição no ranking global segundo dados da Associação Brasileira da Indústria de Higiene Pessoal, Perfumaria e Cosméticos — ABIHPEC (2024). Dentro desse macrossetor, o segmento voltado a cabelos cacheados e crespos experimenta um crescimento particularmente acelerado, impulsionado pelo movimento sociocultural de valorização da textura natural dos fios — frequentemente referido como *transição capilar* — e pela consequente proliferação de salões especializados, linhas cosméticas dedicadas e conteúdo técnico-educacional em plataformas digitais (SANTOS; OLIVEIRA, 2021). Nesse contexto de expansão, a digitalização dos processos de atendimento em salões de beleza emerge como um vetor estratégico de diferenciação competitiva, possibilitando a transição de diagnósticos capilares baseados exclusivamente na percepção empírica do profissional para abordagens sistematizadas, replicáveis e fundamentadas em dados estruturados. Contudo, essa transição esbarra em obstáculos concretos: a maioria dos salões de pequeno e médio porte carece de infraestrutura tecnológica, de bases de dados históricas sobre suas clientes e de ferramentas computacionais capazes de transformar informações clínico-capilares em recomendações acionáveis de produtos e tratamentos.

O salão Vila Cachos, localizado em São Luís do Maranhão e dedicado exclusivamente ao atendimento de cabelos com curvatura (tipos 2, 3 e 4 da escala de classificação de André Walker), exemplifica com precisão esse cenário. Com um portfólio de cosméticos profissionais que inclui linhas como Arvensis, Curly Care e similares, o estabelecimento dispõe de diversas formulações terapêuticas voltadas a queixas capilares específicas — desde ressecamento e alta porosidade pós-química até frizz excessivo e sensibilidade do couro cabeludo. Entretanto, a ausência de um histórico digital estruturado de atendimentos, preferências e avaliações das clientes configura o que a literatura de Sistemas de Recomendação denomina como o problema do *Cold Start* (AGGARWAL, 2016): a incapacidade de um sistema fornecer sugestões personalizadas quando não há dados prévios disponíveis sobre o usuário ou sobre o item a ser recomendado. Na prática operacional do salão, essa lacuna se traduz em recomendações dependentes da experiência individual e da memória de cada profissional, resultando em inconsistências de atendimento entre profissionais distintos, subutilização do catálogo de produtos disponíveis e perda de oportunidades de fidelização baseadas em personalização.

Diante desse problema, este trabalho propõe a concepção, implementação e validação de um **Web App de Diagnóstico Capilar Integrado**, disponibilizado como módulo acessível diretamente via link no site oficial do salão, que emprega um Motor Híbrido de Recomendação baseado em Inteligência Artificial para automatizar e padronizar o processo de triagem e sugestão de produtos. O motor combina três camadas computacionais complementares: (i) uma camada de **Recomendação Baseada em Conhecimento** (*Knowledge-Based*), fundamentada em uma matriz de afinidade terapêutica entre queixas capilares e composições cosméticas, construída em colaboração com o proprietário do salão; (ii) uma camada de **Segmentação de Personas** via algoritmo K-Means aplicado a um espaço vetorial de 8 dimensões normalizadas, que identifica perfis comportamentais recorrentes entre as clientes; e (iii) uma camada de **Aprendizado Contínuo** (*Feedback Loop*) que utiliza Média Bayesiana Amortecida (*Damped Bayesian Average*) para recalibrar dinamicamente os pesos das recomendações com base na satisfação explícita das clientes, prevenindo distorções estatísticas inerentes a amostras de tamanho reduzido. Para mitigar o problema do *Cold Start*, o sistema emprega um gerador de dados sintéticos com causalidade probabilística, simulando um histórico realista de 1.000 atendimentos que reflete as correlações reais do domínio capilar (e.g., a relação causal entre histórico de tratamentos químicos e alta porosidade dos fios).

A solução é exposta por meio de uma API RESTful construída com o framework FastAPI (Python) e consumida por uma interface web responsiva desenvolvida em React com Vite e Tailwind CSS, hospedada na plataforma Vercel. A arquitetura Web App foi deliberadamente escolhida em detrimento de um totem físico de hardware dedicado por três razões fundamentais: (1) **escalabilidade**, ao permitir que o módulo seja acessado por qualquer dispositivo com navegador — inclusive celulares das próprias clientes —, eliminando dependências de equipamentos proprietários; (2) **redução de custos de implantação**, ao dispensar investimentos em terminais físicos, cabeamento e manutenção de hardware; e (3) **manutenibilidade centralizada**, ao possibilitar que evoluções no motor de IA (novas personas, novos produtos, recalibrações de pesos) sejam aplicadas centralmente na API em nuvem (Render.com), sem necessidade de intervenções em dispositivos distribuídos. Cada recomendação gerada é acompanhada de justificativas explicáveis (*Explainable AI — XAI*), promovendo transparência algorítmica e fortalecendo a confiança do profissional e da cliente no sistema.

### 1.2 Justificativa

A padronização do diagnóstico capilar por meio de Inteligência Artificial representa uma oportunidade concreta de diferenciação competitiva para pequenos e médios salões de beleza especializados. Um sistema inteligente disponibilizado como Módulo Web de Diagnóstico Integrado pode (i) reduzir a variabilidade do diagnóstico entre profissionais diferentes, (ii) gerar dados analíticos que alimentem estratégias de estoque e marketing, e (iii) oferecer à cliente uma experiência personalizada e memorável desde o primeiro contato com o salão — mesmo quando ainda não existe nenhum registro histórico sobre ela. Além disso, a capacidade de aprendizado contínuo do sistema, por meio de avaliações pós-atendimento (notas de 1 a 5 estrelas), permite que a qualidade das recomendações evolua organicamente à medida que o salão acumula dados reais, substituindo gradualmente as estimativas iniciais baseadas em conhecimento especialista por evidências empíricas coletivas.

A escolha por uma arquitetura Web App — em detrimento de um totem físico de hardware dedicado — foi fundamentada em três critérios arquitetônicos: (1) **Escalabilidade**: o módulo pode ser acessado via link direto integrado ao site oficial do salão (hospedado na Locaweb), eliminando dependências de equipamentos específicos e permitindo acesso tanto no espaço físico do salão quanto de forma remota, por qualquer dispositivo com navegador; (2) **Redução de custos de hardware**: a implantação dispensa investimento em terminais físicos (totens, tablets fixos, cabeamento), reduzindo a barreira financeira de adoção pelo salão; (3) **Manutenibilidade e atualizações contínuas**: evoluções no motor de IA (novas personas, produtos ou pesos) são aplicadas centralmente na API hospedada em nuvem (Render.com), sem necessidade de atualizações em dispositivos físicos distribuídos.

### 1.3 Objetivo Geral

Este trabalho tem como objetivo geral projetar, implementar e validar um Motor Híbrido de Recomendação de produtos e tratamentos capilares que resolva o problema do *Cold Start* em um salão especializado em cabelos cacheados. O sistema combina três camadas complementares: (1) uma camada de Recomendação Baseada em Conhecimento (*Knowledge-Based*), fundamentada em uma matriz de afinidade terapêutica entre queixas capilares e formulações cosméticas; (2) uma camada de Segmentação de Personas por meio do algoritmo K-Means aplicado a um espaço de 8 variáveis normalizadas; e (3) uma camada de Aprendizado Contínuo (*Feedback Loop*) que utiliza Média Bayesiana Amortecida para recalibrar os pesos das recomendações com base na satisfação explícita das clientes, evitando distorções estatísticas causadas por amostras pequenas. O motor é exposto por meio de uma API RESTful (FastAPI) e consumido por um Web App de Diagnóstico Integrado (React, hospedado na Vercel e acessível via link no site do salão) que fornece justificativas explicáveis (XAI) para cada recomendação gerada.

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
