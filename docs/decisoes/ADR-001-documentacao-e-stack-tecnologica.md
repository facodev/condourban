# ADR-001: Governança de documentação e stack tecnológica definitiva

- **Status:** Aceito
- **Data:** 2026-09-29 (Consolidado e unificado em 2026-10-17)
- **Substitui e unifica:** ADR-001 original (documentação e stack inicial legada) e ADR-002 (stack Python + Angular); incorpora a decisão do backend FastAPI de ADR-012.
- **Autores:** Arquitetura e Engenharia de Software

## Contexto

O sistema de gestão condominial é um produto B2B SaaS de missão crítica, multi-tenant e multi-perfil (morador, portaria, síndico, administradora e conselho). O projeto engloba 9 Bounded Contexts com regras fiscais, bancárias, segurança física e controle de acesso biométrico/IoT.

Para garantir longevidade, rastreabilidade e produtividade contínua entre sessões e desenvolvedores (humanos e agentes de IA), foi necessário:
1. Estabelecer regras claras de governança e documentação versionada no Git.
2. Definir uma **stack tecnológica única, canônica e definitiva**, eliminando qualquer indefinição técnica ou hipóteses provisórias legadas (ex: Next.js/NestJS ou dúvidas entre Django e FastAPI).

## Decisão

### 1. Governança de Documentação Versionada

Toda a inteligência do projeto é mantida no repositório de código, organizada da seguinte forma:
- `docs/decisoes/`: Architecture Decision Records (ADRs) numerados seguindo o formato padrão.
- `docs/dominios/`: Modelagem estratégica e tática dos 9 Bounded Contexts em português brasileiro (`MAPA.md`, `identidade-cadastro.md`, `condominio.md`, etc.).
- `docs/decisoes/Estrutura.md`: Organização padronizada de diretórios do backend e frontend.
- `docs/plano/`: Roadmap, requisitos de negócio e especificações funcionais.
- `docs/historico/`: Registro cronológico de mudanças (`CHANGELOG.md`) e journals de desenvolvimento.

### 2. Stack Tecnológica Definitiva

| Camada / Componente | Tecnologia Escolhida | Papel no Projeto | Justificativa Técnica |
| :--- | :--- | :--- | :--- |
| **Frontend Web / Mobile** | **Angular 22+ (TypeScript)** | Single Page Application (SPA) e Progressive Web App (PWA com `@angular/service-worker`) | Arquitetura opinionated, tipagem rigorosa, roteamento robusto por módulos/guards RBAC, formulários reativos para fluxos complexos de condomínio. |
| **UI & Design System** | **Angular Material + Tailwind CSS** | Componentes densos estruturais + utilitários de estilização | Angular Material para tabelas acessíveis, diálogos, formulários e status badges; Tailwind CSS para design tokens e flexibilidade de layout responsivo. |
| **Backend API** | **Python 3.14+ com FastAPI** | API REST assíncrona de alta performance | I/O assíncrono nativo para streaming e integrações de hardware, validação estrita com Pydantic v2, documentação OpenAPI nativa e tipada. |
| **ORM & Migrations** | **SQLAlchemy 2.0 + Alembic** | Mapeamento relacional e controle de versão de schema | Suporte robusto a queries assíncronas, abstração de engine e controle fino de transações multi-tenant. |
| **Banco de Dados (Produção)** | **PostgreSQL 16+** | Armazenamento relacional multi-tenant com Row-Level Security (RLS) | Confiabilidade, suporte a tipos ricos (`UUID`, `JSONB`), e isolamento nativo de condomínios no banco via `condominio_id`. |
| **Banco de Dados (Dev/Testes)** | **SQLite (`dev.db` / `:memory:`)** | Desenvolvimento local ágil e suíte de testes unitários | Inicialização instantânea sem necessidade de containers Docker pesados no dia a dia do desenvolvimento local. |
| **Autenticação & Sessão** | **JWT Próprio + Google OAuth 2.0** | Autenticação na própria aplicação (sem Keycloak) | Tokens de acesso e refresh leves emitidos pela API; suporte duplo a e-mail/senha criptografada e login social "Entrar com Google" (Gmail). |
| **Filas & Tarefas Assíncronas** | **Celery + Redis** | Processamento em segundo plano e agendamento | Geração assíncrona de boletos e relatórios, reconciliação bancária, disparos de notificações em massa e sincronização com hardware. |
| **Armazenamento de Mídias** | **S3-Compatible Storage** | Armazenamento de arquivos (MinIO em dev; AWS S3/Cloudflare R2 em produção) | Fotos de moradores/veículos, comprovantes financeiros, atas de assembleia e arquivos da portaria. |
| **Contrato de API** | **OpenAPI 3.1** | Contrato unificado entre backend e frontend | Gerado nativamente pelo FastAPI em `/api/v1/openapi.json`, garantindo sincronia perfeita com os clientes Angular. |
| **Integração de Hardware/IoT** | **Adapter Pattern (`AccessControlProvider`)** | Integração desacoplada de catracas e leitoras faciais (ex: Intelbras) | Isolamento das regras de hardware no backend, com chaves de idempotência e filas de retentativa com fallback. |

