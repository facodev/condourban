# Journal — documentação por bounded context

**Data:** 2026-09-30

## O que foi feito

Criada a pasta `docs/dominios/` como **camada de navegação** por bounded context, sem apagar planos, specs, SQL ou ADRs.

Cada domínio agrega: responsabilidade, entidades/SQL, specs, ADRs, API, roadmap, decisões, FAQ e dependências.

## Arquivos

- `docs/dominios/README.md` — índice
- `docs/dominios/MAPA.md` — rastreabilidade completa (specs/ADRs/SQL/planos)
- `docs/dominios/_transversal.md`
- Um `.md` por domínio: identity-tenancy, access, amenities, communication, documents, tickets, governance, finance, saas, audit-usage, community, iot, content-public, intelligence

## Política

Hubs **indexam**; fontes canônicas de regra fina continuam em `funcionalidades/`, `decisoes/`, `sql/`, `plano/`.
