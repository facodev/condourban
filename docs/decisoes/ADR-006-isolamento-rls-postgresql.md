# ADR-006: Isolamento por condomínio com RLS (PostgreSQL)

- **Status:** Aceito (produção/staging Postgres); N/A em SQLite local
- **Data:** 2026-09-29
- **Autores:** consolidação gestao-condominio-documentacao

## Contexto

Dados operacionais são por condomínio. Precisamos de defesa em profundidade além de filtros na aplicação, especialmente multi-tenant na mesma base.

## Decisão

1. Tabelas operacionais possuem `condominio_id`.
2. No **PostgreSQL**, aplicar **Row Level Security** (`docs/sql/006-rls.sql`).
3. Após validar membership, a API executa `SET LOCAL app.condominio_id = '…'` na transação.
4. O `condominio_id` enviado pelo cliente **nunca** autoriza sozinho.

Em SQLite (dev), o isolamento fica só na aplicação; o mesmo modelo lógico de `condominio_id` permanece ([ADR-005](ADR-005-persistencia-sqlite-para-postgres.md)).

## Alternativas consideradas

1. Schema por condomínio — isolamento forte, ops mais caras cedo.
2. Só filtro na app — insuficiente como única linha de defesa em prod.

## Consequências

### Positivas

- Vazamento por bug de query reduzido em Postgres.
- Contrato claro com a sessão.

### Negativas / riscos

- Migrations e testes precisam ativar/desativar RLS conscientemente.
- Superuser/bypass de RLS em jobs batch exige cuidado.

## Referências

- [docs/sql/README.md](../sql/README.md)
- [15-modelo-dados-postgresql.md](../plano/15-modelo-dados-postgresql.md)
- [13-seguranca-plataforma-logs-e-ddos.md](../plano/13-seguranca-plataforma-logs-e-ddos.md)
