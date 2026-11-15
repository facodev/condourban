# Architecture Decision Records (ADRs)

Registro de **decisões arquiteturais importantes** e seu contexto histórico, preservando a rastreabilidade técnica e os direcionamentos do produto.

## Índice

| ADR | Título | Status | Escopo |
| :---: | :--- | :---: | :--- |
| [000](ADR-000-template.md) | Template de ADR | — | Modelo padrão de documentação de decisões |
| [001](ADR-001-documentacao-e-stack-tecnologica.md) | **Governança de documentação e stack tecnológica definitiva** | **Aceito** | Unifica governança de docs e a stack canônica (Angular + FastAPI + PostgreSQL/SQLite + Celery/Redis) |
| [002](ADR-002-stack-python-angular.md) | Stack Python + Angular | *Fundido no ADR-001* | Consolidação das decisões de stack definitiva |
| [003](ADR-003-ui-estilizacao-e-portabilidade-web.md) | **UI, Design System e Portabilidade Web (PWA)** | **Aceito** | Angular Material (app denso) + Tailwind CSS + PWA |
| [004](ADR-004-integracao-intelbras-facial.md) | **Integração Intelbras (facial) + pré-cadastro** | **Aceito** | Padrão Adapter (`AccessControlProvider`), sync assíncrono e fallbacks |
| [005](ADR-005-persistencia-sqlite-para-postgres.md) | **Persistência SQLite para PostgreSQL** | **Aceito** | Escada de persistência: SQLite em dev/testes e PostgreSQL em prod com SQLAlchemy 2.0 |
| [006](ADR-006-isolamento-rls-postgresql.md) | **Isolamento por condomínio com RLS (PostgreSQL)** | **Aceito** | Segurança multi-tenant em profundidade no banco via `SET LOCAL app.condominio_id` |
| [007](ADR-007-autenticacao-jwt-aplicacao.md) | **Autenticação JWT na aplicação (e-mail/senha + Google OAuth)** | **Aceito** | Emissão própria de JWT/refresh, suporte ao Gmail e dispensa de Keycloak/IdP externo |
| [008](ADR-008-pessoa-e-usuario.md) | **Separação de Pessoa e Usuário** | **Aceito** | Desacoplamento entre identidade cadastral de negócio (`pessoa`) e credencial de login (`usuario`) |
| [009](ADR-009-idempotencia-integracoes.md) | **Idempotência em integrações e webhooks** | **Aceito** | Header `Idempotency-Key` e tabela de sync para tolerância a retentativas de hardware |
| [010](ADR-010-nomenclatura-pt-br.md) | **Nomenclatura de negócio em pt-BR (schema físico)** | **Aceito** | Tabelas, enums e colunas em português brasileiro (snake_case) |
| [011](ADR-011-planos-e-funcionalidades.md) | **Planos SaaS e funcionalidades habilitáveis** | **Aceito** | Modelo comercial de planos, assinaturas e overrides por condomínio (`funcionalidade_habilitada`) |
| [012](ADR-012-backend-fastapi.md) | Backend FastAPI para a fundação | *Consolidado no ADR-001* | Adoção do FastAPI como framework assíncrono oficial |
| [013](ADR-013-organizacao-diretorios.md) | **Organização de Diretórios por Bounded Contexts e Consolidação de Subdomínios** | **Aceito** | Estruturação dos 9 Bounded Contexts em pt-BR e consolidação para 2-4 subdomínios |

## Status Possíveis

- **Aceito** — Decisão vigente e ativa na arquitetura.
- **Fundido / Consolidado** — Decisão absorvida por outro ADR unificador.
- **Proposto** — Em avaliação / discussão técnica.
- **Substituído** — Supersedido formalmente por um ADR mais recente.
- **Obsoleto** — Não mais aplicável ao projeto.

## Como Criar um Novo ADR

1. Copie `ADR-000-template.md` para `ADR-NNN-titulo-kebab.md`.
2. Preencha Contexto, Decisão, Alternativas e Consequências.
3. Atualize este arquivo `README.md` com a nova entrada.
4. Referencie o ADR nos documentos afetados (`docs/plano/`, `docs/funcionalidades/` ou `Estrutura.md`).
5. Registre a adição no `docs/historico/CHANGELOG.md`.
