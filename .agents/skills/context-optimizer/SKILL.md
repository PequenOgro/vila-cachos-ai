---
name: context-optimizer
description: Transforms informal developer requests into high-density, structured technical prompts optimized for autonomous execution in Antigravity. Use when prompt optimization, implementation briefing, or context enrichment is needed, or when the user mentions @otimizador.md or asks to structure a raw task.
license: MIT
metadata:
  version: "1.0.0"
  author: Marcos Vinícius
---

# Antigravity Context Optimizer & Prompt Engineer

Esta skill atua como um otimizador de contexto para o ambiente Antigravity IDE. Ela intercepta requisições informais ou de alto nível e as expande em diretrizes técnicas de alta densidade em Markdown, acionando ferramentas nativas, servidores MCP e testes automatizados antes da geração de código.

## Quando Utilizar
- Ao receber pedidos informais ou instruções curtas do usuário para refatorações ou novas features.
- Quando o usuário mencionar `@otimizador.md` ou solicitar a transformação de uma ideia em um plano técnico executável.
- Para planejar tarefas complexas nos projetos **Vila Cachos** ou **IntraCAEMA**.

## Estrutura do Prompt de Saída

Ao otimizar uma requisição, produza um briefing estruturado contendo:

### 1. 🎯 Objetivo Central
Frase concisa e inequívoca definindo a modificação arquitetural, refatoração ou funcionalidade a ser implementada.

### 2. 📂 Mapeamento de Contexto (Filesystem & Terminal)
- **Arquivos-alvo prováveis**: Lista de caminhos absolutos ou relativos a inspecionar/alterar.
- **Protocolo de Leitura Prévia**: Instrução explícita para ler os arquivos e módulos afetados (`read_file`, `grep`, comandos de terminal) ANTES de propor qualquer modificação.

### 3. ⚙️ Ferramentas e MCPs a Acionar
- **Terminal / Execução de Comandos**: Comandos de build, linters e suíte de testes do ecossistema.
- **Database (PostgreSQL / SQL MCP)**: Inspeção de tabelas, índices e migrações prévias caso envolva persistência.
- **Git**: Verificação de branch atual e status limpo antes de iniciar.
- **MCPs de Navegador (Playwright / Chrome DevTools)**: Inspeção visual e validação de fluxos UI quando aplicável.

### 4. 🚧 Restrições de Stack e Arquitetura
- **Vila Cachos (TCC)**: Frontend React (Vite/Tailwind) + Backend Python (FastAPI/ONNX/scikit-learn). Teto estrito de memória de 512MB RAM (Render), conformidade com as diretrizes do `AGENTS.md`.
- **IntraCAEMA**: Frontend React + Backend Spring Boot (Java) + PostgreSQL.
- **Princípios Gerais**: Zero regressão, lazy loading, tipagem estrita, performance e fechamento de buffers/recursos.

### 5. ✅ Critérios de Validação e Conclusão (Definition of Done)
- Comandos exatos para validação (ex: `python test_api.py`, `npm run build`, `npm run lint`, `mvn test`).
- Critério de tolerância zero a erros (Exit Code 0 em todos os testes e builds).

