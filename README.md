# 🌿 Vila Cachos AI — Motor Híbrido de Recomendação Capilar

Projeto de TCC (Sistemas de Informação — IFMA Campus Monte Castelo) desenvolvido para o salão especializado **Vila Cachos** (São Luís - MA).

O sistema resolve o problema de **Cold Start** em salões especializados através de um Motor Híbrido de Inteligência Artificial com **XAI (Explicabilidade)** e **Feedback Loop Bayesiano**, consumido por uma aplicação interativa de autoatendimento (**Totem UI**).

---

## 🏗️ Arquitetura do Sistema

```
vila-cachos-ai/
├── api.py                            # API RESTful em FastAPI com validação estrita (Pydantic)
├── recommender_engine.py             # Motor Híbrido (K-Means 8D + Knowledge-Based + Média Bayesiana)
├── generate_dataset.py               # Gerador sintético causal de perfis e histórico
├── catalog.py                        # Catálogo oficial de cosméticos e matriz de afinidade
├── dataset_historico_vila_cachos.csv # Base de dados analítica persistente
├── requirements.txt                  # Dependências Python para deploy (Render)
├── totem-ui/                         # Aplicação Front-end SPA em React + Vite + Tailwind CSS
│   ├── src/                          # Telas de boas-vindas, anamnese diagnóstica e recomendações
│   └── package.json                  # Dependências do Front-end (Vercel)
└── documentacao_tcc.md               # Documentação acadêmica e capítulos da monografia
```

---

## 🧠 Camadas do Motor de IA

1. **Recomendação Baseada em Conhecimento (*Knowledge-Based*):**
   - Mapeia queixas do diagnóstico capilar (ressecamento, alta porosidade, transição, etc.) com formulações e ativos dos cosméticos.
2. **Segmentação de Personas (*K-Means*):**
   - Espaço vetorial de 8 dimensões normalizado via `StandardScaler`, agrupando clientes em 4 arquétipos do salão.
3. **Aprendizado Contínuo (*Feedback Loop Bayesiano*):**
   - Recalibra as notas dos produtos a partir de avaliações pós-atendimento (1 a 5 estrelas) com média ponderada amortecida, evitando ruídos de amostras pequenas.
4. **Explicabilidade (*XAI*):**
   - Cada indicação é acompanhada de uma justificativa clara gerada dinamicamente para a cliente no Totem.

---

## 🚀 Como Executar Localmente

### 1. Back-end (FastAPI)

```bash
# Instale as dependências
pip install -r requirements.txt

# Inicie a API
uvicorn api:app --reload --port 8000
```
Documentação interativa do Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Front-end Totem (React + Vite)

```bash
# Acesse a pasta do front-end
cd totem-ui

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```
Acesse a aplicação no navegador em: [http://localhost:5173](http://localhost:5173)

---

## ☁️ Deploy em Nuvem

- **Back-end (Render.com):**
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Front-end (Vercel):**
  - **Root Directory:** `totem-ui`
  - **Framework Preset:** Vite
