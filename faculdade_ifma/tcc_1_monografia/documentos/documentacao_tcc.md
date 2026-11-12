# Documentação Acadêmica — TCC Sistemas de Informação (IFMA)

**Título Proposto:**
> *Sistema Híbrido de Recomendação de Produtos Capilares com Feedback Loop Bayesiano: Uma Solução para o Problema do Cold Start em Salões Especializados*

---

## CAPÍTULO 1 — INTRODUÇÃO

O setor brasileiro de beleza e cuidados pessoais configura-se, historicamente, como um dos mais expressivos do mundo, ocupando a quarta posição no ranking global segundo dados da Associação Brasileira da Indústria de Higiene Pessoal, Perfumaria e Cosméticos — ABIHPEC (2024). Dentro desse macrossetor, o segmento voltado a cabelos cacheados e crespos experimenta um crescimento particularmente acelerado, impulsionado pelo movimento sociocultural de valorização da textura natural dos fios — frequentemente referido como *transição capilar* — e pela consequente proliferação de salões especializados, linhas cosméticas dedicadas e conteúdo técnico-educacional em plataformas digitais (SANTOS; OLIVEIRA, 2021). Nesse contexto de expansão, a digitalização dos processos de atendimento em salões de beleza emerge como um vetor estratégico de diferenciação competitiva, possibilitando a transição de diagnósticos capilares baseados exclusivamente na percepção empírica do profissional para abordagens sistematizadas, replicáveis e fundamentadas em dados estruturados. Contudo, essa transição esbarra em obstáculos concretos: a maioria dos salões de pequeno e médio porte carece de infraestrutura tecnológica, de bases de dados históricas sobre suas clientes e de ferramentas computacionais capazes de transformar informações clínico-capilares em recomendações acionáveis de produtos e tratamentos.

O salão Vila Cachos, localizado em São Luís do Maranhão e dedicado exclusivamente ao atendimento de cabelos com curvatura (tipos 2, 3 e 4 da escala de classificação de André Walker), exemplifica com precisão esse cenário. Com um portfólio de cosméticos profissionais que inclui linhas como Arvensis, Curly Care e similares, o estabelecimento dispõe de diversas formulações terapêuticas voltadas a queixas capilares específicas — desde ressecamento e alta porosidade pós-química até frizz excessivo e sensibilidade do couro cabeludo. Entretanto, a ausência de um histórico digital estruturado de atendimentos, preferências e avaliações das clientes configura o que a literatura de Sistemas de Recomendação denomina como o problema do *Cold Start* (AGGARWAL, 2016): a incapacidade de um sistema fornecer sugestões personalizadas quando não há dados prévios disponíveis sobre o usuário ou sobre o item a ser recomendado. Na prática operacional do salão, essa lacuna se traduz em recomendações dependentes da experiência individual e da memória de cada profissional, resultando em inconsistências de atendimento entre profissionais distintos, subutilização do catálogo de produtos disponíveis e perda de oportunidades de fidelização baseadas em personalização.

Diante desse problema, este trabalho propõe a concepção, implementação e validação de um Web App de Diagnóstico Capilar Integrado, disponibilizado como módulo acessível diretamente via link no site oficial do salão, que emprega um Motor Híbrido de Recomendação baseado em Inteligência Artificial para automatizar e padronizar o processo de triagem e sugestão de produtos. O motor combina três camadas computacionais complementares: (i) uma camada de Recomendação Baseada em Conhecimento (*Knowledge-Based*); (ii) uma camada de Segmentação de Personas via algoritmo K-Means aplicado a um espaço vetorial de 8 dimensões normalizadas; e (iii) uma camada de Aprendizado Contínuo (*Feedback Loop*) que utiliza Média Bayesiana Amortecida (*Damped Bayesian Average*). Para mitigar o problema do *Cold Start*, o sistema emprega um gerador de dados sintéticos com causalidade probabilística, simulando um histórico realista de 1.000 atendimentos.

A solução é exposta por meio de uma API RESTful construída com o framework FastAPI (Python) e consumida por uma interface web responsiva desenvolvida em React com Vite e Tailwind CSS, hospedada na plataforma Vercel. A arquitetura Web App foi deliberadamente escolhida em detrimento de um totem físico de hardware dedicado por três razões fundamentais: (1) escalabilidade; (2) redução de custos de implantação; e (3) manutenibilidade centralizada em nuvem (Render.com).

### 1.1 OBJETIVOS E JUSTIFICATIVA

