# Fundações Transversais do Sistema (`transversal`)

Este documento detalha as capacidades técnicas, de infraestrutura, segurança e arquitetura que operam transversalmente em todos os 9 bounded contexts do CondoUrban.

---

## 1. Segurança e Isolamento Multi-Tenancy (RLS)

O sistema adota isolamento de dados a nível de banco de dados no **PostgreSQL** por meio de **Row Level Security (RLS)**:
- Toda requisição autenticada injeta o contexto do condomínio ativo (`current_setting('app.current_condominio_id')`).
- Políticas RLS ativas impedem que qualquer consulta ou comando de escrita acesse dados pertencentes a outro condomínio, mesmo em caso de falha de filtro a nível de aplicação.
- Superadministradores possuem bypass auditado exclusivamente para manutenção de plataforma.

Referência técnica: [ADR-006: Isolamento por condomínio com RLS no PostgreSQL](../../decisoes/ADR-006-isolamento-rls-postgresql.md).

---

## 2. Autenticação e Sessões (JWT + Google OAuth2)

- **Backend**: Criptografia de senhas usando `bcrypt`, emissão de tokens de acesso JWT de curta duração (Access Token) com reivindicações de identidade (`sub`, `papeis`, `condominio_id`) e Refresh Tokens seguros persistidos para renovação de sessão. Suporte nativo a Single Sign-On (SSO) com **Google Identity**.
- **Frontend**: `token.interceptor.ts` injeta automaticamente o token `Bearer` e os cabeçalhos de tenant (`X-Condominio-Id`, `X-Tenant-Id`) em todas as requisições HTTP para a API.
- **Tratamento de 401**: O `error.interceptor.ts` detecta expiração de credencial, desconecta o usuário e o encaminha para `/auth/login`.

Referências: [ADR-007: Autenticação JWT](../../decisoes/ADR-007-autenticacao-jwt-aplicacao.md) e [ADR-008: Pessoa e Usuário](../../decisoes/ADR-008-pessoa-e-usuario.md).

---

## 3. Infraestrutura PWA e Operação Offline

- **Angular Service Worker (`@angular/service-worker`)**: Configurado via `ngsw-config.json` para pre-caching de assets visuais, rotas estáticas e estratégias de cache para respostas de leitura da API.
- **Detecção de Conexão (`pwa-sync.service.ts`)**: Monitora eventos de conectividade do navegador (`online`/`offline`), exibindo alertas não-bloqueantes e gerenciando atualizações de versão em segundo plano.
- **Upload de Evidências em Campo**: O componente `upload-foto` permite a porteiros e zeladores capturarem imagens diretamente da câmera do dispositivo móvel sem exigir aplicativo nativo instalado das lojas.

---

## 4. Sistema Central de Notificações

- Suporte a notificações no padrão Web Push (PWA/Service Worker) e notificações push móveis (Firebase Cloud Messaging - FCM).
- Alertas visuais e central de notificações in-app implementada com Angular Signals no `notification.service.ts`.

---

## 5. Estrutura de Código no Projeto

Conforme [Estrutura.md](../../decisoes/Estrutura.md):

- **Backend (`backend/app/core/`)**:
  - `config.py`: Variáveis de ambiente e segredos
  - `database.py`: Conexão assíncrona SQLAlchemy (PostgreSQL / RLS)
  - `security.py`: Hashing (bcrypt) e JWT
  - `dependencies.py`: Injeção de dependências (`get_db`, `tenant`, `current_user`)
  - `exceptions.py`: Tratamento unificado de erros
- **Frontend (`frontend/src/app/core/`)**:
  - `guards/`: `auth.guard.ts`, `papel.guard.ts`, `unidade.guard.ts`
  - `interceptors/`: `token.interceptor.ts`, `error.interceptor.ts`
  - `services/`: `pwa-sync.service.ts`, `session.service.ts`, `notification.service.ts`
  - `models/`: `usuario-sessao.model.ts`, `resposta-api.model.ts`
- **Frontend Shared (`frontend/src/app/shared/`)**:
  - Componentes reutilizáveis sem regras de negócio (todos com `.component.ts`, `.component.html`, `.component.scss` separados e `ViewEncapsulation.Emulated`): `button`, `card`, `modal`, `confirm-dialog`, `data-table`, `status-badge`, `upload-foto`
  - Formatadores brasileiros: `cpf.pipe`, `placa.pipe`, `moeda.pipe`, `phone.pipe`, `data-format.pipe`
- **Arquitetura Global de Estilos (`frontend/src/styles.css` & `.postcssrc.json`)**:
  - Integração nativa **Tailwind CSS v4** (`@import "tailwindcss";`, `@theme`, `@utility`, `@layer`, sem `tailwind.config.js`) + **Angular Material 3** (`--mat-sys-*`).
  - Observância obrigatória das diretrizes `angular-developer`, `frontend-design` e `web-design-guidelines` (foco `:focus-visible`, `tabular-nums`, `text-wrap: balance`, `overscroll-behavior: contain`, `prefers-reduced-motion` e transições explícitas).

---

## 6. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-001: Governança de documentação e stack definitiva](../../decisoes/ADR-001-documentacao-e-stack-tecnologica.md)
  - [ADR-003: UI, Design System e Portabilidade Web (PWA)](../../decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md)
  - [ADR-006: Isolamento por condomínio com RLS no PostgreSQL](../../decisoes/ADR-006-isolamento-rls-postgresql.md)
  - [ADR-007: Autenticação JWT](../../decisoes/ADR-007-autenticacao-jwt-aplicacao.md)
  - [ADR-011: Planos SaaS e funcionalidades habilitáveis](../../decisoes/ADR-011-planos-e-funcionalidades.md)
- **Especificações Funcionais**:
  - [perfis-e-permissoes.md](perfis-e-permissoes.md)
  - [central-notificacoes.md](central-notificacoes.md)
  - [planos-e-entitlements.md](planos-e-entitlements.md)
- **Scripts SQL**:
  - [011-transversal-e-auditoria.sql](../../sql/011-transversal-e-auditoria.sql)
  - [012-rls.sql](../../sql/012-rls.sql)