### 3. Organização Arquitetural em Bounded Contexts

Tanto o backend quanto o frontend organizam seu código estritamente ao redor dos **9 Bounded Contexts** estabelecidos em `docs/decisoes/Estrutura.md`:
1. `identidade_cadastro`: Pessoas, usuários, moradores, veículos, animais e onboarding.
2. `condominio`: Estrutura física, blocos, unidades e áreas comuns.
3. `controle_acesso`: Dispositivos, credenciais (tags/biometria) e logs de passagem.
4. `portaria`: Atendimento na guarita, visitantes, prestadores e encomendas.
5. `reservas`: Agendamento de áreas comuns, termos e convidados.
6. `comunicacao`: Murais de avisos, ocorrências e notificações push.
7. `governanca`: Assembleias virtuais, votações e atas/documentos.
8. `financeiro`: Boletos, conciliação bancária e prestação de contas.
9. `manutencao`: Chamados preventivos/corretivos e vistorias.

## Alternativas Consideradas e Rejeitadas

1. **Next.js Full-Stack (Node.js)** — Descartado: Menor maturidade para integrações densas de hardware brasileiro, rotinas pesadas de conciliação financeira e separação estrita de camadas corporativas.
2. **Django + Django REST Framework** — Descartado: Embora maduro, traz overhead de ORM/Admin tradicional que dificulta I/O assíncrono nativo e personalizações profundas de multi-tenancy com RLS e FastAPI já oferece OpenAPI de primeira classe.
3. **Keycloak / Auth0 / IdP Externo** — Descartado: Complexidade operacional e custo desnecessários para a fase do produto; JWT na própria API com OAuth Google resolve 100% dos requisitos de segurança com baixo overhead.
4. **App Nativo Inicial (React Native / Flutter)** — Postergado: O PWA oficial em Angular atende integralmente moradores e portaria na web e celular sem necessidade de aprovação imediata em lojas (publicação em lojas via Capacitor reservada para fase futura).

## Consequências

### Positivas
- **Fim da ambiguidade técnica**: Toda a equipe, documentação e geradores de IA trabalham sobre a mesma stack oficial.
- **Portabilidade total**: App roda em qualquer navegador moderno (Chrome, Safari iOS, Edge, Firefox) sem lock-in de sistema operacional.
- **Isolamento e Segurança**: Multi-tenancy nativo com RLS no PostgreSQL e autorização RBAC centralizada.
- **Alta testabilidade**: Desenvolvimento e testes unitários locais rodam instantaneamente com SQLite.

### Riscos e Mitigações
- **Dois runtimes (Python + TypeScript)**: Mitigado pela padronização do contrato OpenAPI 3.1 e pela estrutura espelhada de domínios entre backend e frontend.
- **Sync de Hardware**: Mitigado pelo uso de filas Celery e chaves de idempotência para tolerar oscilações de rede em condomínios.

## Referências

- [docs/decisoes/Estrutura.md](Estrutura.md) — Árvore canônica de diretórios do Backend e Frontend
- [ADR-003: UI e Portabilidade](ADR-003-ui-estilizacao-e-portabilidade-web.md)
- [ADR-005: Persistência SQLite para PostgreSQL](ADR-005-persistencia-sqlite-para-postgres.md)
- [ADR-006: Isolamento RLS no PostgreSQL](ADR-006-isolamento-rls-postgresql.md)
- [ADR-007: Autenticação JWT e Google OAuth](ADR-007-autenticacao-jwt-aplicacao.md)
- [ADR-008: Separação de Pessoa e Usuário](ADR-008-pessoa-e-usuario.md)
- [ADR-010: Nomenclatura em pt-BR](ADR-010-nomenclatura-pt-br.md)
- [docs/funcionalidades/MAPA.md](../funcionalidades/MAPA.md) — Mapa dos Bounded Contexts