A padronização do diagnóstico capilar por meio de Inteligência Artificial representa uma oportunidade concreta de diferenciação competitiva para pequenos e médios salões de beleza especializados. Um sistema inteligente disponibilizado como Módulo Web de Diagnóstico Integrado pode (i) reduzir a variabilidade do diagnóstico entre profissionais diferentes, (ii) gerar dados analíticos que alimentem estratégias de estoque e marketing, e (iii) oferecer à cliente uma experiência personalizada e memorável desde o primeiro contato com o salão — mesmo quando ainda não existe nenhum registro histórico sobre ela. Além disso, a capacidade de aprendizado contínuo do sistema, por meio de avaliações pós-atendimento, permite que a qualidade das recomendações evolua organicamente à medida que o salão acumula dados reais.

#### 1.1.1 Objetivo Geral
Compreender e mitigar o problema do *Cold Start* em salões especializados por meio do projeto, implementação e validação de um Motor Híbrido de Recomendação capilar integrado a um Web App de Diagnóstico para o salão Vila Cachos.

#### 1.1.2 Objetivos Específicos
*   Modelar a taxonomia do domínio capilar (escala de André Walker como *ground truth* para curvaturas 2A a 4C), criando uma matriz de afinidade terapêutica entre queixas e produtos.
*   Integrar módulo de visão computacional (YOLOv8/11 com *Transfer Learning* e *Data Augmentation*) para inferência determinística de curvatura e frizz a partir de fotos de mechas.
*   Desenvolver algoritmo de clusterização (K-Means) para segmentar o espaço vetorial de 8 dimensões de fusão multimodal e aplicar Feedback Loop com Média Bayesiana Amortecida.
*   Construir e implantar uma interface web (React) e uma API RESTful (FastAPI) com suporte a justificativas explicáveis (XAI).
*   Garantir Requisitos Não-Funcionais adequados para ambientes corporativos (Rate Limiting, Dark Mode, Sessão Inativa, gestão de memória sob 512 MB).
*   Avaliar os resultados gerados pela clusterização metricamente (Inércia, Silhouette Score, Método do Cotovelo).

---

## CAPÍTULO 2 — REFERENCIAL TEÓRICO E TRABALHOS CORRELATOS

### 2.5 VISÃO COMPUTACIONAL E RECONHECIMENTO DE PADRÕES CAPILARES
A caracterização morfológica da fibra capilar na ciência cosmética contemporânea adota universalmente a taxonomia proposta por Andre Walker (1997) como verdade fundamental (*ground truth*), estruturada em quatro tipos (1 a 4 com subdivisões A, B e C). Para contornar a escassez de bases volumosas no nicho capilar e a restrição orçamentária do salão, adota-se *Transfer Learning* com redes da família YOLO (Ultralytics YOLOv8/11), aliada a técnicas de *Data Augmentation* (rotação, corte, variação de brilho e ruído gaussiano) para prevenir sobreajuste a fundos ou marcas d'água de postagens de redes sociais.

O sistema adota o paradigma de **Fusão Multimodal de Características (*Multimodal Feature Fusion*)**: os atributos visuais determinísticos (curvatura e frizz extraídos pela rede neural) fundem-se às variáveis clínicas tabulares (porosidade, histórico de química transformadora, densidade e queixa principal coletadas na anamnese). Essa união gera um vetor de 8 dimensões normalizado via `StandardScaler`, que alimenta diretamente o espaço euclidiano do K-Means, blindando o diagnóstico contra alterações cosméticas superficiais.

