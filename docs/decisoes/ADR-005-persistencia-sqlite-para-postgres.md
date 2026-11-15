# ADR-005 — Persistência: começar leve (memória/SQLite) e evoluir para PostgreSQL

## Status

Aceito — 2026-09-29

## Contexto

No início do desenvolvimento queremos **velocidade** (sem subir PostgreSQL/Redis/Celery obrigatórios no dia 1), sem abandonar o modelo de dados e os **domínios** já definidos. O stakeholder pediu banco **em memória** para crescer depois.

`:memory:` puro some a cada reinício do processo e **não compartilha** entre workers — útil em **testes**, frágil para demo contínua.

## Decisão

1. **Abstração desde o dia 1:** ORM (**SQLAlchemy 2.0** assíncrono) + migrations versionadas com **Alembic**. Troca de engine = configuração (`DATABASE_URL`), sem rewrite.
2. **Escada de persistência:**

| Estágio | Engine | Quando |
|---------|--------|--------|
| Testes unitários | SQLite `:memory:` | CI / pytest |
| Dev local / spike / demo cedo | **SQLite arquivo** (`dev.db`) — “quase memória”, zero ops | Até haver necessidade multi-processo ou staging |
| Staging / produção / multi-tenant real | **PostgreSQL** | Antes de dados reais de condomínio / Intelbras sync |
| Cache / rate-limit / filas | In-process → **Redis** (+ Celery quando jobs forem necessários) | Local: fallback in-process; produção: Redis |

3. **Não** usar banco em memória como store de produção (perda de dados, sem backup, sem isolamento sério).
4. Modelos e domínios já nascem **compatíveis com PostgreSQL** (tipos, constraints, índices); evitar SQL específico de SQLite nas regras de negócio.

## Consequências

- Fase 1.2 do roadmap: “API + persistência configurável (SQLite → PostgreSQL)”, não “só PostgreSQL”.
- Docker Compose: perfil `dev` (SQLite ou Postgres opcional) e perfil `prod` (Postgres + Redis).
- Documentar em `.env.example`: `DATABASE_URL` / `DB_ENGINE`.
- Revisar [02](../plano/02-arquitetura-tecnica.md) e [14](../plano/14-revisao-plano-consolidada.md).

## Alternativas rejeitadas

- Só dict/`tinydb` sem ORM — reescreveria tudo na migração.
- PostgreSQL obrigatório no primeiro commit — atrito desnecessário no spike.
- Redis como “banco” principal — não substitui relacional/multi-tenant.
