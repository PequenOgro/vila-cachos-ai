# Vila Cachos AI — Conteúdo Estruturado para Slides no Canva
**Disciplina:** Análise e Projeto de Sistemas II — IFMA  
**Docente:** Profª. Eveline de Jesus Viana Sá  
**Equipe:** Marcos Vinícius, Jordan, Rafael  
**Data da Avaliação 1:** 29 de Outubro de 2026  

---

## 💡 Dica para o Canva:
Copie e cole cada bloco abaixo diretamente nos slides do Canva. Se você usar templates do Canva com o tema **"Software Architecture Pitch"**, **"Tech Minimalist"** ou **"Dark/Emerald Green AI"**, o resultado fica no padrão profissional corporativo.

---

### SLIDE 1 — Capa do Projeto
* **Título Principal:** Vila Cachos AI
* **Subtítulo:** Totem Inteligente de Diagnóstico Capilar & Recomendação Personalizada de Cosméticos
* **Contexto Acadêmico:** Avaliação 1 — Entrega e Apresentação da Modelagem Completa de Software
* **Disciplina:** Análise e Projeto de Sistemas II
* **Docente:** Profª. Eveline de Jesus Viana Sá
* **Equipe de Desenvolvimento:**
  * Marcos Vinícius (Gerente / Desenvolvedor)
  * Jordan (Analista / Desenvolvedor)
  * Rafael (Analista / Desenvolvedor)

---

### SLIDE 2 — Contexto, Problema e Solução
* **O Problema:** No atendimento a clientes com cabelos cacheados e crespos (curvaturas 2A a 4C), o diagnóstico manual e a indicação de cosméticos tomam tempo das cabeleireiras e geram filas na recepção do salão.
* **A Solução:** Um **Totem físico de autoatendimento interativo** posicionado na entrada do salão Vila Cachos.
* **Inteligência Artificial Aplicada:**
  1. **Visão Computacional (YOLOv8):** Análise da mecha do cabelo pela câmera do totem.
  2. **Motor Híbrido (K-Means + Heurísticas):** Recomenda o cronograma capilar (Hidratação, Nutrição, Reconstrução) e produtos com base no tipo de cacho, porosidade e orçamento do cliente.
* **Impacto:** Acelera o início do atendimento, empodera o cliente com dados reais sobre seu cabelo e converte vendas de cosméticos.

---

### SLIDE 3 — Atores do Sistema
* **1. Cliente do Salão (Ator Principal):**
  * Interage diretamente com a tela touch do totem.
  * Tira a foto, responde ao questionário rápido de hábitos e recebe a rotina personalizada com QR Code.
* **2. Gestor / Profissional do Salão (Ator Secundário):**
  * Acessa a retaguarda administrativa.
  * Gerencia o catálogo de cosméticos (adiciona produtos, preços, marcas) e audita relatórios de feedbacks.
* **3. Subsistema de Visão Computacional (Ator Externo/Serviço):**
  * Processa o feed de imagem, detecta a presença de cabelo/mechas e infere a curvatura com índice de confiança.
* **4. Subsistema Recomanadador IA (Ator Interno/Serviço):**
  * Executa o pipeline de Machine Learning (clusterização K-Means + regras de negócio).

---

### SLIDE 4 — Requisitos do Sistema (RFs & RNFs)
* **Requisitos Funcionais Principais:**
  * **RF-01 (Captura de Imagem):** Capturar foto da mecha via câmera do totem com validação anti-fraude (cabelo presente).
  * **RF-02 (Diagnóstico Visual):** Detectar curvatura capilar (2A-4C) e estimar porosidade.
  * **RF-03 (Anamnese Interativa):** Coletar nível de ressecamento, química prévia e orçamento do cliente.
  * **RF-04 (Geração de Rotina):** Indicar produtos compatíveis com o cluster capilar do cliente.
  * **RF-05 (Feedback e Avaliação):** Coletar nota (1 a 5 estrelas) ao final do atendimento para re-treino.
* **Requisitos Não Funcionais (Critérios de Qualidade):**
  * **RNF-01 (Performance):** Tempo de resposta do diagnóstico completo em menos de 1,5 segundos.
  * **RNF-02 (Segurança & LGPD):** Nenhuma foto facial é salva desnecessariamente; descarte de buffer após inferência.
  * **RNF-03 (Resiliência do Totem):** *Timeout* automático de 15 minutos de inatividade com reset para tela inicial.
  * **RNF-04 (Rate Limiting):** Proteção da API contra requisições abusivas repetidas.

