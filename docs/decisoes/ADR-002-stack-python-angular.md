# ADR-002: Stack Python (backend) + Angular (frontend)

- **Status:** Fundido / Consolidado no [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md)
- **Data original:** 2026-09-29
- **Data de consolidação:** 2026-10-17
- **Referência definitiva:** [ADR-001: Governança de documentação e stack tecnológica definitiva](ADR-001-documentacao-e-stack-tecnologica.md)

## Nota de Consolidação

As deliberações técnicas sobre a escolha de **Python (FastAPI)** para o backend e **Angular** para o frontend foram unificadas no **[ADR-001](ADR-001-documentacao-e-stack-tecnologica.md)**.

Todas as alternativas preliminares (Next.js, NestJS e Django) foram avaliadas e descartadas, estabelecendo-se uma especificação canônica única para todo o projeto:
- **Frontend:** Angular 22+ (TypeScript) SPA/PWA com Angular Material e Tailwind CSS.
- **Backend:** FastAPI + SQLAlchemy 2.0 assíncrono + Pydantic v2 + OpenAPI 3.1.
- **Dados & Infra:** PostgreSQL com RLS (produção) / SQLite (dev e testes), Celery + Redis, S3-compatible.
- Usar sempre a skill `fastapi` para auxiliar no desenvolvimento do backend.
- Usar sempre a skill `angular-developer` para auxiliar no desenvolvimento do frontend.

Consulte o [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md) para os detalhes completos e vigentes.
