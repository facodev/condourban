# AGENTS.md — Guia de Engenharia e Operação para Agentes de IA

Instruções canônicas para agentes autônomos de IA e desenvolvedores que operam no monorepo **CondoUrban** (plataforma modular de gestão condominial multi-tenant).

---

## 1. Stack Tecnológica Canônica

| Camada | Tecnologia | Detalhes Operacionais |
| :--- | :--- | :--- |
| **Backend API** | Python 3.11+ / FastAPI | Rotas assíncronas (`async def`), injeção de dependências (`Depends`), Pydantic v2. |
| **ORM & Migrations** | SQLAlchemy 2.0 (async) + Alembic | Consultas assíncronas e controle transacional multi-tenant. |
| **Banco de Dados** | PostgreSQL 16+ (Prod) / SQLite (Dev) | Prod com Row-Level Security (RLS) via `condominio_id`; SQLite para desenvolvimento rápido local. |
| **Frontend Web/PWA** | Angular 22+ (TypeScript) | Standalone Components (3 arquivos separados: `.ts`, `.html`, `.scss`), Signals, Lazy Loading por Bounded Context, Angular Material 3 (`--mat-sys-*`) + Tailwind CSS v4 CSS-first (`@theme`, `@utility`, sem `tailwind.config.js`). |
| **Autenticação** | JWT Próprio + Google OAuth 2.0 | Tokens com claims (`sub`, `papeis`, `condominio_id`); sem dependência de Keycloak/IdP externo. |
| **IoT / Hardware** | Adapter Pattern (`AccessControlProvider`) | Chaves de idempotência (`Idempotency-Key`) e filas para sincronização assíncrona tolerante a falhas. |

---

## 2. Mapa dos 9 Bounded Contexts

O código-fonte organiza-se estritamente de acordo com o [ADR-013](docs/decisoes/ADR-013-organizacao-diretorios.md) em **9 Bounded Contexts** (e camada Transversal):

| # | Bounded Context | Backend (`backend/app/modules/`) | Frontend (`frontend/src/app/features/`) | Responsabilidade Central |
| :-: | :--- | :--- | :--- | :--- |
| **1** | [**Identidade e Cadastro**](docs/funcionalidades/01_identidade_cadastro/identidade-cadastro.md) | `identidade_cadastro/` | `identidade_cadastro/` | Pessoas, contas de usuário, perfis (RBAC), auto-onboarding, veículos e pets. |
| **2** | [**Condomínio**](docs/funcionalidades/02_condominio/condominio.md) | `condominio/` | `condominio/` | Estrutura física (blocos, unidades, garagens, áreas comuns) e branding institucional. |
| **3** | [**Controle de Acesso**](docs/funcionalidades/03_controle_acesso/controle-acesso.md) | `controle_acesso/` | `controle_acesso/` | Dispositivos IoT, biometria facial Intelbras, tags RFID e trilha forense de passagens. |
| **4** | [**Portaria**](docs/funcionalidades/04_portaria/portaria.md) | `portaria/` | `portaria/` | Guarita, atendimento unificado de visitantes/prestadores/delivery e encomendas com foto. |
| **5** | [**Reservas**](docs/funcionalidades/05_reservas/reservas.md) | `reservas/` | `reservas/` | Agendamento de áreas comuns, regras de concorrência, lista de convidados e vistorias. |
| **6** | [**Comunicação**](docs/funcionalidades/06_comunicacao/comunicacao.md) | `comunicacao/` | `comunicacao/` | Comunicados urgentes, livro unificado de ocorrências e mural comunitário com enquetes. |
| **7** | [**Governança**](docs/funcionalidades/07_governanca/governanca.md) | `governanca/` | `governanca/` | Assembleias híbridas (Lei 14.309), pautas, votação digital, atas e auditoria do sistema. |
| **8** | [**Financeiro**](docs/funcionalidades/08_financeiro/financeiro.md) | `financeiro/` | `financeiro/` | Emissão de boletos, Pix dinâmico, conciliação bancária, acordos e medições de água/gás. |
| **9** | [**Manutenção**](docs/funcionalidades/09_manutencao/manutencao.md) | `manutencao/` | `manutencao/` | Chamados corretivos com foto, ordens de serviço (OS) e cronograma PMO preventivo. |
| — | [**Transversal**](docs/funcionalidades/10_transversal_plataforma/transversal.md) | `app/core/` | `app/core/` + `shared/` | RLS, JWT, interceptors, pipes brasileiros, Service Worker PWA e entitlements SaaS. |

---

## 3. Regras Invariantes Obrigatórias