---

### SLIDE 5 — Diagrama de Casos de Uso (UML)
*(Inserir aqui o print do diagrama de casos de uso do repositório)*
* **Casos de Uso Mapeados:**
  * **UC-01:** Iniciar Atendimento no Totem (Cliente)
  * **UC-02:** Realizar Diagnóstico Fotográfico (Cliente + YOLOv8)
    * *Extensão:* UC-02.1 Fallback Manual se foto for inconclusiva.
  * **UC-03:** Preencher Questionário Capilar (Cliente)
  * **UC-04:** Gerar Recomendação Híbrida (Sistema Recomanadador)
  * **UC-05:** Visualizar Rotina & Enviar por QR Code / WhatsApp (Cliente)
  * **UC-06:** Avaliar Recomendação Recebida (Cliente)
  * **UC-07:** Gerenciar Catálogo de Cosméticos (Gestor)
* **Especificação Formal:** Todos os casos possuem atores, pré-condições, fluxo principal (caminho feliz) e fluxos de exceção documentados.

---

### SLIDE 6 — Diagrama de Classes & Dicionário de Métodos
*(Esclarecimento do "Diagrama de Métodos" exigido pela professora)*
* **O que é:** Na UML, os métodos são expressos na terceira seção das classes do Diagrama de Classes e detalhados na sua execução pelos Diagramas de Sequência.
* **Classes Principais e Seus Métodos Chave:**
  * **`VilaCachosRecommender`:**
    * `+fit(dados_historicos: DataFrame): void`
    * `+recomendar(perfil: PerfilCliente): RecomendacaoResponse`
    * `+calcular_score_hibrido(cluster_id, restricoes): List[Produto]`
  * **`YoloHairClassifier`:**
    * `+carregar_modelo(weights_path: str): void`
    * `+predict_image_bytes(image_data: bytes): HairAnalysisResult`
    * `+validar_presenca_cabelo(boxes): bool`
  * **`IFeedbackRepository` (Interface / DIP):**
    * `+salvar(feedback: FeedbackRegistro): bool`
    * `+obter_historico(): List[FeedbackRegistro]`
  * **Schemas Pydantic (Modelos de Dados):**
    * `PerfilClienteRequest`, `RecomendacaoResponse`, `ProdutoCatalogo`.

---

### SLIDE 7 — Diagrama de Sequência 01: Atendimento Completo no Totem
*(Inserir a Página 1 do PDF de Sequência - `diagramas_sequencia_drawio_completo.pdf`)*
* **Objetivo:** Mapear o ciclo de vida de uma sessão de autoatendimento, do primeiro toque à saída da rotina.
* **Linhas de Vida (Lifelines):**
  * `Cliente` ➡️ `Totem UI (React/Vite)` ➡️ `FastAPI Gateway` ➡️ `YOLO Classifier` ➡️ `Recommender Engine`
* **Momentos Críticos:**
  * Handshake inicial e criação de sessão temporária (`session_id`).
  * Processamento assíncrono da imagem em memória sem gravação em disco.
  * Retorno instantâneo do cronograma capilar na tela.

---

### SLIDE 8 — Diagrama de Sequência 02: Diagnóstico por Visão Computacional
*(Inserir a Página 2 do PDF de Sequência)*
* **Objetivo:** Detalhar a validação de segurança e acurácia visual da foto capilar.
* **Fluxo de Decisão (alt / opt):**
  1. Cliente posiciona mecha e câmera captura imagem.
  2. Frontend envia imagem via multipart para `POST /vision/analyze`.
  3. YOLOv8 executa segmentação e contagem de classes capilares.
  4. **Se cabelo for detectado:** Retorna curvatura (ex: `3B - Cacheado`) e confiança (ex: `94%`).
  5. **Se foto não tiver cabelo (ex: objeto, pessoa careca, fundo vazio):** Dispara `422 Unprocessable` e abre **Fallback Manual** guiado na interface sem travar o totem.

---

