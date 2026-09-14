# Projeto de Monografia — TCC I (Sistemas de Informação - IFMA)

## 1. Tema
**Sistema Híbrido de Recomendação de Produtos Capilares com Feedback Loop Bayesiano atuando como um Web App de Diagnóstico Integrado.**

O presente projeto de monografia circunscreve-se na interseção entre a Inteligência Artificial e a Engenharia de Software, propondo a construção de um Motor Híbrido de Recomendação aplicado ao nicho de mercado de salões de beleza especializados em cabelos com curvatura (cacheados e crespos). O sistema, materializado em um Módulo Web de Diagnóstico Integrado, combina heurísticas baseadas em conhecimento de especialistas, segmentação não supervisionada de dados (K-Means) e aprendizado contínuo através da inferência bayesiana. 

## 2. Justificativa
A padronização do diagnóstico capilar por meio de Inteligência Artificial representa uma oportunidade concreta de diferenciação competitiva para pequenos e médios salões de beleza especializados, como a Vila Cachos. Um sistema inteligente disponibilizado como Módulo Web de Diagnóstico Integrado pode (i) reduzir significativamente a variabilidade e a subjetividade do diagnóstico entre diferentes profissionais do estabelecimento, (ii) gerar dados analíticos valiosos que alimentem estratégias de reposição de estoque e campanhas de marketing direcionadas, e (iii) oferecer à cliente uma experiência de atendimento inovadora, personalizada e fundamentada tecnicamente desde o seu primeiro contato com o salão — mesmo na ausência de registros históricos sobre ela.

A adoção de uma arquitetura baseada em Web App — operando em nuvem e dispensando a infraestrutura de um totem físico dedicado de hardware — justifica-se por três pilares centrais: (1) **Escalabilidade**: o módulo pode ser acessado universalmente por meio de um link direto integrado ao site oficial do salão, permitindo que o diagnóstico seja realizado tanto presencialmente através do smartphone do profissional ou da cliente, quanto remotamente de forma prévia ao agendamento; (2) **Redução de Custos**: a eliminação de dependências de terminais físicos, totens interativos e cabeamento suprime as barreiras financeiras e logísticas de implantação, democratizando o acesso da microempresa à tecnologia; (3) **Manutenibilidade Contínua**: evoluções no algoritmo de IA, calibrações de pesos e atualizações no portfólio de produtos são aplicadas centralizadamente na API hospedada em nuvem, refletindo imediatamente na interface do usuário sem a necessidade de intervenções distribuídas.

## 3. Problema de Pesquisa
O mercado especializado em cabelos curvos ressente-se da ausência de bases de dados históricas estruturadas, uma condição que inviabiliza a aplicação de abordagens convencionais de recomendação, configurando o chamado problema do *Cold Start*. Consequentemente, o salão enfrenta inconsistências operacionais e subjetividade diagnóstica humana. 

Diante desse cenário, formula-se o seguinte questionamento científico: **De que maneira a combinação de uma arquitetura híbrida de Inteligência Artificial — integrando clusterização K-Means para segmentação de personas e Média Bayesiana Amortecida para aprendizado contínuo — pode mitigar o problema do *Cold Start* e padronizar o diagnóstico de cosméticos em um salão de beleza especializado, operando sob uma interface Web App altamente escalável?**

## 4. Objetivos

### 4.1 Objetivo Geral
Compreender e mitigar o problema do *Cold Start* em salões especializados por meio do projeto, implementação e validação matemática de um Motor Híbrido de Recomendação capilar integrado a um Web App de Diagnóstico, concebido especificamente para as necessidades operacionais e o portfólio do salão Vila Cachos.

### 4.2 Objetivos Específicos
*   **Modelar a taxonomia do domínio capilar** através da colaboração com especialistas, criando uma matriz de afinidade terapêutica entre atributos do fio (curvatura, porosidade, tratamentos químicos), queixas reportadas e composições de produtos cosméticos.
*   **Desenvolver e calibrar um algoritmo de clusterização (K-Means)** para segmentar o espaço de variáveis capilares e identificar personas comportamentais dominantes.
*   **Implementar uma camada de Aprendizado Contínuo (*Feedback Loop*)** empregando a métrica de Média Bayesiana Amortecida para ancorar as avaliações iniciais e proteger o sistema de flutuações estatísticas severas em amostras pequenas.
*   **Construir e implantar uma interface web reativa (React/Vite)** suportada por uma **API RESTful (FastAPI)**, assegurando a transparência das recomendações por meio de justificativas explicáveis em linguagem natural (XAI).
*   **Garantir o cumprimento de Requisitos Não-Funcionais** essenciais para ambientes corporativos reais, incluindo segurança (*Rate Limiting*), usabilidade (*Dark Mode* nativo) e gestão automatizada de estado e privacidade (*Inactivity Timeout* de 15 minutos).
*   **Avaliar os resultados algorítmicos metricamente**, atestando a qualidade dos agrupamentos formados por meio dos coeficientes matemáticos de Inércia (*Within-Cluster Sum of Squares*), Silhouette Score e Método do Cotovelo.