### 2.6 TRABALHOS CORRELATOS E MATRIZ COMPARATIVA
O cenário tecnológico divide-se entre sistemas proprietários industriais e pesquisas acadêmicas isoladas:
1. **Soluções Comerciais BeautyTech:** 
   - *Perfect Corp (AI Hair Type Detection API)*: API B2B que exige 3 fotos angulares distintas (frente e laterais 45º) sem motor de recomendação embutido e a alto custo de licenciamento;
   - *Zenvy Beauty (AI Curl Identifier)*: Web app baseado em LLM multimodal (Claude 3.5 Sonnet) com foto única, vulnerável a custos recorrentes por requisição e alucinações de formulação química;
   - *Kérastase K-Scan (L'Oréal)*: Câmera com luzes UV e LED (12.000 imagens) associada a iPad, excelente em diagnóstico tricológico, mas com custo proibitivo de hardware proprietário para pequenos salões;
   - *MYAVANA (HairAI/MyHairID)*: IA e microscopia capilar laboratorial com catálogo validado, demandando envio físico de mechas pelo correio;
   - *HairDays / OurX / Curltine*: Aplicativos móveis dependentes de formulários manuais longos sem visão computacional integrada.
2. **Baselines Acadêmicos e Repositórios:**
   - *Hairmony (Meishvili et al., 2024)*: Classificação justa de curvaturas 1 a 4 com CNNs e dados sintéticos, sem camada de recomendação cosmética;
   - *PERM (He et al., 2024)*: Modelagem da geometria 3D separando volume global de padrão local de cacho via PCA;
   - *Three-Stage Hybrid Recommender (Haloho & Liao, 2026 - Springer)*: Recomendador cosmético híbrido em três estágios para rotinas tópicas dermatológicas;
   - *Hair-Type-Classifier (Kavya-sree, 2023)*: ResNet18 com Transfer Learning (88% de acurácia) para classificação visual pura.

| Trabalho / Sistema | Visão Computacional | Motor Híbrido | Mitigação Cold Start | Foco Cabelos 2A–4C | Arquitetura |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kavya-sree (GitHub)** | Sim (ResNet18) | Não | Não | Parcial | Script Python / Notebook |
| **Hairmony (2024)** | Sim (CNN) | Não | Parcial (Sintéticos) | Sim | Modelo de Pesquisa |
| **Haloho & Liao (2026)** | Não | Sim (3 Estágios) | Sim (Conteúdo) | Não (Pele) | Regras + Cosseno |
| **Perfect Corp API** | Sim (3 Ângulos) | Não | Não | Sim (Geral) | API B2B Proprietária |
| **Zenvy Beauty** | Sim (LLM Sonnet) | Baseado em Regras | Não formal | Sim | Web / Cloud Generativa |
| **Kérastase K-Scan** | Sim (Hardware UV) | Sim (Catálogo) | Não | Geral | Hardware Proprietário + iPad |
| **Vila Cachos AI (Este TCC)** | **Sim (YOLOv8/11)** | **Sim (K-Means + Regras)** | **Sim (Bayes + Mock Causal)** | **Sim (Especializado)** | **Web App Leve (FastAPI + React)** |

**Vantagem Competitiva:** Conexão pioneira da visão computacional com o espaço euclidiano do K-Means e estabilização de longo prazo pela Média Bayesiana Amortecida, dispensando hardware proprietário e assinaturas de APIs onerosas.

---

## CAPÍTULO 4 — DESENVOLVIMENTO DO SISTEMA

### 4.5 REQUISITOS NÃO-FUNCIONAIS

#### 4.5.1 Segurança e Proteção contra Abusos
Para mitigar riscos de disponibilidade em nossa hospedagem gratuita (Render.com), foi implementado um mecanismo de **Rate Limiting** por meio da biblioteca *SlowAPI*. As rotas críticas da API (`/recommend` e `/feedback`) foram configuradas com um limite máximo de 10 requisições por minuto por endereço IP. Requisições excedentes recebem uma resposta HTTP 429 (*Too Many Requests*). Adicionalmente, foram adotadas práticas de **sanitização do console do navegador**, removendo logs de depuração no ambiente de produção.

#### 4.5.2 Usabilidade e Acessibilidade
**a) Suporte nativo a Tema Escuro (Dark Mode)**
Implementação baseada na estratégia `darkMode: 'class'` do Tailwind CSS, alternável via interface. Em ambientes com iluminação controlada (salões), telas com fundo escuro reduzem o ofuscamento e a fadiga visual.

**b) Gestão de Sessão Inativa (Inactivity Timeout)**
Mecanismo de *timeout* com duração de 15 minutos. A lógica global no componente React reinicia o *timer* a cada interação. Caso ocioso, o sistema executa o *reset* do estado para a tela inicial, garantindo privacidade de dados e continuidade de atendimento.

### 4.6 ARQUITETURA DE CLASSIFICAÇÃO DE 4 CLASSES E INFERÊNCIA LEVE EM NUVEM (GREEN AI)

#### 4.6.1 Eliminação de Outliers e Classe Negativa (`careca_sem_cabelo`)
Nos primeiros ciclos de teste em produção, identificou-se uma vulnerabilidade típica de classificadores fechados: ao receber fotografias de pessoas calvas com barba espessa ou objetos cotidianos, o modelo forçava uma predição em uma das três classes de curvatura (2, 3 ou 4), frequentemente atribuindo alta confiança de cacho devido à densidade de bordas da barba. Para solucionar essa limitação, a arquitetura foi expandida para 4 classes:
1. `careca_sem_cabelo` (Classe negativa de controle: calvície, ausência de fios e imagens não capilares);
2. `tipo_2_ondulado`;
3. `tipo_3_cacheado`;
4. `tipo_4_crespo`.

O pipeline foi dotado de dupla proteção: (i) pré-filtragem anatômica no espaço de cores HSV avaliando a proporção de tons dérmicos no topo craniano versus densidade de mechas; e (ii) inferência neural direta. Se a probabilidade da classe negativa for superior a 20% ou se a imagem for ambígua, o sistema aborta a rotulagem automática, emitindo um alerta explicativo e acionando o padrão *Human-in-the-Loop* para seleção manual pela cliente.

