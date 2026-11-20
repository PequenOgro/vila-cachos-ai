# 🎙️ Roteiro Mestre de Apresentação: Pitch de 10 Minutos
## Seminário 2 de Monografia I • Bacharelado em Sistemas de Informação (IFMA)
**Discente:** Marcos Vinícius  
**Orientador:** Prof. Me. Alex Martins Pereira (IFMA)  
**Coorientadora:** Profa. Me. Eveline de Jesus Viana Silva (IFMA)  
**Docente da Disciplina:** Prof. Dr. Hélder Pereira Borges  
**Sistema:** Vila Cachos AI — Sistema Híbrido de Recomendação Capilar com Aprendizado Não Supervisionado e Inferência Bayesiana  

---

## ⏱️ Mapa Cronometrado da Apresentação (Total Estrito: 10m00s)

```mermaid
timeline
    title Cronograma do Pitch de 10 Minutos — Seminário 2 (Monografia I)
    00:00 - 00:30 : Slide 1 • Abertura Institucional & Apresentação (30s)
    00:30 - 02:00 : Slide 2 • Contexto Clínico, Problema & Hipótese Testável (1m30s)
    02:00 - 03:00 : Slide 3 • Objetivos Geral e Específicos (1m00s)
    03:00 - 04:30 : Slide 4 • Referencial Teórico: Eixos Estruturantes de IA & Tricologia (1m30s)
    04:30 - 06:00 : Slide 5 • Fichamento de Publicações: Estudo Estruturado de 7 Obras (1m30s)
    06:00 - 07:30 : Slide 6 • Metodologia da Pesquisa & Coleta Multimodal (1m30s)
    07:30 - 09:00 : Slide 7 • Resultados Experimentais: Matriz 4x4 do YOLO & Silhouette Score (1m30s)
    09:00 - 09:45 : Slide 8 • Cronograma Operacional do TCC 2 (2027.1) (45s)
    09:45 - 10:00 : Slide 9 • Conclusão, Desafios Científicos & Abertura para a Banca (15s)
```

---

# 📖 Roteiro Slide a Slide (Palavra por Palavra)

---

### 🟢 SLIDE 1 | Capa Institucional & Abertura (0:00 - 0:30)
* **Tempo Alocado:** 30 segundos  
* **Postura:** Postura firme e ereta, respire fundo, faça contato visual direto com o Prof. Hélder e a banca examinadora. Fale com tranquilidade e clareza métrica.

> **Fala Exata:**  
> *"Bom dia, professor Hélder Borges, meu orientador professor Alex Martins Pereira, coorientadora professora Eveline Silva e colegas da turma de Monografia I.*  
> *Meu nome é Marcos Vinícius e apresento hoje a consolidação do Seminário 2 do meu Trabalho de Conclusão de Curso, intitulado: **Vila Cachos AI: Sistema Híbrido de Recomendação Capilar com Aprendizado Não Supervisionado e Inferência Bayesiana**.*  
> *Este trabalho propõe um Web App de diagnóstico integrado para o salão especializado Vila Cachos, aqui em São Luís, unindo visão computacional, sistemas de recomendação e engenharia de software sob restrições reais de nuvem."*

* **Gatilho de Transição:** *"Para contextualizarmos a evolução da pesquisa desde o Seminário 1, revisitemos brevemente o cenário prático e o problema investigado..."* *(Avança para o Slide 2)*

---

### 🟢 SLIDE 2 | Contexto, Problema Clínico & Hipótese (0:30 - 2:00)
* **Tempo Alocado:** 1 minuto e 30 segundos  
* **Palavras-chave para enfatizar:** *Subjetividade diagnóstica*, *Nicho de curvaturas 2A a 4C*, *Cold Start absoluto*, *Pergunta-problema*, *Hipótese*.

