# ADR-010: Nomenclatura de negócio em pt-BR (schema)

- **Status:** Aceito (schema físico); APIs podem usar aliases
- **Data:** 2026-09-29
- **Autores:** consolidação gestao-condominio-documentacao

## Contexto

Stakeholders e SQL de referência usam termos em português (`pessoa`, `condominio`, `autorizacao_acesso`). A documentação de arquitetura também usa nomes conceituais em inglês (`User`, `AccessGrant`).

## Decisão

1. **Tabelas, enums e campos de negócio** no PostgreSQL: **português brasileiro** (snake_case).
2. Termos técnicos consolidados permanecem: `JWT`, `RLS`, `UUID`, `JSONB`, `API`, `OIDC`.
3. Documentação e código de domínio podem usar nomes EN conceituais com **glossário** em [15](../plano/15-modelo-dados-postgresql.md).
4. OpenAPI: escolher uma convenção por versão (`/api/v1`) e não misturar no mesmo recurso.

## Alternativas consideradas

1. Schema 100% inglês — desalinha com SQL já escrito e linguagem do produto PT-BR.

## Consequências

### Positivas

- DDL legível para o time de negócio/ops BR.
- Consistência com seeds e motivos de correção.

### Negativas / riscos

- Dual naming EN/PT exige glossário mantido.

## Referências

- [docs/sql/](../sql/README.md)
- [15-modelo-dados-postgresql.md](../plano/15-modelo-dados-postgresql.md)
