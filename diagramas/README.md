# Pasta de Arquivos de Diagramas de Sequência — Vila Cachos AI

Esta pasta reúne todos os arquivos de **Diagramas de Sequência UML** renderizados e exportados do **draw.io**, além dos respectivos códigos-fonte em **Mermaid.js**, preparados para a documentação acadêmica de **Análise 2**.

---

## 📁 Estrutura de Arquivos

### 1. Documento Consolidado Completo
* 📄 [`diagramas_sequencia_drawio_completo.pdf`](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/diagramas_sequencia_drawio_completo.pdf) — Contém todos os 6 diagramas renderizados em vetor de alta definição em um único arquivo.

---

### 2. Arquivos Individuais por Caso de Uso (PDF e Mermaid)

Cada membro da equipe pode acessar diretamente os 2 diagramas da sua atribuição tanto no formato visual exportado (PDF) quanto no código editável (Mermaid):

| Caso de Uso | Arquivo Visual (draw.io) | Código Fonte Mermaid | Atores & Escopo |
| :--- | :--- | :--- | :--- |
| **UC-02**: Preencher anamnese capilar | [UC02_preencher_anamnese_capilar.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC02_preencher_anamnese_capilar.pdf) | [UC02_preencher_anamnese_capilar.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC02_preencher_anamnese_capilar.mermaid) | Cliente do salão / Interface Web (4 etapas, regras de negócio e timeout de 15 min) |
| **UC-03**: Gerar recomendação híbrida | [UC03_gerar_recomendacao_hibrida.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC03_gerar_recomendacao_hibrida.pdf) | [UC03_gerar_recomendacao_hibrida.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC03_gerar_recomendacao_hibrida.mermaid) | Interface Web, RecommenderAPI, Motor K-Means, Matriz e Histórico (Top 3, Bayesiano, Exceções 422/429/503) |
| **UC-04**: Visualizar diagnóstico e recomendações | [UC04_visualizar_diagnostico_recomendacoes.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC04_visualizar_diagnostico_recomendacoes.pdf) | [UC04_visualizar_diagnostico_recomendacoes.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC04_visualizar_diagnostico_recomendacoes.mermaid) | Cliente do salão, Interface Web, RecommenderAPI (Apresentação da persona, pesos adaptativos, Top 3 e extensões) |
| **UC-05**: Registrar feedback de produto | [UC05_registrar_feedback_produto.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC05_registrar_feedback_produto.pdf) | [UC05_registrar_feedback_produto.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC05_registrar_feedback_produto.mermaid) | Cliente do salão, RecommenderAPI, Motor, Catálogo e CSV (Validação catálogo HTTP 400, recalibração bayesiana) |
| **UC-06**: Consultar catálogo | [UC06_consultar_catalogo.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC06_consultar_catalogo.pdf) | [UC06_consultar_catalogo.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC06_consultar_catalogo.mermaid) | Gestor / responsável técnico, RecommenderAPI, ProdutoCatalogo (Matriz terapêutica de cosméticos) |
| **UC-07**: Monitorar saúde e métricas | [UC07_monitorar_saude_metricas.pdf](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC07_monitorar_saude_metricas.pdf) | [UC07_monitorar_saude_metricas.mermaid](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/diagramas/UC07_monitorar_saude_metricas.mermaid) | Gestor / responsável técnico, RecommenderAPI, Motor e Histórico (Validação is_fitted, Silhouette e inércia) |

---

## 🛠️ Como reutilizar ou editar no draw.io
1. Abra o arquivo `.mermaid` desejado em qualquer editor de texto.
2. Acesse o [draw.io](https://app.diagrams.net/).
3. Vá em **Arrange / Insert** $\rightarrow$ **Advanced** $\rightarrow$ **Mermaid**.
4. Cole o conteúdo e clique em **Insert**.