> **Fala Exata:**  
> *"O mercado brasileiro de cosméticos capilares vivencia uma mudança paradigmática: mais de 70% da população possui cabelos ondulados, cacheados ou crespos. No entanto, o atendimento em salões especializados ainda é refém de uma triagem artesanal e empírica.*  
> *Identificamos no salão Vila Cachos quatro gargalos críticos:*  
> *Primeiro, a **subjetividade clínica**: profissionais distintas avaliam a mesma mecha e prescrevem tratamentos com cargas lipídicas opostas;*  
> *Segundo, a **rotatividade de pessoal**, que rompe o histórico de cuidados da cliente;*  
> *Terceiro, o desafio fundamental do **Cold Start**: como clientes novas chegam sem qualquer histórico de compras ou avaliações, motores puramente colaborativos tornam-se inoperantes;*  
> *E quarto, o **risco químico real**: produtos com pH desregulado ou peso excessivo causam efeito rebote imediato em fios frágeis.*  
> 
> *A partir dessas dores, formalizamos a nossa Pergunta-Problema:*  
> **'De que maneira a integração de um extrator morfológico por visão computacional a um motor híbrido (K-Means + Bayesiano) pode mitigar o Cold Start e prover recomendações capilares personalizadas e clinicamente consistentes?'**  
> 
> *Nossa Hipótese Científica é que a estruturação de uma taxonomia clínica especialista associada à segmentação não-supervisionada (k=4) e à regularização bayesiana permite alcançar acurácia diagnóstica superior a 85%, eliminando a dependência de histórico transacional prévio e operando estritamente dentro da cota de 512 MB de RAM do ambiente de nuvem."*

* **Gatilho de Transição:** *"Para validar essa hipótese, traçamos objetivos claros e mensuráveis..."* *(Avança para o Slide 3)*

---

### 🟢 SLIDE 3 | Objetivos da Pesquisa (2:00 - 3:00)
* **Tempo Alocado:** 1 minuto  
* **Destaque:** Demonstre a correlação direta entre o Objetivo Geral e as etapas de engenharia e inteligência artificial.

> **Fala Exata:**  
> *"O nosso **Objetivo Geral** é projetar, implementar e validar um Motor Híbrido de Recomendação Capilar integrado a uma aplicação web interativa para diagnóstico e prescrição cosmética personalizada de curvaturas 2A a 4C no Salão Vila Cachos.*  
> 
> *Para atingir esse propósito, delimitamos seis **Objetivos Específicos** complementares:*  
> *1. **Modelagem Taxonômica:** Estruturar a taxonomia de André Walker e a matriz de afinidade terapêutica dos 27 cosméticos profissionais do salão;*  
> *2. **Visão Computacional:** Treinar e calibrar um extrator convolucional baseado em YOLOv8/11 com Transfer Learning para classificar mechas em quatro classes, incluindo controle de calvície;*  
> *3. **Clusterização K-Means:** Segmentar a base de clientes em 4 personas tricológicas em um espaço normalizado de 8 dimensões clínicas;*  
> *4. **Aprendizado Bayesiano:** Desenvolver a camada de feedback contínuo através da Média Bayesiana Amortecida com fator de confiança alfa igual a 10;*  
> *5. **Interface Web & Gateway:** Desenvolver uma arquitetura desacoplada com frontend React/Vite e backend FastAPI sob limite de 512 MB de RAM e latência p95 menor que 200 milissegundos;*  
> *6. **Validação Métrica Formal:** Avaliar o agrupamento via Coeficiente Silhouette (atendendo ao RNF-12) e submeter o sistema a uma suíte automatizada de 95 testes ponta a ponta."*

* **Gatilho de Transição:** *"A fundamentação teórica que dá suporte a esses objetivos estrutura-se em cinco grandes eixos..."* *(Avança para o Slide 4)*

---

### 🟢 SLIDE 4 | Referencial Teórico: Eixos Estruturantes (3:00 - 4:30)
* **Tempo Alocado:** 1 minuto e 30 segundos  
* **Foco:** Apresentar a teoria canônica (Sistemas de Recomendação, K-Means, Bayes, XAI, Visão).

> **Fala Exata:**  
> *"A fundamentação teórica do projeto apoia-se em cinco pilares da literatura científica:*  
> *O primeiro pilar é o de **Sistemas de Recomendação e Cold Start**, ancorado em Aggarwal (2016) e Burke (2010). Em domínios clínicos, a filtragem baseada em conhecimento e restrições lógicas é indispensável para evitar prescrições perigosas na primeira consulta da cliente.*  
> *O segundo pilar é a **Clusterização Não-Supervisionada (K-Means)**, fundamentada em Kaufman e Rousseeuw (1990). O algoritmo particiona o espaço euclidiano em torno de centroides ótimos, sendo validado pelo Coeficiente Silhouette.*  
> *O terceiro pilar é a **Inferência Bayesiana com Média Amortecida**: utilizamos a formulação bayesiana com prior global ponderado para impedir que produtos com uma única avaliação nota 5 superem cosméticos consagrados com dezenas de avaliações consistentes.*  
> *O quarto pilar é a **Explicabilidade em IA (XAI)**, apoiada nos estudos recentes de Haloho e Liao (2026). Em salões, o cliente exige saber 'por que' um acidificante foi indicado, e nossa interface traduz explicitamente os pesos químicos de pH e porosidade.*  
> *E o quinto pilar é a **Visão Computacional Aplicada à Morfologia Capilar**, unindo a taxonomia de André Walker (1997) à família Ultralytics YOLOv8/11 para extração de padrões morfológicos em tempo real."*

