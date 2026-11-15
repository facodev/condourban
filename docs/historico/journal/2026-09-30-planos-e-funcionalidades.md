# Journal — planos e funcionalidades habilitáveis

**Data:** 2026-09-30

## O que foi feito

- Modelo de **entitlement** SaaS documentado (sem implementar produto): catálogo `funcionalidade`, `plano`, `plano_funcionalidade`, `assinatura`, override `condominio_funcionalidade`.
- Função `funcionalidade_habilitada(condo, codigo)` como contrato de resolução (núcleo → override → plano).
- Seed dos tiers ilustrativos (Starter / Essencial / Acesso / Administradora) alinhados ao doc 17.
- ADR-011, spec, FAQ; personalização: branding no JSONB, módulos on/off nas tabelas SaaS.
- **Higiene contínua** no planejamento: itens **R1–R8** (refactoring, limpeza de obsoleto/duplicado) no roadmap 03 + seção em boas práticas 01.

## Arquivos

- `docs/sql/008-saas-planos-e-funcionalidades.sql`
- `docs/sql/009-seed-planos-e-funcionalidades.sql`
- `docs/decisoes/ADR-011-planos-e-funcionalidades.md`
- `docs/funcionalidades/planos-e-funcionalidades.md`
- `docs/conteudo/faq/planos-saas.md`
- `docs/plano/03-roadmap-e-entregas.md` (§ Higiene contínua)
- `docs/plano/01-boas-praticas-e-funcionalidades.md` (§ Refactoring)

## Próximo

- Quando o código nascer: expor rotas (`/saas/...`, `/condominio/funcionalidades`) e guards Angular; aplicar R1–R8 desde o primeiro spike.
- Fechar valores comerciais reais no checklist do doc 17 §6.
