# ADR-012: Backend FastAPI para a fundação

- **Status:** Aceito (Consolidado no [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md))
- **Data:** 2026-10-01 (Revisado em 2026-10-17)
- **Relacionado:** [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md), [ADR-005](ADR-005-persistencia-sqlite-para-postgres.md)
- **Autores:** Arquitetura de Backend

## Contexto

Com a stack Python + Angular formalizada no [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md), restava consolidar a escolha entre **FastAPI** e **Django + DRF** para a API principal da plataforma.

## Decisão

1. **FastAPI como Framework Oficial de API**:
   - Assíncrono nativo (`asyncio`), ideal para alto throughput de I/O, streaming de eventos e webhooks de controle de acesso/IoT.
   - Tipagem rigorosa com **Pydantic v2** e integração fluida com **SQLAlchemy 2.0** assíncrono.
   - Geração automática e em tempo de execução da especificação **OpenAPI 3.1** (`/api/v1/openapi.json`), servindo de contrato para o frontend Angular.
   - Arquitetura limpa estruturada por módulos de domínio em `backend/app/modulos/` (9 Bounded Contexts).
   - Usar sempre a skill fastapi para auxiliar no desenvolvimento.
2. **Descarte de Django + DRF**:
   - Descartado devido ao overhead de um ORM primordialmente síncrono e rigidez de admin que não se alinha ao isolamento nativo multi-tenant com Row-Level Security (RLS) no PostgreSQL.

## Consequências

- A decisão está integrada canonicamente na fundação tecnológica descrita no [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md).
- Menor consumo de memória e latência mínima nas rotas de autenticação, portaria e acesso.

## Referências

- [ADR-001: Governança e Stack Tecnológica](ADR-001-documentacao-e-stack-tecnologica.md)
- [docs/decisoes/Estrutura.md](Estrutura.md) — Árvore de módulos do Backend FastAPI