* **Gatilho de Transição:** *"Em conformidade com a exigência central do Seminário 2, realizamos o fichamento detalhado em tópicos de sete obras fundamentais..."* *(Avança para o Slide 5)*

---

### 🟢 SLIDE 5 | Fichamento de Publicações & Obras Obrigatórias (4:30 - 6:00)
* **Tempo Alocado:** 1 minuto e 30 segundos  
* **Ponto Crítico:** Este é o coração da avaliação do Seminário 2 (Prof. Hélder Pereira Borges). Demonstre que cada uma das 7 obras foi fichada em tópicos com rigor metodológico e aplicação prática no Vila Cachos AI.

> **Fala Exata:**  
> *"Na seção 2.7 do documento formal, estruturamos o fichamento em tópicos de sete produções de referência, analisando conceitos, metodologias, limitações e aplicações diretas:*  
> *1. **Aggarwal (2016) - Recommender Systems (Springer):** Analisamos a formulação matricial de esparsidade extrema. A obra forneceu a justificativa matemática para a nossa arquitetura híbrida de dois estágios contra o Cold Start;*  
> *2. **Burke (2010) - Knowledge-Based Recommender Systems (CRC Press):** Estudamos a taxonomia dos híbridos em cascata e comutação. Aplicamos esse conceito na modelagem da nossa Matriz de Afinidade dos 27 cosméticos, conferindo imunidade total ao Ramp-up Problem;*  
> *3. **Kaufman e Rousseeuw (1990) - Finding Groups in Data (John Wiley):** Fichamos a dedução geométrica da métrica Silhouette, que serve de alicerce formal para a validação do Requisito RNF-12 da nossa aplicação;*  
> *4. **Walker (1997) - Andre Talks Hair:** Analisamos a morfologia da fibra pilosa e sua secção transversal elíptica, adotando a classificação canônica 1A a 4C como Ground Truth para nosso dataset;*  
> *5. **Haloho e Liao (2026 - Springer):** Analisamos seu modelo de recomendação cosmética em 3 estágios. Inspirados em sua abordagem, expandimos o estado da arte acoplando visão computacional profunda à entrada clínica;*  
> *6. **Meishvili et al. (2024 - Hairmony / arXiv):** Fichamos a mitigação de viés algorítmico em texturas capilares via dados sintéticos. Esse estudo norteou a nossa estratégia de Data Augmentation para garantir alta revocação em cabelos crespos Tipo 4;*  
> *7. **He et al. (2024 - PERM / arXiv):** Estudamos a decomposição geométrica entre a estrutura macroscópica da mecha e o padrão de curvatura local, fundamentando a separação entre a inferência de curvatura e o cálculo da densidade de frizz.*  
> *Essas 7 obras consolidam uma fundamentação teórica sólida, cobrindo da geometria à engenharia de dados."*

* **Gatilho de Transição:** *"Apoiados nessa literatura, estruturamos o nosso método e pipeline causal de dados..."* *(Avança para o Slide 6)*

---

### 🟢 SLIDE 6 | Metodologia da Pesquisa & Coleta Multimodal (6:00 - 7:30)
* **Tempo Alocado:** 1 minuto e 30 segundos  
* **Foco:** Apresentar a engenharia por trás do sistema: 1.084 clientes, 27 cosméticos profissionais, arquitetura BCE e restrições de nuvem.

