# Clean Architecture & Modularização Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refatorar a arquitetura do Vila Cachos AI aplicando Clean Architecture, Domain-Driven Design (DIP via Repository Pattern) e decomposição de rotas (APIRouter), além de eliminar 100% dos warnings de Fast Refresh no frontend e documentar a arquitetura via ADR.

**Architecture:** 
1. **Camada de Domínio e Persistência**: Criar `repositories/feedback_repository.py` com interface abstrata `FeedbackRepository` e implementação concreta `CsvFeedbackRepository` desacoplando I/O de disco da camada web.
2. **Camada de Apresentação/Web**: Decompor o monólito `api.py` em submódulos desacoplados sob `routers/` (`health.py`, `recommendation.py`, `catalog.py`, `vision.py`), reduzindo `api.py` para um orquestrador conciso (<80 linhas).
3. **Frontend (Totem UI)**: Ajustar componentes Radix/Shadcn para conformidade total com ESLint / React Fast Refresh.
4. **Governança**: Registrar a decisão arquitetural em `docs/architecture/adr-001-clean-architecture-persistence-and-routers.md`.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, Scikit-Learn, Pandas, Ultralytics YOLO, OpenCV, React 19, Vite, TanStack Router/Nitro, ESLint.

**Spec:** Baseado nas diretrizes das skills `software_architecture`, `senior-architect`, `clean-code`, `recsys-pipeline-architect` e regra de execução contínua `AGENTS.md`.

---

## Tasks

### Task 1: Criar Abstração de Repositório (`FeedbackRepository` e `CsvFeedbackRepository`)

**Files:**
- Create: `repositories/__init__.py`
- Create: `repositories/feedback_repository.py`
- Create: `tests/test_repository.py`

**Interfaces:**
- Produces: `FeedbackRepository(ABC)` com métodos:
  - `obter_historico() -> pd.DataFrame`
  - `salvar_feedback(perfil_cliente: dict, nome_produto: str, nota_satisfacao: int, cluster_id: int) -> None`
  - `obter_total_avaliacoes() -> int`
  - `obter_media_global() -> float`
- Produces: `CsvFeedbackRepository(FeedbackRepository)` com resolução robusta de caminho e persistência atômica.

- [ ] **Step 1: Criar teste unitário para o repositório**
- [ ] **Step 2: Executar teste e validar comportamento**
- [ ] **Step 3: Implementar `repositories/feedback_repository.py`**
- [ ] **Step 4: Executar `python -m pytest tests/test_repository.py` e validar sucesso**

---

### Task 2: Decompor Rotas em Módulos `routers/` e Refatorar `api.py`

**Files:**
- Create: `routers/__init__.py`
- Create: `routers/health.py`
- Create: `routers/catalog.py`
- Create: `routers/recommendation.py`
- Create: `routers/vision.py`
- Modify: `api.py` (decompor em orquestrador enxuto)

**Interfaces:**
- Produces: `routers.health.router`, `routers.catalog.router`, `routers.recommendation.router`, `routers.vision.router`.
- Produces: `api.app` compatível 100% com endpoints legados (`/`, `/health`, `/recommend`, `/feedback`, `/catalogo`, `/diagnostico/imagem`).

- [ ] **Step 1: Criar `routers/health.py` e `routers/catalog.py`**
- [ ] **Step 2: Criar `routers/recommendation.py` desacoplado usando `FeedbackRepository`**
- [ ] **Step 3: Criar `routers/vision.py`**
- [ ] **Step 4: Refatorar `api.py` para incluir os roteadores e inicializar dependências**
- [ ] **Step 5: Executar `python test_api.py` e comprovar 100% de sucesso**

---

### Task 3: Eliminar Warnings de Fast Refresh no Frontend (`totem-ui`)

**Files:**
- Modify: `totem-ui/src/components/ui/badge.tsx`
- Modify: `totem-ui/src/components/ui/button.tsx`
- Modify: `totem-ui/src/components/ui/toggle.tsx`
- Modify: `totem-ui/src/components/ui/form.tsx`
- Modify: `totem-ui/src/components/ui/navigation-menu.tsx`
- Modify: `totem-ui/src/components/ui/sidebar.tsx`

- [ ] **Step 1: Extrair variantes e helpers de componentes para manter arquivos exportando apenas componentes ou configurar regras de ESLint adequadamente**
- [ ] **Step 2: Executar `npm run lint` e comprovar 0 erros e 0 warnings**
- [ ] **Step 3: Executar `npm run build` e comprovar compilação sem falhas**

---

### Task 4: Criar ADR de Arquitetura e Organizar Árvore de Arquivos

**Files:**
- Create: `docs/architecture/adr-001-clean-architecture-persistence-and-routers.md`
- Create: `docs/architecture/SOFTWARE_ARCHITECTURE.md`

- [ ] **Step 1: Documentar decisões, trade-offs e limites na ADR-001**
- [ ] **Step 2: Gerar mapa arquitetural do repositório em `SOFTWARE_ARCHITECTURE.md`**
- [ ] **Step 3: Executar suíte completa de testes de ponta a ponta (`python test_api.py`, `npm run build`, `npm run lint`)**