## 5. Referencial Teórico
O embasamento teórico da monografia perpassará pelos seguintes eixos temáticos:
*   **Sistemas de Recomendação (SR):** Fundamentos, taxonomia de algoritmos (Filtragem Baseada em Conteúdo, Colaborativa e Híbrida).
*   **O Problema do *Cold Start* em SR:** Desafios da escassez inicial de dados, matrizes esparsas, e estratégias de mitigação (*Knowledge-Based Systems* e injeção de dados sintéticos).
*   **Aprendizado de Máquina Não Supervisionado:**
    *   Fundamentos de Clusterização particional.
    *   Funcionamento matemático do Algoritmo K-Means.
    *   Métricas de validação interna de clusters: Inércia (WCSS) e o Coeficiente Silhouette.
*   **Inferência Bayesiana Aplicada a Rankings:** Abordagens de *Feedback Loop*, diferenças críticas entre média aritmética simples e Média Bayesiana Amortecida (*Damped Average*) na estabilização de sistemas recém-implantados.
*   **Explicabilidade em IA (Explainable AI - XAI):** O imperativo ético e de negócios por trás da abertura das "caixas-pretas" algorítmicas, especialmente na área de estética e saúde capilar.

## 6. Metodologia
A presente investigação caracteriza-se pela natureza de **pesquisa aplicada e de caráter exploratório**, estruturada de acordo com o Anexo III do Projeto Pedagógico do Curso (PPC) de Sistemas de Informação do IFMA, e voltada à resolução de um entrave operacional prático em um ambiente empresarial real.

O processo de coleta e geração de dados, tendo em vista a restrição inicial do *Cold Start*, dar-se-á por meio da concepção de um **gerador de dados sintéticos com causalidade probabilística**. Este simulador mimetizará um histórico consistente de 1.000 atendimentos, refletindo as probabilidades condicionais e correlações clínicas reais previamente extraídas junto ao catálogo de produtos e ao conhecimento especialista do salão Vila Cachos (e.g., a elevada correlação condicional entre progressivas passadas e alta porosidade). 

A matriz de análise e validação técnica será bifásica: do ponto de vista da Engenharia de Software, validar-se-á o consumo da API FastAPI, suas restrições de tráfego (*Rate Limiting*) e responsividade do Web App em ambiente de homologação real (Vercel/Render); do ponto de vista de Ciência de Dados, o motor K-Means será submetido a rigorosa validação matemática, avaliando-se a coesão intra-cluster e a separação inter-cluster por meio da inflexão gráfica do Método do Cotovelo e da maximização do Silhouette Score para matrizes ordinais.

## 7. Cronograma Físico-Financeiro (Projeção)

| Etapas (Disciplinas TCC I e II) | Set/26 | Out/26 | Nov/26 | Dez/26 | Fev/27 | Mar/27 | Abr/27 | Mai/27 | Jun/27 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TCC I: Levantamento bibliográfico sistemático e Modelagem** | X | X | | | | | | | |
| **TCC I: Definição da taxonomia de domínio com o salão** | | X | X | | | | | | |
| **TCC I: Desenvolvimento do MVP Arquitetural (API + Web App)** | | | X | X | | | | | |
| **TCC I: Redação e entrega do Projeto de Monografia** | | | | X | | | | | |
| **TCC II: Geração e análise matemática dos dados sintéticos (Silhouette/Elbow)** | | | | | X | X | | | |
| **TCC II: Homologação em Staging com o Cliente (UAT)** | | | | | | X | X | | |
| **TCC II: Refatoração, Ajustes XAI e Deploy em Produção (Locaweb)** | | | | | | | X | X | |
| **TCC II: Redação dos Capítulos de Resultados e Discussão** | | | | | | | | X | X |
| **TCC II: Defesa Final perante Banca Examinadora** | | | | | | | | | X |

## 8. Referências Bibliográficas Base

1. AGGARWAL, Charu C. **Recommender Systems: The Textbook**. 1. ed. Cham: Springer International Publishing, 2016.
2. INSTITUTO FEDERAL DO MARANHÃO (IFMA). **Resolução nº 088/2022**. Aprova o Regulamento do Trabalho de Conclusão de Curso (TCC) dos Cursos de Graduação do IFMA. São Luís: Conselho Superior do IFMA, 2022.
3. KAUFMAN, L.; ROUSSEEUW, P. J. **Finding Groups in Data: An Introduction to Cluster Analysis**. New York: John Wiley & Sons, 1990.
4. PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software: Uma Abordagem Profissional**. 9. ed. Porto Alegre: AMGH, 2021.
5. TAN, Pang-Ning; STEINBACH, Michael; KUMAR, Vipin. **Introdução ao Data Mining - Mineração de Dados**. 2. ed. Rio de Janeiro: Ciência Moderna, 2019.