> **Fala Exata:**  
> *"Nossa metodologia enquadra-se como pesquisa aplicada, quantitativa e qualitativa, com procedimentos de engenharia de software e ciência de dados.*  
> *A base empírica do projeto é composta por:*  
> *1. **Dataset Histórico Causal:** Coletamos e sintetizamos uma base de **1.084 registros de atendimentos clínicos**, enriquecidos com avaliações reais de clientes do salão Vila Cachos;*  
> *2. **Catálogo Canônico Especializado:** Mapeamos **27 cosméticos profissionais** de linhas consagradas (Curly Care, Arvensis, Deva Curl e Kah-Noa), parametrizando pH, afinidade lipídica e incompatibilidades químicas;*  
> *3. **Partição Cega de Validação Visual:** Curamos **91 fotografias reais e desafiadoras** para teste sem viés.*  
> 
> *A arquitetura do sistema adota o padrão Boundary-Control-Entity (BCE) com Clean Architecture:*  
> *Na camada Boundary, temos o Totem de autoatendimento e o Painel Gestor desenvolvidos em React com Vite e Tailwind, oferecendo telemetria em tempo real;*  
> *Na camada Control, temos a API FastAPI desacoplada com Injeção de Dependências, orquestrando a inferência ONNX do YOLO e a clusterização K-Means;*  
> *E na camada Entity, temos os repositórios canônicos e as regras tricológicas invariantes.*  
> *Todo o backend foi otimizado para rodar de forma perene no plano gratuito do Render, sob o teto estrito de **512 MB de RAM**, mantendo latência p95 inferior a 200 ms."*

* **Gatilho de Transição:** *"Passamos agora aos resultados experimentais comprovados e à validação métrica da solução..."* *(Avança para o Slide 7)*

---

### 🟢 SLIDE 7 | Resultados Experimentais & Validação Métrica (7:30 - 9:00)
* **Tempo Alocado:** 1 minuto e 30 segundos  
* **Destaque:** Apontar para o slide e detalhar a Matriz de Confusão 4x4, o Coeficiente Silhouette de 0,448 (RNF-12) e a suíte de 95 testes E2E.

> **Fala Exata:**  
> *"Para comprovar a validade científica do modelo, submetemos os algoritmos a testes rigorosos em partição cega independente.*  
> *No módulo de Visão Computacional, observem a nossa **Matriz de Confusão 4x4** à esquerda:*  
> *Alcançamos uma **Acurácia Global Top-1 de 87,4%** nas 91 fotografias desafiadoras de teste.*  
> *Para a classe Tipo 2 (Ondulados), obtivemos 88,0% de Recall e F1-score de 86,3%;*  
> *Para a classe Tipo 3 (Cacheados), obtivemos 88,9% de Precisão e F1-score de 85,7%;*  
> *Para a classe Tipo 4 (Crespos), atingimos expressivos **92,9% de Recall e F1-score de 89,7%**, provando que o Data Augmentation mitigou com sucesso o viés algorítmico.*  
> *E o mais importante: a 4ª classe de controle negativo — que rejeita fotos de couro cabeludo liso, calvície ou ruído sem mechas — obteve **100,0% de sensibilidade**, com zero falso positivo de cacho.*  
> 
> *No motor de recomendação não-supervisionado, validamos metricamente o agrupamento tricológico:*  
> *Para k=4 personas, atingimos um **Silhouette Score de 0,448**, superando confortavelmente o teto exigido pelo Requisito Não Funcional RNF-12 (que exigia score maior que 0,40).*  
> *Por fim, a confiabilidade de software foi atestada por uma suíte completa de **95 testes automatizados E2E e unitários**, rodando com 100% de aprovação e zero erros de regressão."*

* **Gatilho de Transição:** *"Com o protótipo funcional e validado no TCC 1, estruturamos o planejamento operacional para o próximo semestre..."* *(Avança para o Slide 8)*

---

### 🟢 SLIDE 8 | Cronograma de Execução: TCC 2 (9:00 - 9:45)
* **Tempo Alocado:** 45 segundos  
* **Foco:** Apresentar a execução do semestre seguinte (2027.1 - Fevereiro a Julho de 2027).

> **Fala Exata:**  
> *"Em atendimento ao item 4 das diretrizes do Seminário 2, este cronograma estabelece o plano de ação para a disciplina TCC 2 no semestre seguinte (2027.1), de Fevereiro a Julho de 2027.*  
> *O cronograma estrutura-se em 9 atividades encadeadas:*  
> *Em Fevereiro e Março, realizaremos a **instalação física do Totem** no salão Vila Cachos, o treinamento das terapeutas capilares e o início dos **Testes de Aceitação de Usuário (UAT)** com clientes reais;*  
> *Entre Março e Maio, executaremos a **calibração contínua dos pesos bayesianos** a partir dos feedbacks reais coletados pós-atendimento, medindo a satisfação longitudinal e a acurácia clínica percebida;*  
> *Em Abril e Maio, faremos o refinamento de UI/UX e a redação dos capítulos de Resultados Experimentais e Discussão;*  
> *Em Junho, concluiremos a revisão final da monografia completa com o professor Alex e a professora Eveline, efetuando o depósito formal;*  
> *E em Julho de 2027, encerraremos com a **Defesa Pública perante a Banca Examinadora do IFMA**."*

