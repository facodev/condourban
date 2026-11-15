# Project state

## Decisions

| ID | Decision | Rationale | Status | Date |
| --- | --- | --- | --- | --- |
| AD-001 | Stack FastAPI + Angular 22+ Standalone | Desempenho assíncrono Python, tipagem Pydantic v2 e reatividade moderna com Signals (ADR-001, ADR-002) | active | 2026-10-17 |
| AD-002 | Organização por 9 Bounded Contexts | Desacoplamento de domínios, isolamento de regras e manutenibilidade modular (ADR-013, Estrutura.md) | active | 2026-10-17 |
| AD-003 | Arquitetura de 4 arquivos por submódulo | router.py, models.py, schemas.py e service.py padronizados no backend (ADR-013) | active | 2026-10-17 |
| AD-004 | Isolamento multi-tenant via condominio_id | PostgreSQL Row-Level Security (RLS) em staging/prod e escopo de sessão em dev (ADR-005, ADR-006) | active | 2026-10-17 |
| AD-005 | Separação civil pessoa vs conta usuario | Resguardo LGPD e suporte a dependentes sem credencial própria de login (ADR-008) | active | 2026-10-17 |
| AD-006 | Nomenclatura estrita em pt-BR snake_case | Termos de domínio brasileiros padronizados em tabelas, colunas e enums sem acentos (ADR-010) | active | 2026-10-17 |
| AD-007 | Ortogonalidade entre RBAC e Entitlements | Papel de usuário e licenciamento de funcionalidades são verificados de forma independente (ADR-011) | active | 2026-10-17 |
| AD-008 | Autenticação JWT Próprio + Google OAuth 2.0 | Tokens assinados com claims de tenant e perfil sem dependência de IdP externo pesado (ADR-007) | active | 2026-10-17 |
| AD-009 | Livro de ocorrências unificado | Registro centralizado com coluna origem ('MORADOR', 'PORTARIA', 'GESTAO') e sigilo (ADR-013) | active | 2026-10-17 |
| AD-010 | Reestruturação do Roadmap por 10 Fases de Bounded Context | Unificação de submódulos por Bounded Context eliminando fragmentação e estabelecendo 3 trilhas paralelas | active | 2026-10-18 |
| AD-011 | Marco 0 e Pilares Essenciais de Dados (BC-01 e BC-02) | Infraestrutura transversal consolidada como Marco 0; BC-01 e BC-02 definidos como cadastros mestres indispensáveis para as trilhas de Hardware, Social e Finanças | active | 2026-10-18 |
| AD-012 | Agente Conversacional Multicanal (PWA + WhatsApp) com RAG em pgvector e Adapter LLM | Orquestração por opções numeradas determinísticas (1..N), busca vetorial pgvector sob RLS multi-tenant, ProvedorLLM desacoplado e governança granular pelo síndico | active | 2026-10-20 |

## Handoff

**Feature**: bc-04-portaria
**Where**: Plan aprovado pelo validador em `.specs/features/bc-04-portaria/plan.md` (`validate_plan.py` 0 erros). Aguardando revisão humana.
**In progress**: TLC Spec Lean — fase PLAN concluída; sem `checks.md` ainda.
**Next step**: Após OK do humano → escrever `checks.md`, validar, build (encomendas+visitantes+UI+RBAC+pytest BC-01/02), Verifier.
**Blockers**: revisão humana do plan (defaults em Assumptions: status RECEBIDA/ENTREGUE, menu morador → encomendas).
**Uncommitted**: `.specs/features/bc-04-portaria/plan.md`, `.specs/STATE.md`
**Branch**: main
**Paused**: agente-conversacional (checks prontos, build não iniciado nesta sessão)