#### 4.6.2 Eficiência Computacional: Migração PyTorch para ONNX Runtime
Em virtude das restrições operacionais de servidores de nuvem gratuitos (teto estrito de 512 MB de RAM no Render.com), o uso do framework PyTorch tradicional provocava risco iminente de *Out of Memory* (consumo basal de ~400 MB). Para viabilizar a sustentabilidade operacional (*Green AI*), os pesos treinados do YOLOv8 foram convertidos para o formato aberto **ONNX** (*Open Neural Network Exchange*). A inferência com a biblioteca `onnxruntime`:
* Reduziu a ocupação de memória RAM para apenas **~25 MB** (redução de 93,7%);
* Atingiu latência média de inferência de **12 ms em CPU** padrão;
* Eliminou qualquer dependência pesada de CUDA ou compiladores de aprendizado profundo em ambiente de produção.

---

## CAPÍTULO 5 — RESULTADOS E DISCUSSÃO

### 5.2.1 Coeficiente Silhouette e Validação Interna

![Coeficiente Silhouette](fig_silhouette.png)
*Figura 1 — Coeficiente Silhouette por número de clusters (k).*

O valor obtido para $k = 4$ foi de 0,2185. Embora classificado como "estrutura fraca" pela taxonomia convencional, as variáveis capilares utilizadas são de natureza ordinal e categórica codificada, limitando a separabilidade geométrica. A sobreposição entre personas é esperada clinicamente (ex: alta porosidade química compartilhada em diferentes curvaturas), reforçando a validade ecológica do agrupamento.

### 5.2.2 Método do Cotovelo para Escolha de *k*

![Método do Cotovelo](fig_elbow_method.png)
*Figura 2 — Inércia intra-cluster (WCSS) em função do número de clusters (k).*

Observa-se uma inflexão pronunciada em $k = 4$, adotado como o número de clusters operacionais do motor. Esse valor equilibra a granularidade das personas com a parcimônia do modelo, evitando *overfitting* aos dados sintéticos causais.

### 5.4 Demonstração do Feedback Loop (Convergência Bayesiana)

![Convergência Bayesiana](fig_bayesian_feedback.png)
*Figura 3 — Convergência da Média Bayesiana Amortecida vs. Média Simples.*

Nas fases iniciais ($n < C$), enquanto a média simples oscila violentamente, a média bayesiana permanece ancorada à estimativa conservadora global ($C = 10$). Conforme $n$ cresce, a curva converge para a evidência empírica, prevenindo ajustes precipitados nos *rankings* durante o período de *Cold Start*.

### 5.5 Validação Experimental da Visão Computacional (Matriz de Confusão YOLOv8/11)

![Matriz de Confusão YOLOv8/11](fig_matriz_confusao.png)
*Figura 4 — Matriz de Confusão Normalizada do Classificador YOLOv8/11 na Validação com 91 Mechas Reais (3 Classes).*

A avaliação inicial na partição de validação com 3 classes (91 fotografias de mechas) demonstrou acurácia Top-1 de 59,3%, com destaque para a classe Tipo 3 (Cacheado), que alcançou **F1-Score de 0,899 (Precisão 91,2% e Recall 88,6%)**. A confusão entre Tipo 2 (Ondulado) e Tipo 4 (Crespo) decorrente de frizz e reflexos de óleos reforça metodologicamente a necessidade da **Fusão Multimodal** com a anamnese clínica para blindar o diagnóstico.

### 5.6 Validação do Modelo de 4 Classes e Rejeição Adversarial de Outliers

![Matriz de Confusão 4 Classes](fig_matriz_confusao_4classes.png)
*Figura 5 — Matriz de Confusão do Classificador YOLOv8 Expandido para 4 Classes com Classe Negativa de Controle.*

A incorporação da classe negativa `careca_sem_cabelo` elevou a acurácia global do modelo para **92,0%** no conjunto de validação supervisionado. Na avaliação de estresse adversarial contendo 13 cenários extremos (incluindo homens calvos com barba cerrada, fotos com óculos reflexivos, iluminação em penumbra, documentos impressos, tecidos com padronagem, ruído digital e anúncios comerciais), o motor atingiu **100% de taxa de rejeição correta**, retornando `cabelo_detectado: False` e prevenindo diagnósticos falsos de curvatura. O tempo de resposta médio registrado em contêiner de produção com ONNX Runtime foi de **12,4 ms**, comprovando a viabilidade técnica e escalabilidade em hardware de baixo custo.