### SLIDE 9 — Diagrama de Sequência 03: Motor Híbrido de Recomendação
*(Inserir a Página 3 do PDF de Sequência)*
* **Objetivo:** Mostrar como a inteligência analítica combina Machine Learning com regras dermatológicas.
* **Etapas Internas da API:**
  1. Vetorização das características do cliente (Curvatura, Porosidade, Danos, Orçamento).
  2. Inferência de Cluster pelo modelo `K-Means`.
  3. Filtragem de catálogo (elimina produtos com químicos incompatíveis).
  4. Ranqueamento pelo score de afinidade com o cacho.
  5. Montagem da resposta estruturada com Shampoo, Máscara, Condicionador e Finalizador.

---

### SLIDE 10 — Diagrama de Sequência 04: Feedback e Ciclo de Aprendizado
*(Inserir a Página 4 do PDF de Sequência)*
* **Objetivo:** Demonstrar como o sistema evolui a partir da avaliação do usuário real.
* **Arquitetura Desacoplada (Clean Architecture):**
  * O endpoint `POST /feedback` injeta a interface `IFeedbackRepository`.
  * Não trava a interface do totem: o feedback é salvo e confirmação visual rápida é exibida.
  * O modelo fica pronto para retreino periódico com novas amostras reais.

---

### SLIDE 11 — Diagramas de Sequência 05 & 06: Resiliência, Timeouts e Gestão
*(Inserir as Páginas 5 e 6 do PDF de Sequência)*
* **Cenário 05 (Timeout e Limpeza de Sessão):**
  * O cliente abandonou o totem no meio do preenchimento?
  * O temporizador expira em 15 minutos, a tela emite alerta sonoro/visual sutil e limpa os dados da memória, retornando à tela de descanso para o próximo cliente.
* **Cenário 06 (Administração do Catálogo):**
  * O gestor entra com credenciais seguras, atualiza preços e o cache do recommender é invalidado instantaneamente.

---

### SLIDE 12 — Conclusão & Status do Projeto
* **Status Atual da Engenharia de Software:**
  * ✅ **Requisitos & Casos de Uso:** 100% formalizados e validados.
  * ✅ **Diagrama de Classes & Métodos:** Estruturados com princípios SOLID e Clean Architecture.
  * ✅ **Diagramas de Sequência:** 6 fluxos arquiteturais validados no draw.io.
  * ✅ **Implementação Real:** Backend FastAPI com testes automatizados e Frontend Totem UI em React / TypeScript compilando com 0 erros.
* **Equipe pronta para a banca:** Marcos Vinícius, Jordan e Rafael.

---

## 👥 ROTEIRO DE APRESENTAÇÃO — DIVISÃO DE FALAS

### 🎤 Integrante 1 (Marcos Vinícius) — ~3 a 4 minutos
* **Abertura e Contexto:** Apresenta o salão Vila Cachos, a proposta do totem inteligente e a arquitetura geral do sistema.
* **Atores e Requisitos:** Explica os atores principais (Cliente, Gestor, IAs) e os requisitos não funcionais críticos (Segurança LGPD, latência < 1.5s, timeout de 15 min).
* **Casos de Uso:** Mostra o diagrama de casos de uso e os fluxos principais (UC-01 e UC-02).

### 🎤 Integrante 2 (Jordan) — ~3 a 4 minutos
* **Classes e Métodos:** Explica o diagrama de classes, o desacoplamento de responsabilidades (Repository Pattern, Pydantic Schemas) e esclarece a assinatura dos métodos centrais (`recomendar()`, `predict_image_bytes()`).
* **Sequência do Diagnóstico Visual (Diagrama 02):** Explica como o modelo YOLOv8 processa a foto e a segurança do fallback manual caso a imagem não tenha cabelo.

### 🎤 Integrante 3 (Rafael) — ~3 a 4 minutos
* **Sequência do Recomanadador Híbrido (Diagrama 03):** Explica a mágica do K-Means operando em conjunto com as heurísticas de curvatura capilar.
* **Resiliência e Feedback (Diagramas 04 e 05):** Detalha a persistência assíncrona da nota do cliente e a política de timeout de 15 minutos do totem.
* **Conclusão:** Destaca que o projeto não é apenas teórico, mas um software funcional rodando com testes e validação contínua.
