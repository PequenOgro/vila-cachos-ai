# ADR-001: Desacoplamento de Persistência (DIP) e Modularização de Rotas (APIRouter)

## Status
Accepted

## Context
- **Problema**: O backend apresentava acoplamento direto entre os controladores web (`api.py`) e a persistência em arquivo CSV, além de um arquivo `api.py` monolítico (>350 linhas) concentrando lógica de roteamento, serialização, rate limiting e instanciação de modelos.
- **Restrições**: Manter 100% de retrocompatibilidade com o deploy no Render (`uvicorn api:app`), os testes automatizados existentes (`test_api.py`) e o frontend (`totem-ui`).

## Options Considered
| Opção | Prós | Contras | Complexidade |
|---|---|---|---|
| **Opção A: Repository Pattern + APIRouter (Modular)** | Mantém compatibilidade total com CSV atual e Render; desacopla rotas e I/O; reduz `api.py` para <90 linhas; segue Clean Architecture e DDD. | Exige criação de pacotes `repositories/`, `routers/` e `schemas/`. | Baixa / Média |
| **Opção B: Migração Imediata para SQLite/PostgreSQL** | Maior robustez transacional com ACID nativo. | Quebra o fluxo baseado no dataset CSV histórico e adiciona dependências externas ou migrações de schema. | Alta |
| **Opção C: Manter Monólito `api.py`** | Zero alteração estrutural. | Viola o princípio de responsabilidade única (SRP), dificulta testes unitários e ultrapassa limites de tamanho de arquivo recomendados. | Nula |

## Decision
Adotou-se a **Opção A**:
1. Criação do contrato abstrato `FeedbackRepository` e implementação concreta `CsvFeedbackRepository` em `repositories/feedback_repository.py`.
2. Decomposição das rotas do FastAPI em 4 submódulos sob `routers/`:
   - `routers/health.py`: Status e métricas operacionais.
   - `routers/catalog.py`: Consulta a produtos e taxonomia.
   - `routers/recommendation.py`: Geração de recomendações e ciclo de feedback.
   - `routers/vision.py`: Diagnóstico visual via YOLO e morfologia.
3. Centralização dos contratos de dados em `schemas/`.
4. Redução de `api.py` a um orquestrador limpo de <90 linhas.

## Rationale
- **Dependency Inversion Principle (DIP)**: A camada de recomendação e a API dependem de abstrações, permitindo que a troca do backend de dados (CSV para PostgreSQL ou Supabase) no futuro não exija modificações nas rotas ou no motor de recomendação.
- **Single Responsibility Principle (SRP)**: Cada submódulo possui uma responsabilidade única e bem definida.
- **Early Return & Testabilidade**: Testes unitários para o repositório agora podem rodar isoladamente sem subir o servidor HTTP.

## Consequences
- **Positive**:
  - Código limpo, extensível e 100% alinhado com Clean Architecture e DDD.
  - Zero erros em testes de integração (`test_api.py`) e testes de repositório (`test_repository.py`).
  - Redução drástica da complexidade cognitiva ao auditar o código.
- **Negative**:
  - Aumento na quantidade de arquivos no repositório.
- **Mitigation**:
  - Árvore de diretórios padronizada e documentada em `docs/architecture/SOFTWARE_ARCHITECTURE.md`.

## Revisit Trigger
- Quando a aplicação migrar para banco de dados relacional (ex: PostgreSQL/Supabase) ou exigir persistência distribuída em múltiplos nós.
