# 🌿 Módulo Web de Diagnóstico Capilar (IA Híbrida)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-F7931E?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

**Projeto de TCC** (Sistemas de Informação — IFMA Campus Monte Castelo) desenvolvido para o salão especializado **Vila Cachos** (São Luís - MA).

O sistema resolve o problema de **Cold Start** em salões especializados em cabelos curvos através de um Motor Híbrido de Inteligência Artificial com **XAI (Explicabilidade)** e **Feedback Loop Bayesiano**, consumido por um **Web App de Diagnóstico Capilar** acessível via link no site do salão.

---

## 🌐 Links de Produção

| Ambiente | URL | Plataforma |
| :--- | :--- | :--- |
| 🖥️ **Front-end (Web App)** | [vila-cachos-ai.vercel.app](https://vila-cachos-ai.vercel.app) | Vercel |
| ⚙️ **Back-end (API REST)** | [vila-cachos-ai.onrender.com](https://vila-cachos-ai.onrender.com) | Render |
| 📄 **Documentação da API (Swagger)** | [/docs](https://vila-cachos-ai.onrender.com/docs) | Render |

---

## 🏗️ Arquitetura do Sistema

```
vila-cachos-ai/
├── api.py                            # API RESTful (FastAPI) com Rate Limiting (SlowAPI)
├── recommender_engine.py             # Motor Híbrido (K-Means 8D + Knowledge-Based + Média Bayesiana)
├── generate_dataset.py               # Gerador sintético causal de perfis capilares
├── catalog.py                        # Catálogo de cosméticos e matriz de afinidade terapêutica
├── plot_metrics.py                   # Script de geração de figuras científicas (Elbow, Silhouette, Bayes)
├── dataset_historico_vila_cachos.csv  # Base de dados analítica persistente (1.000 perfis)
├── requirements.txt                  # Dependências Python para deploy (Render)
├── projeto_tcc_I.md                  # Projeto de Monografia (TCC I — Resolução nº 088/2017 IFMA)
├── documentacao_tcc.md               # Documentação acadêmica expandida (Capítulos 1, 4 e 5)
├── diario_homologacao.md             # Registro de UAT com o cliente (Vila Cachos)
├── roteiro_homologacao.md            # Roteiro de testes enviado ao cliente
├── fig_elbow_method.png              # Figura: Método do Cotovelo (k ótimo)
├── fig_silhouette.png                # Figura: Coeficiente Silhouette por k
├── fig_bayesian_feedback.png         # Figura: Convergência Bayesiana vs. Média Simples
└── totem-ui/                         # Aplicação Front-end SPA (React + Vite + Tailwind CSS)
    ├── src/App.jsx                   # Componente principal (wizard, dark mode, timeout)
    ├── src/index.css                 # Estilos globais com suporte a dark mode
    ├── .env                          # Variável de ambiente VITE_API_URL
    └── package.json                  # Dependências do Front-end (Vercel)
```

---

## 🧠 Camadas do Motor de IA

1. **Recomendação Baseada em Conhecimento (*Knowledge-Based*):**
   Mapeia queixas capilares (ressecamento, alta porosidade, transição, etc.) com formulações e ativos dos cosméticos através de uma matriz de afinidade terapêutica.

2. **Segmentação de Personas (*K-Means*):**
   Espaço vetorial de 8 dimensões normalizado via `StandardScaler`, agrupando clientes em 4 arquétipos validados por Silhouette Score (0,2185) e Método do Cotovelo.

3. **Aprendizado Contínuo (*Feedback Loop Bayesiano*):**
   Recalibra os *rankings* de produtos a partir de avaliações pós-atendimento (1 a 5 ⭐) com Média Bayesiana Amortecida (*C = 10*), protegendo contra flutuações estatísticas em amostras pequenas.

4. **Explicabilidade (*XAI*):**
   Cada indicação é acompanhada de uma justificativa clara gerada dinamicamente em linguagem natural, promovendo transparência algorítmica.

---

## 🛡️ Features de Nível Corporativo

| Feature | Implementação | Detalhes |
| :--- | :--- | :--- |
| **Rate Limiting** | `SlowAPI` (FastAPI) | Limite de 10 requisições/min por IP nas rotas `/recommend` e `/feedback`. Resposta HTTP 429 para requisições excedentes, mitigando ataques DoS e uso abusivo por bots. |
| **Sanitização de Console** | Produção (Vite build) | Mensagens de depuração, *stack traces* e dados internos são suprimidos no ambiente de produção, impedindo inspeção via DevTools. |
| **Dark Mode Nativo** | Tailwind CSS (`darkMode: 'class'`) | Alternância via botão de toggle (ícones Sol/Lua). Transição completa de toda a paleta visual. Reduz fadiga visual em ambientes com iluminação controlada. |
| **Inactivity Timeout** | `useEffect` global (React) | Timer de 15 minutos monitorando `click`, `touchstart`, `mousemove` e `keydown`. Após inatividade, executa reset automático para a tela inicial, garantindo privacidade e continuidade de atendimento. |

---

## 🚀 Como Executar Localmente

### 1. Back-end (FastAPI)

```bash
# Instale as dependências
pip install -r requirements.txt

# Inicie a API
uvicorn api:app --reload --port 8000
```
Documentação interativa (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Front-end (React + Vite)

```bash
cd totem-ui

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```
Acesse no navegador: [http://localhost:5173](http://localhost:5173)

> **Nota:** A variável `VITE_API_URL` no arquivo `totem-ui/.env` aponta para `http://127.0.0.1:8000` por padrão. Na Vercel, essa variável é configurada para o endpoint do Render.

---

## ☁️ Deploy em Nuvem

| Serviço | Configuração |
| :--- | :--- |
| **Render (Back-end)** | Build: `pip install -r requirements.txt` · Start: `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| **Vercel (Front-end)** | Root Directory: `totem-ui` · Framework Preset: `Vite` · Env: `VITE_API_URL=https://vila-cachos-ai.onrender.com` |

---

## 📚 Documentação Acadêmica

- [`projeto_tcc_I.md`](projeto_tcc_I.md) — Projeto de Monografia (TCC I, Resolução nº 088/2017 IFMA)
- [`documentacao_tcc.md`](documentacao_tcc.md) — Capítulos expandidos da monografia (Introdução, Requisitos Não-Funcionais, Resultados)
- [`diario_homologacao.md`](diario_homologacao.md) — Registro de UAT com o salão Vila Cachos
- [`roteiro_homologacao.md`](roteiro_homologacao.md) — Roteiro de testes para homologação com o cliente

---

## 📄 Licença
Projeto acadêmico desenvolvido como Trabalho de Conclusão de Curso no IFMA. Uso restrito ao contexto educacional e ao salão Vila Cachos.