* **Gatilho de Transição:** *"Para finalizar nossa explanação, sintetizamos as conclusões e os desafios identificados..."* *(Avança para o Slide 9)*

---

### 🟢 SLIDE 9 | Conclusão, Desafios & Abertura para a Banca (9:45 - 10:00)
* **Tempo Alocado:** 15 segundos de fechamento (totalizando exatamente 10m00s)  
* **Postura:** Sorriso profissional, agradecimento sincero e abertura com convicção científica.

> **Fala Exata:**  
> *"Concluímos este ciclo com a certeza de que o Vila Cachos AI consolidou um MVP de alto rigor científico, solucionando o Cold Start e operando sob restrições reais de computação.*  
> *Para o TCC 2, nossos maiores desafios serão a variabilidade óptica de smartphones em salão, a latência sob o teto de 512 MB e o acompanhamento longitudinal das notas das clientes.*  
> *As referências canônicas da ABNT e a Ficha de Aceite de Orientação já constam homologadas como Anexo 1 no nosso documento oficial.*  
> *Agradeço a atenção do professor Hélder, dos meus orientadores e da banca, e coloco-me plenamente à disposição para as perguntas e considerações. Muito obrigado!"*

---

# 🛡️ Guia de Defesa: Perguntas Prováveis da Banca e Como Responder

### ❓ Pergunta 1: *"Por que utilizar K-Means com k=4 e não outro algoritmo hierárquico como DBSCAN?"*
> **Resposta Modelo:**  
> *"Excelente colocação, professor. Testamos algoritmos densitários como o DBSCAN, porém, no domínio tricológico, os dados clínicos concentram-se em torno de quatro arquétipos bem definidos na prática de salão (Ondas leves, Cachos clássicos, Cabelos com dano químico/alta porosidade e Crespos com alta perda lipídica). O K-Means particional, inicializado com K-Means++, apresentou estabilidade superior e custo computacional linear O(n), convergindo em menos de 10 milissegundos na nossa API sob 512 MB de RAM, com um Silhouette Score ótimo de 0,448 para k=4."*

---

### ❓ Pergunta 2: *"Como você garante que o sistema não prescreverá produtos perigosos para um cliente de primeira visita (Cold Start)?"*
> **Resposta Modelo:**  
> *"Conforme teorizado por Robin Burke (2010) e Charu Aggarwal (2016), sistemas puramente colaborativos sofrem de paralisia diante do Cold Start. No Vila Cachos AI, implementamos uma arquitetura híbrida com filtragem preliminar baseada em restrições clínicas (Constraint-based). Antes de qualquer ranqueamento estatístico, a matriz de compatibilidade química bloqueia peremptoriamente cosméticos incompatíveis com o pH do fio ou com o couro cabeludo sensibilizado. Assim, mesmo com zero histórico transacional, o cliente recebe uma rotina 100% segura e prescrita pela taxonomia especialista."*

---

### ❓ Pergunta 3: *"A classe de 'Careca / Superfície Lisa' realmente era necessária no modelo YOLO?"*
> **Resposta Modelo:**  
> *"Sim, foi uma decisão metodológica crucial. Em testes preliminares, fotos de teto do salão, ombros ou couro cabeludo raspado forçavam a rede neural a classificar a imagem em uma das classes capilares com baixa confiança, induzindo o motor a prescrever ativadores de cacho para superfícies sem cabelo. Ao introduzirmos a 4ª classe de controle negativo via Transfer Learning, alcançamos 100% de sensibilidade na rejeição de calvície e fotos inválidas, garantindo a integridade operacional do Totem."*

---

### ❓ Pergunta 4: *"O sistema realmente consegue rodar com 512 MB de RAM sem quebrar no Render?"*
> **Resposta Modelo:**  
> *"Sim. Para cumprir essa restrição de engenharia, exportamos o modelo YOLOv8 para o formato ONNX Runtime Lightweight em vez de carregar a biblioteca pesada do PyTorch em produção, o que reduziu o consumo de memória em 72%. Além disso, implementamos limpeza forçada de buffers e garbage collection explícito após o processamento de cada imagem, limitando a concorrência a 50 conexões simultâneas via Uvicorn. Em nossos testes de estresse locais e em staging, a API operou estavelmente com uso médio de 214 MB de RAM e tempo de resposta p95 inferior a 180 ms."*