1. **Nomenclatura em pt-BR ([ADR-010](docs/decisoes/ADR-010-nomenclatura-pt-br.md)):** Tabelas, colunas, enums e DDL devem ser em português brasileiro (`snake_case`), sem acentos ou caracteres especiais (ex: `cobranca_condominial`, `inquilino`, `area_comum`).
2. **Isolamento Multi-Tenant ([ADR-006](docs/decisoes/ADR-006-isolamento-rls-postgresql.md)):** Toda query e comando de escrita opera sob o tenant ativo (`condominio_id`). Em PostgreSQL, a aplicação injeta `current_setting('app.current_condominio_id')` e o RLS barra acessos cruzados no banco.
3. **Separação Civil vs. Conta ([ADR-008](docs/decisoes/ADR-008-pessoa-e-usuario.md)):** Dados civis e LGPD pertencem à tabela `pessoa`; credenciais de login e sessões residem na tabela `usuario`. Uma pessoa física pode existir sem conta ativa.
4. **Entitlements vs. RBAC ([ADR-011](docs/decisoes/ADR-011-planos-e-funcionalidades.md)):** Papel de usuário (RBAC) e habilitação do plano (Entitlement) são ortogonais. Se um módulo não estiver ativo para o condomínio (`funcionalidade_habilitada`), o acesso é rejeitado com HTTP 403 `FEATURE_DISABLED` independentemente de ser `SINDICO`.
5. **Estrutura de 4 Arquivos no Backend ([ADR-013](docs/decisoes/ADR-013-organizacao-diretorios.md)):** Cada submódulo de negócio (`backend/app/modules/{contexto}/{submodulo}/`) deve conter estritamente:
   - `router.py`: Rotas e injeção de dependências.
   - `models.py`: Entidades SQLAlchemy 2.0.
   - `schemas.py`: Modelos Pydantic v2 (Request/Response).
   - `service.py`: Lógica de domínio e transações.
6. **Padrão de Componentes e Estilização no Frontend ([ADR-003](docs/decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md)):**
   - **Separação Estrita de Arquivos:** É proibido declarar `template` ou `styles` inline em arquivos `.component.ts`. Todo componente Angular deve utilizar arquivos externos próprios (`.component.html` via `templateUrl` e `.component.scss`/`.component.css` via `styleUrls`).
   - **Encapsulamento de Escopo (`ViewEncapsulation`):** Todo componente deve declarar `encapsulation: ViewEncapsulation.Emulated` e definir escopo explícito `:host` (`display: block` ou `display: inline-block`) para impedir vazamento de estilos.
   - **Arquitetura Tailwind CSS v4 Nativa (CSS-First):** Não utilizar nem gerar `tailwind.config.js` ou diretivas legadas `@tailwind`. Toda customização de design tokens, cores, fontes e espaçamentos deve ser feita em `frontend/src/styles.css` com `@import "tailwindcss";`, `@theme`, `@utility` e `@layer`, integrando-se às variáveis de sistema do Angular Material 3 (`--mat-sys-*`).
7. **Observância Obrigatória de Skills Especializadas:** Toda implementação de código deve consultar e seguir rigorosamente as skills canônicas:
   - **Frontend (Angular, UI/UX & Design):** Seguir obrigatoriamente as skills [`angular-developer`](.agents/skills/angular-developer/SKILL.md) (Signals, standalone, roteamento, formulários, Tailwind v4), `frontend-design` (identidade estética autoral, tipografia, hierarquia espacial e superfícies refinadas) e `web-design-guidelines` (acessibilidade ARIA, `:focus-visible`, `tabular-nums`, `text-wrap: balance`, `overscroll-behavior: contain`, `prefers-reduced-motion` e proibição de `transition: all`).
   - **Backend (FastAPI):** Seguir a skill [`fastapi`](.agents/skills/fastapi/SKILL.md) para convenções de API REST assíncrona, injeção de dependências (`Depends`), modelagem Pydantic v2 e respostas tipadas.

---

## 4. Comandos de Desenvolvimento e Testes

### Backend (Python / FastAPI)
```bash
# Execução local da API (acessível na máquina local e dispositivos da rede)
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Execução da suíte de testes
poetry run pytest

# Execução de migrações Alembic
poetry run alembic upgrade head
```

### Frontend (Angular PWA)
```bash
# Iniciar servidor de desenvolvimento (escuta em 0.0.0.0, acessível na rede local)
npm start

# Execução dos testes unitários
npm test

# Build de produção
npm run build
```

---

## 5. Rastreabilidade e Governança de Documentação

- **Especificações e Regras de Negócio:** Centralizadas em [`docs/funcionalidades/`](docs/funcionalidades/README.md).
- **Matriz de Rastreabilidade Técnica:** [`docs/funcionalidades/MAPA.md`](docs/funcionalidades/MAPA.md) mapeia specs, ADRs e DDL SQL.
- **Decisões Arquiteturais (ADRs):** [`docs/decisoes/`](docs/decisoes/README.md) e [`Estrutura.md`](docs/decisoes/Estrutura.md).
- **Rituais de Modificação:** Ao criar ou alterar funcionalidades, modelos ou rotas, atualize a respectiva spec em `docs/funcionalidades/`, a matriz `MAPA.md` e adicione uma nota no [`docs/historico/CHANGELOG.md`](docs/historico/CHANGELOG.md).
