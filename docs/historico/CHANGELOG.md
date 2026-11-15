# Changelog do projeto

Registro **cronológico** de marcos, entregas e mudanças relevantes de plano. Formato inspirado em Keep a Changelog; foco em histórico de produto/planejamento (releases de código virão aqui também).

## [Unreleased]

### Adicionado (2026-11-04 — Isolamento Multi-Tenant Completo, RLS com Role de Aplicação e Onboarding Seguro com Magic Link)

- **Correção Crítica de Vazamento Multi-Tenant:**
  - Corrigida a falha em que pessoas e ocupações de outros condomínios ativos eram exibidas na tela de Vínculos & Ocupações (`ids_pessoas_visiveis`, `PessoaService.list_pessoas`, `OcupacaoUnidadeService.listar_ocupacoes`).
  - `ActiveCondominioDep` injetado e validado em todos os endpoints de Pessoas, Usuários e Ocupações.
- **Reforço de Row-Level Security (RLS) no PostgreSQL 16:**
  - Script [`docs/sql/015-rls-completo-e-roles.sql`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/sql/015-rls-completo-e-roles.sql) aplicado ao banco com sucesso.
  - Criação da role de aplicação `condourban_app` (`NOSUPERUSER` e `NOBYPASSRLS`), garantindo a execução irrestrita das políticas de RLS no PostgreSQL.
  - Ativado `FORCE ROW LEVEL SECURITY` em todas as tabelas operacionais e adicionadas políticas RLS para tabelas filhas e compartilhadas (`pessoa`, `documento_identificacao`, `usuario`, `evento_encomenda`, `historico_analise_cadastro`, `historico_ocorrencia`, `opcao_enquete`, `voto_enquete`, `pauta_assembleia`, `participante_assembleia`, `votacao_assembleia`, `opcao_votacao`, `voto_assembleia`).
  - Listener SQLAlchemy `@event.listens_for(Session, 'after_begin')` em `app.core.database` para re-injetar `SET LOCAL app.condominio_id` a cada nova transação (inclusive após `session.commit()`).
- **Proteção Anti-Scraping / LGPD e E-mail Preventivo com Link de Revogação de 15 Minutos:**
  - Bloqueada a raspagem de dados via consulta de CPF por síndicos: o cadastro de um CPF já existente reutiliza o cadastro civil de forma transparente, sem vazar e-mails, telefones ou contatos ao operador.
  - Emissão de e-mail preventivo de segurança com token criptográfico de revogação de 15 minutos (`/api/v1/identidade/onboarding/revogar-vinculo`), permitindo ao titular cancelar sumariamente vínculos não reconhecidos.
  - Rastreabilidade com eventos de auditoria forense (`VINCULO_PESSOA_EXISTENTE_CRIADO`, `VINCULO_REVOGADO_PELO_TITULAR`).
- **Auto-Onboarding com Magic Link Temporário (15 Minutos):**
  - Endpoints públicos: `POST /api/v1/identidade/onboarding/verificar-cpf`, `POST /api/v1/identidade/onboarding/confirmar-magic-link`, `POST /api/v1/identidade/onboarding/revogar-vinculo` e `GET /api/v1/identidade/onboarding/revogar-vinculo`.
  - Mascaramento de e-mail cadastrado (ex: `r***a@email.com`) e validação via token de 15 minutos para que o próprio titular confirme e confira seus dados.
- **Frontend Angular 22:**
  - `IdentidadeCadastroService.getPessoas(condominioId?)` passa o identificador do condomínio ativo.
  - Componentes `OcupacoesComponent`, `BlocoUnidadeListComponent` e `UsuariosComponent` atualizados para propagar o tenant ativo em todas as consultas.
- **Suíte de Testes:**
  - 100% dos testes do backend (`79 passed`) validados com sucesso via `pytest`.
  - Build de produção do Angular 22 compilado com sucesso.

### Adicionado (2026-11-03 — BC-04 Portaria: encomendas com PIN + papéis separados)

- API autenticada: `GET/POST /portaria/encomendas`, `POST /portaria/encomendas/{id}/baixa` (PIN) e `GET/POST /portaria/visitantes`.
- Papel `ENCOMENDAS` opera pacotes; `PORTARIA`/`PORTEIRO` opera visitantes; morador lista só a própria unidade.
- Seed demo: `encomendas@condourban.com` / `admin123`.
- UI de encomendas consome API real (empty/loading/error + baixa só operador).

### Alterado (2026-11-02 — Separação RBAC Portaria vs Encomendas)

- Catálogo de papéis passa a distinguir **liberação de entrada** (`PORTEIRO` / `PORTARIA`) de **correspondências** (`ENCOMENDAS`).
- Atualizados [`perfis-e-permissoes.md`](../funcionalidades/10_transversal_plataforma/perfis-e-permissoes.md), [`correspondencias-encomendas.md`](../funcionalidades/04_portaria/correspondencias-encomendas.md), [`atendimento-visitantes-prestadores.md`](../funcionalidades/04_portaria/atendimento-visitantes-prestadores.md) e o plano TLC [`.specs/features/bc-04-portaria/plan.md`](../../.specs/features/bc-04-portaria/plan.md).
- Seed/build BC-04 inclui usuário demo `encomendas@condourban.com`; `portaria@` permanece só no eixo de visitantes.

### Refatorado (2026-11-02 — Tabelas com Styled Header, Paginação Integrada, Filtros Unificados e Reuso Global de CSS)

- **Tabelas com Styled Header (`.styled-table` / `.refined-table`) e Paginação Integrada (`.table-pagination`):**
  - Centralizado em [`frontend/src/styles.css`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/styles.css) (`@layer components`) o sistema de tabelas padronizadas com cabeçalho estilizado em gradiente dark-slate (`thead tr`), linhas agrupadoras (`tbody tr.group-header-row`), suporte a `MatRipple` do Angular Material 3 e barra de paginação integrada (`.table-pagination`, `.pagination-info`, `.page-size-control`, `.pagination-controls`, `.page-btn`).
  - Atualizado o componente compartilhado [`DataTableComponent`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/shared/components/data-table/data-table.component.ts) com `.styled-table`, seletor de itens por página (`5, 10, 20, 50`) e navegação de páginas numeradas.
  - Extraídos e consolidados em `styles.css` os estilos estruturais reutilizados em toda a aplicação (`.view-layout`, `.section-hero`, `.subnav-tabs`, `.metrics-ribbon`, `.toolbar-card`, `.form-panel`, `.modal-backdrop`, `.modal-card`), reduzindo drasticamente o CSS local de cada componente.
- **Identidade e Cadastro (`identidade_cadastro`):**
  - **Usuários & Perfis ([`usuarios.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/usuarios/usuarios.component.ts)):** Implementada a barra de filtros idêntica à tela de Vínculos & Ocupações (`.toolbar-card` com busca textual + filtro encadeado de Torre/Bloco + filtro de Unidade + filtro de Perfil RBAC + filtro de Status + botão `✕ Limpar`), mantendo a visualização em tabela com `.styled-table` (Styled Header), coluna de Unidade/Vínculo e paginação integrada.
  - **Pessoas Físicas ([`pessoas.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/pessoas/pessoas.component.ts)):** Convertida para visualização em tabela no mesmo estilo da tela de Usuários & Perfis (`.styled-table` com Styled Header, células de avatar/nome, CPF, contato, LGPD, status, modal de edição e paginação integrada).
- **Condomínio (`condominio`):**
  - **Menu Principal ([`app.component.html`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/app.component.html)):** Ajustado o texto do item de menu de navegação para exibir apenas `"Condomínio"`.
  - **Blocos & Unidades ([`bloco-unidade-list.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/condominio/components/blocos-unidades/bloco-unidade-list.component.ts)):** Refatorada a listagem para o formato de tabela direta e limpa com Styled Header (`.styled-table`), barra de filtros unificada (`.toolbar-card`), **destaque cromático na coluna Bloco / Torre** (`.bloco-badge` no estilo de badge da tipologia com paleta de cores distintas por bloco/torre) e paginação integrada.
  - **Vagas de Garagem ([`vaga-list.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/condominio/components/vagas/vaga-list.component.ts)):** Padronizada com `.toolbar-card`, `.styled-table` e paginação integrada.

### Refatorado (2026-11-02 — Arquitetura de Estilos Tailwind CSS v4 + Angular Material 3 e Separação Estrita de Componentes)

- **Arquitetura Global CSS-First (`Tailwind CSS v4` + `Angular Material 3`):**
  - Configurado pipeline PostCSS nativo ([`frontend/.postcssrc.json`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/.postcssrc.json)) com `@tailwindcss/postcss` e instalado `@angular/material` v22 + `tailwindcss` v4, sem qualquer dependência de `tailwind.config.js`.
  - Criado o stylesheet global canônico [`frontend/src/styles.css`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/styles.css) estruturado em 5 camadas:
    1. **Tokens & Ponte Angular Material 3 (`:root`)**: Sincronização bidirecional entre os design tokens do CondoUrban (`--color-*`, `--radius-*`, `--shadow-*`, `--font-family-*`) e as variáveis de sistema M3 (`--mat-sys-primary`, `--mat-sys-surface`, `--mat-sys-on-surface`, `--mat-sys-outline`, `--mat-sys-error`, `--mat-sys-corner-*`).
    2. **Bloco `@theme` Nativo**: Mapeamento completo de fontes (`--font-sans`, `--font-display`, `--font-mono`), paleta semântica, tokens Material (`--color-mat-*`), raios de borda e sombras para geração automática de utilitários Tailwind v4.
    3. **Reset Saneado em `@layer base`**: Eliminação dos conflitos de especificidade com `@layer utilities` e exclusão explícita de `.mat-mdc-input-element` / `.mdc-text-field__input` via `:where(...)` para evitar bordas duplas em `<mat-form-field>`.
    4. **Harmonização MDC em `@layer components`**: Ajustes para `.mdc-notched-outline__notch`, `.mat-mdc-card`, `.mat-mdc-dialog-container`, `.mat-mdc-button` e `.mat-mdc-table`.
    5. **Diretivas `@utility` Nativas**: Criação de utilitários reutilizáveis (`tabular-nums`, `text-balance`, `surface-card`, `surface-interactive`, `focus-ring`, `container-page`, `input-control`).
- **Separação Estrita de Arquivos (`.ts`, `.html`, `.scss`) e `ViewEncapsulation.Emulated` em 100% dos Componentes:**
  - Extraídos todos os templates (`template`) e estilos (`styles`) inline dos **38 componentes Angular** (`app.component`, 7 componentes em `shared/components/` e 30 componentes de negócio em `features/`) para arquivos dedicados `.component.html` e `.component.scss`.
  - Configurado `encapsulation: ViewEncapsulation.Emulated` e seletor `:host` explícito em todos os componentes de layout, primitivos compartilhados e telas de domínio, prevenindo vazamento de estilos.
- **Conformidade com `web-design-guidelines` e `frontend-design`:**
  - Substituição de `:focus { outline: none; }` por `:focus-visible` e utilitário `focus-ring`.
  - Remoção de `transition: all` em favor de propriedades explícitas (`background-color`, `border-color`, `color`, `box-shadow`, `transform`, `opacity`) e suporte global a `@media (prefers-reduced-motion: reduce)`.
  - Aplicação de `aria-label` em botões de ícone, `aria-hidden="true"` em SVGs decorativos, `overscroll-behavior: contain` em modais/dialogs e `tabular-nums` em tabelas de dados.
- **Governança e Documentação:**
  - Atualizados [`AGENTS.md`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/AGENTS.md), [`ADR-003`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md), [`ADR-013`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-013-organizacao-diretorios.md), [`transversal.md`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/funcionalidades/10_transversal_plataforma/transversal.md) e [`MAPA.md`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/funcionalidades/MAPA.md) instituindo obrigatoriamente essas regras de arquitetura e design no frontend.

### Refatorado (2026-10-31 — Decomposição Arquitetural do Subdomínio `condominio/estrutura` em Submódulos Especializados)

- **Backend (FastAPI / SQLAlchemy 2.0 / Pydantic v2):**
  - O antigo submódulo monolítico `backend/app/modules/condominio/estrutura/` foi decomposto em 3 novos submódulos canônicos (além de `areas_comuns/`), cada um estritamente alinhado à **Regra dos 4 Arquivos ([ADR-013](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-013-organizacao-diretorios.md))**:
    - **`branding/`**: `models.py` (`Condominio`, `Inquilino`), `schemas.py` (`CondominioInfoResponse`, `CondominioInfoUpdate`, `ConfiguracaoCondominioUpdate`), `service.py` (`BrandingService`) e `router.py` (`/info`, `/configuracoes`, `/todos`, `/novo`, `/condominios/{id}`).
    - **`blocos_unidades/`**: `models.py` (`Bloco`, `Unidade`), `schemas.py` (`BlocoCreate`, `BlocoUpdate`, `BlocoResponse`, `UnidadeCreate`, `UnidadeUpdate`, `UnidadeResponse`), `service.py` (`BlocosUnidadesService`) e `router.py` (`/blocos`, `/blocos/{id}`, `/unidades`, `/unidades/{id}`, `/unidades/importar`).
    - **`vagas/`**: `models.py` (`VagaGaragem`), `schemas.py` (`VagaGaragemCreate`, `VagaGaragemUpdate`, `VagaGaragemResponse`), `service.py` (`VagasService`) e `router.py` (`/vagas`, `/vagas/{id}`).
  - `backend/app/modules/condominio/router.py` atualizado para agregar os 4 submódulos canônicos (`branding`, `blocos_unidades`, `vagas`, `areas_comuns`).
  - `backend/app/modules/condominio/estrutura/` mantido como camada de retrocompatibilidade para exportação de models, schemas e services, garantindo integridade de migrações e testes legados.
  - Testes automatizados do backend: 60/60 testes passando com 100% de sucesso.
- **Frontend (Angular 22 / Tailwind CSS / Signals):**
  - O componente monolítico `condominio-list.component.ts` (1.200+ linhas) foi decomposto em 3 visões standalone dedicadas:
    - **[`bloco-unidade-list.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/condominio/components/blocos-unidades/bloco-unidade-list.component.ts)**: Catálogo hierárquico de torres e unidades habitacionais, métricas de metragem privativa, filtros combinados, modais de edição e exclusão segura.
    - **[`vaga-list.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/condominio/components/vagas/vaga-list.component.ts)**: Gestão de vagas de garagem, métricas de vagas cobertas vs. descobertas, formulário expansível de nova vaga, edição e vinculação a unidades privativas.
    - **[`condominio-admin.component.ts`](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/frontend/src/app/features/condominio/components/branding/condominio-admin.component.ts)**: Painel multi-condomínio com alternância de condomínio ativo da sessão, cadastro de novos empreendimentos e edição cadastral/branding oficial.
  - Sub-navegação consistente e unificada entre todas as 4 telas (`Blocos & Unidades`, `Vagas de Garagem`, `Áreas Comuns`, `Condomínios (Admin)`).
  - Serviços decompostos em `branding.service.ts`, `bloco-unidade.service.ts` e `vagas.service.ts`, com `condominio.service.ts` mantido como fachada unificada para retrocompatibilidade.
  - Rotas configuradas em `condominio.routes.ts` com suporte direto a `/condominio/estrutura`, `/condominio/vagas`, `/condominio/admin` e `/condominio/areas-comuns`.
  - Build do Angular (`npm run build`) validado com zero erros.


### Adicionado (2026-10-31 — Filtros Avançados por Torre/Unidade em Ocupações e Busca por Placa/Unidade em Veículos & Pets)

- **Vínculos & Ocupação de Unidades ([`ocupacoes.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/ocupacoes/ocupacoes.component.ts)):**
  - Adicionado seletor de filtragem por Torre / Bloco com auto-filtro encadeado do select de Unidades autônomas.
  - Adicionado seletor de filtragem direta por Unidade Habitacional para localizar instantaneamente todas as pessoas (proprietários, inquilinos, dependentes e hóspedes) vinculadas a uma unidade específica.
  - Busca textual expandida para contemplar identificador da unidade, nome do bloco/torre, CPF e nome do morador.
  - Botão `✕ Limpar` para resetar rapidamente todos os filtros combinados.
- **Veículos & Pets ([`veiculos-pets.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/veiculos-pets/veiculos-pets.component.ts)):**
  - Adicionada barra de busca integrada e filtros seletores por Torre/Bloco e por Unidade Habitacional.
  - Busca inteligente por placa (com ou sem formatação/hífen), modelo, fabricante/marca, cor, nome do pet, espécie, raça ou unidade.
  - Exibição destacada da Unidade e Torre em badges (`🏠 Unidade X (Torre Y)`) em cada card de veículo e card de pet.
  - Contadores dinâmicos nos cabeçalhos de seção refletindo o total de itens filtrados em tempo real.

### Adicionado (2026-10-31 — Suporte a Acesso por Outros Dispositivos na Rede Local / LAN)

- **Backend FastAPI / Uvicorn:**
  - Configurado Uvicorn para escutar em `0.0.0.0:8000` (`--host 0.0.0.0`), permitindo requisições originadas de outros computadores, tablets e smartphones conectados na rede local.
  - Habilitado `allow_origin_regex=r"^https?://.*"` no `CORSMiddleware` em [`app/main.py`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/backend/app/main.py), aceitando cabeçalhos de origem vindos de qualquer IP local com suporte a credenciais.
- **Frontend Angular Dev Server & Proxy:**
  - Configurado `npm start` e `angular.json` com `--host 0.0.0.0 --allowed-hosts`, permitindo resolução de requisições por IP ou nomes de máquina na rede.
  - Ajustados [`environment.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/environments/environment.ts) e [`environment.development.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/environments/environment.development.ts) com caminhos de API relativos (`/api/v1`) e WebSockets dinâmicos via `window.location`. Dessa forma, qualquer celular ou notebook na rede consome a API através do proxy do dev server sem tentar acessar indevidamente o localhost do próprio dispositivo cliente.

### Adicionado / Corrigido (2026-10-31 — Exclusão Segura com Integridade Referencial, Gestão Multi-Condomínio e Massa de Teste Rica)

- **Exclusão Segura de Entidades com Proteção de Integridade Referencial (BC-01 & BC-02):**
  - **Blocos Estruturais:**
    - Rotas `DELETE /api/v1/condominio/blocos/{id}` e `/blocks/{id}` no backend rejeitando a remoção com HTTP 400 (`BLOCO_POSSUI_UNIDADES`) caso existam unidades vinculadas.
    - No frontend, adicionado botão `🗑 Excluir` em cada card de bloco em [`condominio-list.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/condominio-list.component.ts) com confirmação e alerta preventivo se houver unidades.
  - **Unidades Habitacionais Autônomas:**
    - Rotas `DELETE /api/v1/condominio/unidades/{id}` e `/units/{id}` rejeitando a exclusão com HTTP 400 (`UNIDADE_POSSUI_OCUPACOES`) caso haja pessoas, moradores, veículos ou pets vinculados. Vagas associadas são automaticamente desvinculadas.
    - No frontend, botão `🗑 Excluir` no rodapé de cada unidade com confirmação e tratamento de bloqueio amigável.
  - **Pessoas Físicas (Registro Civil LGPD):**
    - Rota `DELETE /api/v1/identidade/pessoas/{id}` rejeitando com HTTP 400 caso a pessoa possua conta de usuário (`PESSOA_POSSUI_CONTA`), ocupações ativas (`PESSOA_POSSUI_OCUPACOES`), veículos ou pets tutelados. Remove ocupações históricas inativas e desvincula registros órfãos.
    - No frontend ([`pessoas.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/pessoas/pessoas.component.ts)), botão `🗑 Excluir` em cada card civil com painel inline de confirmação de exclusão.
  - **Vagas de Garagem, Veículos e Pets:**
    - Exclusão de vagas (`DELETE /condominio/vagas/{id}`), veículos (`DELETE /identidade/veiculos-pets/veiculos/{id}`) e pets (`DELETE /identidade/veiculos-pets/pets/{id}`) com confirmação e atualização reativa dos signals no frontend.
  - **Áreas Comuns:**
    - `DELETE /condominio/areas-comuns/{id}` verificando se há reservas pendentes ou confirmadas ativas antes de excluir.
- **Gestão Central Multi-Condomínio para Administradores:**
  - **Backend API:** Adicionadas rotas `GET /api/v1/condominio/todos` (lista todos os condomínios da base), `POST /api/v1/condominio/novo` (cadastra novo condomínio com endereço e CNPJ) e `DELETE /api/v1/condominio/condominios/{id}` (exclui condomínio vazio).
  - **Frontend UI & Session:**
    - Nova aba `[Condomínios (Admin)]` em [`condominio-list.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/condominio-list.component.ts) com formulário inline para cadastrar novos condomínios e listagem em cards informativos.
    - Suporte a alternância de condomínio ativo no sistema via [`SessionService.setCondominioId()`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/core/services/session.service.ts), atualizando dinamicamente os cabeçalhos `X-Condominio-Id` e `X-Tenant-Id` via `tokenInterceptor` e recarregando blocos, unidades e vagas.
- **Massa de Teste Rica & Usuário Administrador (`seed.py`):**
  - Gerados 3 condomínios completos no banco `backend/dev.db`:
    1. *Condomínio Residencial Jardins* (São Paulo/SP)
    2. *Residencial Solar das Acácias* (Brasília/DF)
    3. *Edifício Metropolitan Tower* (Rio de Janeiro/RJ)
  - Dezenas de blocos (Torre Girassol, Orquídea, Tulipa, Torre Norte, Torre Sul), unidades residenciais e duplex, vagas demarcadas e 5 áreas comuns completas (Salão de Festas, Churrasqueira Gourmet, Piscina, Academia, Quadra).
  - Pessoas físicas com CPFs formatados, hash criptográfico, ocupações ativas com dependentes em cascata, veículos com placa Mercosul e pets cadastrados.
  - Criado usuário Superadministrador: `admin@condourban.com` / `admin123` (papel `SUPERADMIN`).
- **Validação de Qualidade e Conformidade:**
  - Build de produção do frontend (`npm run build`) concluído com **0 erros**.
  - Suíte completa de testes no backend (`poetry run pytest`) com **60/60 testes passando (100% de sucesso)**.

### Adicionado / Corrigido (2026-10-31 — Conclusão Integral dos Contratos Frontend-Backend para BC-01 e BC-02)

- **Correções de Falhas Críticas no Frontend e Autenticação:**
  - **Segurança de Menus & RBAC:** A barra global de navegação (`nav.nav-bar`) em [`app.component.html`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/app.component.html) foi encapsulada em `@if (authService.isAuthenticated())`, ocultando abas na tela de login. Implementado controle refinado de visibilidade com `podeAcessar(modulo)` conforme os papéis (`SINDICO`, `PORTARIA`, `MORADOR`).
  - **Logout Confiável com Redirecionamento:** Atualizado [`auth.service.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/auth/services/auth.service.ts) para injetar `Router`, limpar credenciais locais e redirecionar imediatamente para `/auth/login`, impedindo que o usuário deslogado continue operando em telas restritas.
- **Edição Completa de Entidades (BC-01 e BC-02):**
  - **Pessoas Físicas (Registro Civil):**
    - Adicionados endpoints `GET /pessoas/{id}`, `PATCH /pessoas/{id}` e `PUT /pessoas/{id}` no backend com schema [`PessoaUpdate`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/backend/app/modules/identidade_cadastro/pessoas/schemas.py).
    - Adicionado botão `✎ Editar` em cada card de [`pessoas.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/pessoas/pessoas.component.ts) com formulário inline reativo para atualizar nome, e-mail, celular e CPF via `IdentidadeCadastroService.updatePessoa`.
  - **Blocos e Unidades Habitacionais:**
    - Criados schemas `BlocoUpdate` e `UnidadeUpdate` no backend e rotas `PATCH` e `PUT` em `/condominio/blocos/{id}` e `/condominio/unidades/{id}` (com suporte a aliases `/blocks` e `/units`).
    - Adicionados botões e painéis de edição inline em [`condominio-list.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/condominio-list.component.ts) para alterar nomes, descrições, andares, identificações e status.
- **Gestão de Vagas de Garagem (BC-02):**
  - Adicionado suporte a vagas no frontend com aba dedicada `[Vagas de Garagem]` em [`condominio-list.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/condominio-list.component.ts), permitindo cadastrar novas vagas (com tipo de veículo, cobertura e vinculação opcional à unidade autônoma) e visualizá-las em cards com tags visuais.
  - No backend, `create_vaga` agora resolve e valida o `condominio_id` automaticamente a partir da unidade informada.
- **Resolução de Erro ao Salvar Veículos e Animais (BC-01):**
  - Schema `VeiculoCreate` e `PetCreate` tornados flexíveis com `condominio_id: Optional[UUID] = None`. O backend infere o condomínio diretamente da unidade habitacional vinculada, eliminando o erro HTTP 422 Unprocessable Entity ao salvar veículos ou pets no frontend.
- **Vínculos Habitacionais & Posse Direta (`OcupacoesComponent` - BC-01):**
  - Criado o componente [`OcupacoesComponent`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/ocupacoes/ocupacoes.component.ts) e rota associada `/identidade-cadastro/ocupacoes`.
  - Formulário completo para vincular qualquer pessoa física cadastrada a uma unidade habitacional, com seleção de papel (`PROPRIETARIO`, `INQUILINO`, `DEPENDENTE`, `TEMPORARIO`, `HOSPEDE`), indicador de posse direta ("Mora no local"), vigência contratual e vínculo hierárquico com o morador responsável.
  - Ação de inativação de vínculo com confirmação e opção de desocupação em cascata de dependentes.
  - Botão de execução da rotina diária de expiração de ocupações temporárias e estadias com feedback visual em tempo real.
  - Sub-navegação atualizada em todas as 5 visões do módulo de Identidade e Cadastro.
- **Garantia de Qualidade e Compilação:**
  - Build Angular (`ng build`) concluído com **0 erros e 0 alertas**.
  - Suíte completa de testes unitários e de integração no backend (`poetry run pytest`) executada com **60/60 testes passando (100% de sucesso)**.

### Adicionado / Refatorado (2026-10-30 — Refatoração de Frontend Design para BC-01 e BC-02)

- **Design System & Fundações Visuais (`frontend-design`):**
  - **Identidade Arquitetônica & Paleta Coesa:** Atualizado [`tokens.scss`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/shared/ui/tokens.scss) e [`styles.scss`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/styles.scss) com tipografia modular (`Plus Jakarta Sans` para display, `Inter` para leitura, `JetBrains Mono` para identificadores/placas), sombras difusas em múltiplas camadas e sistema de neutrals com tingimento slate/ink, eliminando templates genéricos e drop-shadows artificiais.
  - **Primitivas UI Elevadas:** Refatorados [`ButtonComponent`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/shared/components/button.component.ts), [`CardComponent`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/shared/components/card.component.ts) e [`StatusBadgeComponent`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/shared/components/status-badge/status-badge.component.ts) com suporte a micro-indicadores e feedback tátil (`active:scale-[0.98]`).
  - **Header & Navegação Global:** Reestruturado o shell da aplicação em [`app.component.html`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/app.component.html) com glifo vetorial arquitetônico para a marca **CondoUrban**, badge de condomínio ativo e perfil de usuário com avatar e papel RBAC.
- **Refatoração Completa do BC-02 (Condomínio & Estrutura Física):**
  - **Visão Geral e Mapeamento Dimensional:** Refatorado [`condominio-list.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/condominio-list.component.ts) com faixa de resumo estrutural (blocos, unidades, andares), barra de busca inteligente reativa com Signals, filtros pill por torre e layout em grid de cartões de unidades autônomas.
  - **Formulários Estruturais de Precisão:** Refatorados [`block-form.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/block-form.component.ts) e [`unit-form.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/estrutura/unit-form.component.ts) com breadcrumbs, ícones vetoriais de cabeçalho, micro-labels e feedback de erro descritivo.
  - **Catálogo de Espaços de Convivência:** Refatorado [`areas-comuns.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/condominio/components/areas-comuns/areas-comuns.component.ts) com cards de áreas de lazer, indicadores de capacidade/horários, taxa de uso e botão de alternância imediata de interdição preventiva para manutenção.
- **Refatoração Completa do BC-01 (Identidade & Cadastro):**
  - **Sub-navegação Integrada:** Adicionada barra de abas unificada entre `Pessoas Físicas`, `Usuários & RBAC`, `Onboarding & Convites` e `Veículos & Pets`.
  - **Pessoas Físicas (Base Civil LGPD):** Refatorado [`pessoas.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/pessoas/pessoas.component.ts) com busca instantânea por nome/CPF/e-mail, avatares em monograma, selo de conformidade legal e formulário estruturado.
  - **Usuários & Perfis RBAC:** Refatorado [`usuarios.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/usuarios/usuarios.component.ts) com tabela refinada, badges de perfil de acesso (`SÍNDICO`, `PORTARIA`, `MORADOR`) e histórico de último login.
  - **Fila de Auto-Onboarding & Convites:** Refatorado [`onboarding.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/onboarding/onboarding.component.ts) com gerador de convites com tokens seguros válidos por 7 dias e fila de análise documental com ações de aprovação e rejeição com motivo.
  - **Veículos e Pets:** Refatorado [`veiculos-pets.component.ts`](file:///c:/Users/frede/Projetos pessoais/gestao_condominios/frontend/src/app/features/identidade_cadastro/components/veiculos-pets/veiculos-pets.component.ts) com estilização autêntica de placas padrão Mercosul com tarja azul e tipografia monospace, vínculo de vagas de garagem e controle sanitário/vacinal de pets.
- **Validação de Build e Testes:** Build Angular (`ng build`) concluído com **0 erros e 0 alertas** de orçamento; suíte backend de contratos mantida com **100% de aprovação**.


### Adicionado / Concluído (2026-10-30 — Integração E2E Frontend-Backend e Validação dos Módulos BC-01 e BC-02)

- **Integração Ponta a Ponta Frontend-Backend e Dev Environment:**
  - **Proxy Dev Server e Portas:** Configurado `frontend/proxy.conf.json` e integrado ao `frontend/angular.json` para direcionar requisições `/api` e `/ws` da porta 4200 para a porta 8000 da API FastAPI.
  - **Fluxo de Autenticação Real:** Ajustado `frontend/src/app/features/auth/services/auth.service.ts` para chamar `/api/v1/auth/login`, mapeando credenciais, decodificando claims JWT e sincronizando com `SessionService`. Adicionado fallback de compatibilidade no backend para `/identidade/users/login` e `/api/v1/identidade/usuarios/login`.
  - **Banco de Dados Local e Seed:** Corrigido `backend/scripts/seed.py` e gerado `backend/dev.db` populado com 3 usuários padrão (`sindico@condourban.com`, `portaria@condourban.com`, `morador@condourban.com` / `admin123`) e condomínio de demonstração.
- **Implementação e Conexão de Telas no Frontend (Angular 22+):**
  - **BC-02 (Condomínio):**
    - Criado `BlockFormComponent` (`/condominio/novo-bloco`) com validação reativa e vínculo ao condomínio ativo.
    - Atualizado `CondominioListComponent` com botão `+ Novo Bloco` e listagem de blocos com suas unidades.
    - Atualizado `UnitFormComponent` com dropdown de blocos carregados dinamicamente e tratamento de erro `UNIDADE_DUPLICADA`.
    - Conectado `AreasComunsComponent` à API para listagem, cadastro e interdição/liberação operacional de espaços.
    - Adicionado suporte a endpoints `/units` e `/blocks` como alias para `/unidades` e `/blocos` no backend.
  - **BC-01 (Identidade e Cadastro):**
    - Atualizado `IdentidadeCadastroService` com métodos completos para Pessoas, Usuários, Convites, Aprovações/Rejeições de Onboarding, Veículos e Pets.
    - Conectado `PessoasComponent` para listar e cadastrar pessoas físicas com validação de CPF e tipo de vínculo.
    - Conectado `UsuariosComponent` com visualização de usuários e perfis RBAC do condomínio.
    - Conectado `OnboardingComponent` com geração de convites com token, aprovação de solicitações e rejeição com motivo obrigatório.
    - Conectado `VeiculosPetsComponent` com formulários inline e listagem dinâmica de veículos e pets.
- **Auditoria de Conformidade TLC-Spec-Lean:**
  - Execução estrita do validador determinístico `python .specs/scripts/validate_verification.py` com **0 erros e 0 avisos** para `bc-01-identidade-cadastro` e `bc-02-condominio`.
  - Auditoria independente pelo agente Verifier confirmando conformidade de arquitetura, isolamento multi-tenant (ADR-006), separação civil vs conta (ADR-008) e padronização pt-BR (ADR-010). Suíte backend com 60 testes passando (100% de sucesso).


### Adicionado / Concluído (2026-10-18 — Conclusão Unificada do BC-02 Condomínio e Estrutura Física sob TLC-Spec-Lean)

- **Conclusão Integral do Bounded Context `02_condominio` (Segundo Pilar Essencial de Dados):**
  - **Estrutura Física (Blocos e Unidades):** Submódulo `estrutura` enriquecido com cadastro e listagem de blocos e unidades, validação de unicidade de unidade por bloco (`UNIDADE_DUPLICADA` com HTTP 400) e importação em lote CSV (`POST /unidades/importar`).
  - **Vagas de Garagem e Estacionamento:** Cadastro, listagem e atualização de vínculos de vagas (`POST`, `GET`, `PATCH /vagas`) com validação de unicidade de identificação por condomínio (`VAGA_DUPLICADA` com HTTP 400).
  - **Áreas Comuns e Espaços de Convivência:** Submódulo `areas_comuns` complementado com consulta detalhada por ID (`GET /areas-comuns/{id}`) e alteração de status/interdição operacional para manutenção (`PATCH /areas-comuns/{id}`).
  - **Perfil Cadastral e Configurações Globais:** Endpoints para dados cadastrais e endereço (`GET`, `PUT /info`) e gestão de branding institucional (logos, cores primárias) e regras de convivência em formato JSON (`GET`, `PATCH /configuracoes`).
  - **Artefatos TLC-Spec-Lean:** Criados `.specs/features/bc-02-condominio/plan.md`, `checks.md` (18 checks observáveis C1–C18) e `verification.md` (veredicto PASS).
  - **Validação Automatizada:** Gates `validate_plan.py`, `validate_checks.py` e `validate_verification.py` executados com **0 erros e 0 avisos**.
  - **Suíte de Testes Monorepo:** 60 testes automatizados passando com 100% de sucesso em `pytest` (12 testes específicos para o BC-02).
  - **Liberação das Trilhas Paralelas:** Com BC-01 e BC-02 concluídos, os pilares mestres de dados estão finalizados, permitindo a paralelização das Trilhas A (Hardware/Portaria), B (Social/Reservas) e C (Governança/Finanças/PMO).

### Adicionado / Concluído (2026-10-18 — Conclusão Unificada do BC-01 Identidade e Cadastro sob TLC-Spec-Lean)

- **Reestruturação Integral do Roadmap (`docs/plano/03-roadmap-e-entregas.md` e `04-status-e-proximos-passos.md`):**
  - Consolidação da infraestrutura transversal e fundação sob a denominação canônica **Marco 0: Fundação Transversal & Core Base** (`BC-00`).
  - Estabelecimento de **BC-01 (Identidade e Cadastro)** e **BC-02 (Condomínio)** como os **Pilares Essenciais de Dados (Cadastros Mestres)** que fundamentam todas as operações da plataforma.
  - Definição do Grafo Topológico de Dependências e mapeamento de **3 Trilhas Paralelas Independentes** (Hardware/Portaria, Social/Reservas e Governança/Finanças/PMO).
- **Conclusão Integral do Bounded Context `01_identidade_cadastro` (Primeiro Pilar de Dados):**
  - **Auto-onboarding e Fila de Validação Documental:** Implementação dos endpoints `/api/v1/identidade/onboarding/solicitar`, `/solicitacoes`, `/aprovar` e `/rejeitar` com criação automática de ocupação de unidade e membro de condomínio.
  - **Veículos e Vagas de Garagem:** Submódulo `veiculos_pets` completo (`router.py`, `service.py`, `models.py`, `schemas.py`) com normalização de placas em maiúsculas, validação de formato e bloqueio estrito de placas duplicadas no mesmo condomínio.
  - **Animais Domésticos (Pets):** Cadastro de animais domésticos para controle comunitário, porte e situação vacinal.
  - **Artefatos TLC-Spec-Lean:** Criados `.specs/features/bc-01-identidade-cadastro/plan.md`, `checks.md` (22 checks observáveis C1–C22) e `verification.md` (veredicto PASS).
  - **Validação Automatizada:** Gates `validate_plan.py`, `validate_checks.py` e `validate_verification.py` executados com **0 erros e 0 avisos**.
  - **Suíte de Testes:** Suíte completa com 55 testes automatizados passando (100% de sucesso).

### Adicionado (2026-10-18 — Implementação das 5 Regras de Ocupação da Unidade)

- **Regras Invariantes de Ocupação (`identidade_cadastro`):**
  - **Conflito de Posse Direta:** Regra impedindo proprietário de ter `mora_no_local = TRUE` se houver inquilino ativo; desativação automática de moradia do proprietário ao ativar inquilino com evento de auditoria.
  - **Datas Obrigatórias para Curtos Prazos:** Vínculos `TEMPORARIO` e `HOSPEDE` exigem `data_inicio` e `data_fim` obrigatórias (validação Pydantic v2 + `CHECK` constraint ANSI SQL).
  - **Validação de Retroatividade:** Validação estrita de que `fim_em > inicio_em`.
  - **Bloqueio Automático e Rotina Diária:** Implementação do script CLI `backend/scripts/rotina_expiracao_ocupacoes.py`, endpoint `POST /api/v1/identidade/ocupacoes/rotina-expiracao` e função PL/pgSQL `fn_expirar_ocupacoes_vencidas` para expiração automática de vínculos vencidos.
  - **Dependentes Exigem Responsável:** Vínculos `DEPENDENTE` vinculados a `responsavel_ocupacao_id` e condicionados a responsável residente ativo na unidade, com inativação em cascata (`cascade_dependentes`).
- **Endpoints de Ocupação:** Criado `ocupacoes_router` com endpoints para listagem, criação, atualização, inativação e disparo de rotina de expiração em `/api/v1/identidade/ocupacoes`.

### Adicionado (2026-10-17 — Criação do AGENTS.md Canônico)

- **Guia para Agentes de IA:** Criado [`AGENTS.md`](../../AGENTS.md) na raiz do projeto contendo a síntese canônica da stack (FastAPI + Angular PWA), mapa dos 9 Bounded Contexts com correspondência estrita backend/frontend, regras invariantes inegociáveis (RLS, pt-BR, pessoa vs usuário, entitlements, observância obrigatória das skills `angular-developer` e `fastapi`) e comandos essenciais de dev/testes.

### Adicionado / Alterado (2026-10-17 — Consolidação dos Documentos de Domínio em docs/funcionalidades/)

- **Colocação dos Documentos de Domínio:** Os 10 documentos de arquitetura de domínio (`identidade-cadastro.md`, `condominio.md`, `controle-acesso.md`, `portaria.md`, `reservas.md`, `comunicacao.md`, `governanca.md`, `financeiro.md`, `manutencao.md` e `transversal.md`) foram copiados para seus respectivos Bounded Contexts em `docs/funcionalidades/01_identidade_cadastro/` até `10_transversal_plataforma/`.
- **Saneamento e Resolução de Links Relativos:** Todos os links relativos nos documentos movidos foram calibrados para a nova profundidade de diretório (`../../decisoes/`, `./spec-local.md`, `../outro_contexto/spec.md`, `../../sql/`).
- **Hub Canônico e Matriz de Rastreabilidade:** Criado [`docs/funcionalidades/MAPA.md`](../funcionalidades/MAPA.md) e enriquecido [`docs/funcionalidades/README.md`](../funcionalidades/README.md) com links diretos para cada documento de domínio e para o MAPA.
- **Atualização Global de Referências:** Atualizados `docs/README.md`, `docs/dominios/README.md`, `docs/dominios/MAPA.md`, `docs/decisoes/` e `docs/plano/` para manter 100% de integridade referencial.

### Alterado (2026-10-17 — Revisão e Reorganização dos Planos por Bounded Contexts)

- **Alinhamento dos Planos aos 9 Bounded Contexts:** Todos os documentos de planejamento em `docs/plano/` (20 arquivos) foram revisados e alinhados aos 9 Bounded Contexts em pt-BR formalizados no [ADR-013](decisoes/ADR-013-organizacao-diretorios.md).
- **Catálogo de Módulos (06):** Reestruturado com os 9 Bounded Contexts como eixo primário (`identidade_cadastro`, `condominio`, `controle_acesso`, `portaria`, `reservas`, `comunicacao`, `governanca`, `financeiro`, `manutencao` + `transversal`), mantendo matriz de correlação com os 5 Pilares de negócio e links atualizados para todas as 26 especificações em `docs/funcionalidades/`.
- **Roadmap Tagueado (03):** Todas as entregas das Fases 1 a 9 e GTM/M5 foram explicitamente tagueadas com seus Bounded Contexts correspondentes (`[identidade_cadastro]`, `[controle_acesso]`, etc.).
- **Arquitetura Técnica (02) e Rotas de API (16):** Removidas indefinições legadas (FastAPI + SQLAlchemy 2.0 async + Angular 22+ consolidados); endpoints de `/api/v1` mapeados por Bounded Context.
- **Modelo de Dados (15):** Tabelas em pt-BR organizadas diretamente sob os 9 Bounded Contexts.
- **Saneamento Global de Links:** Eliminados 100% dos links legados para a raiz de `docs/funcionalidades/`, garantindo rastreabilidade pericial com `docs/dominios/MAPA.md`.

### Adicionado / Alterado (2026-10-17 — Reorganização e Detalhamento de docs/funcionalidades)

- **Reorganização em 9 Bounded Contexts:** Todas as especificações funcionais foram migradas da raiz para subpastas temáticas numeradas (`01_identidade_cadastro` até `10_transversal_plataforma`), espelhando a arquitetura backend/frontend e o [ADR-013](decisoes/ADR-013-organizacao-diretorios.md).
- **Detalhamento das Especificações:** Cada uma das 26 especificações foi detalhada com 9 seções padronizadas (objetivos, metadados com tabelas em pt-BR, matriz RBAC, máquinas de estados, fluxos passo a passo, regras de negócio numeradas, endpoints FastAPI, componentes Angular PWA e conformidade LGPD).
- **Novas Especificações Criadas:**
  - `02_condominio/estrutura-fisica.md`: Modelagem de blocos, unidades, garagens e catálogo de áreas comuns.
  - `08_financeiro/prestacao-contas-e-despesas.md`: Balancetes digitais, notas fiscais e parecer do conselho fiscal.
  - `08_financeiro/acordos-e-inadimplencia.md`: Simulação e termos de confissão/parcelamento de dívidas.
- **Rastreabilidade e Limpeza:** Atualizado `docs/funcionalidades/README.md` como Guia Mestre e removidos arquivos legados na raiz. Mapeamento sincronizado em `docs/dominios/MAPA.md` e em todos os 9 arquivos de Bounded Context.

### Alterado (2026-10-17 — Consolidação das ADRs e Estrutura)

- **ADR-001 unificado:** Fusão de ADR-001 e ADR-002 em [ADR-001: Governança de documentação e stack tecnológica definitiva](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md). Alternativas provisórias e hipóteses descartadas (Next.js/Nest e Django) foram removidas, fixando a stack oficial canônica: Python 3.11+ (FastAPI + SQLAlchemy 2.0 assíncrono + Alembic) + TypeScript (Angular 19+ SPA/PWA com Angular Material e Tailwind) + PostgreSQL com RLS / SQLite dev + Celery/Redis + S3.
- **Simplificação das ADRs:**
  - `ADR-002` marcado como *Fundido no ADR-001*.
  - `ADR-003` simplificado para foco direto no Design System (Angular Material + Tailwind CSS) e portabilidade PWA sem redundância.
  - `ADR-005` simplificado com ORM explicitamente definido para SQLAlchemy 2.0 assíncrono e Alembic.
  - `ADR-012` marcado como *Consolidado no ADR-001*.
  - `ADR-013` formalizado: **Organização de Diretórios por Bounded Contexts e Consolidação de Subdomínios**, estruturando os 9 Bounded Contexts em pt-BR e consolidando subdomínios (2 a 4 por módulo).
  - `README.md` das decisões atualizado com escopos e links limpos.

### Adicionado (2026-10-01 — fundação código Fase 1)

- Monorepo: `services/api` (**FastAPI** + SQLAlchemy 2 + SQLite), `apps/web-app` (Angular 19 + Material), `packages/ui-brand`, `docker-compose.yml`.
- Domínios: identity/tenancy (JWT), communication, documents, tickets, audit_usage, content_public.
- Seed demo + [ADR-012](decisoes/ADR-012-backend-fastapi.md) (T1 FastAPI; T8 Material).

### Alterado (2026-10-01 — nome do produto)

- **Nome oficial do produto: CondoUrban** (`condourban`) — substitui o placeholder Habitar (T4 / decisão 1.1).
- Hub, landings, wordmarks e políticas atualizados.
- **Logo oficial** em [`design/sugestoes/logos/oficial/condourban-logo.png`](design/sugestoes/logos/oficial/condourban-logo.png) — aplicada no hub e landings (decisão 1.2 parcial; faltam favicon/app icon).

### Adicionado (2026-10-01 — Angular AI / Cursor)

- Regra Cursor [`.cursor/rules/angular-ai-best-practices.mdc`](../../.cursor/rules/angular-ai-best-practices.mdc) com o prompt oficial de [angular.dev/ai/develop-with-ai](https://angular.dev/ai/develop-with-ai).
- Seção em [01-boas-praticas](plano/01-boas-praticas-e-funcionalidades.md#geração-de-código-angular-com-ia) + ponteiro no [ADR-002](decisoes/ADR-002-stack-python-angular.md).

### Alterado (2026-09-30 — revisão e alinhamento docs/funcionalidades ↔ docs/dominios)

- **Harmonização de Bounded Contexts:** códigos canônicos alinhados em todas as specs funcionais (`identity_tenancy`, `tickets`, `_transversal`, `saas`).
- **Correção de domínios em specs:** `achados-e-perdidos` e `mudanca` corrigidos para domínio `tickets` (com papéis operacionais da portaria); `notificacoes` vinculado a `_transversal`.
- **Metadados e referências:** metadados de domínio inseridos em `00-perfis-e-permissoes` (e ajuste de `condominium_id` → `condominio_id`); esclarecida referência à pergunta F3 em `reservas`.
- **Integridade de links:** resolvido link quebrado para FAQ de conta em `identity-tenancy.md`; 100% dos links validados sem quebra.

### Adicionado (2026-09-30 — apps dos concorrentes)

- Screenshots de app (Google Play / login web) em cada pasta de [`referencia/concorrentes/`](referencia/concorrentes/README.md) (`02-app-*` + `02-app-meta.json`); README atualizado com links Play.

### Adicionado (2026-09-30 — documentação por bounded context)

- Pasta [`docs/dominios/`](dominios/README.md): um hub por domínio (`identity_tenancy`, `access`, `amenities`, …) + [`_transversal`](dominios/_transversal.md) + [`MAPA.md`](dominios/MAPA.md) de rastreabilidade.
- Planos, specs, SQL e ADRs **permanecem**; os hubs só agregam links e inventário para navegar por BC.

### Adicionado (2026-09-30 — decisões a tomar)

- [18-decisoes-a-tomar.md](plano/18-decisoes-a-tomar.md): checklist (nome, logo, hospedagem, **modelo de negócios**, marca, infra, Intelbras…).
- Pergunta **B1** em [05](plano/05-perguntas-abertas.md); vínculo no [17](plano/17-modelos-de-negocio-e-precificacao.md) §6.

### Adicionado (2026-09-30 — planos/funcionalidades + higiene)

- **P8 / ADR-011:** planos SaaS com funcionalidades habilitáveis por plano e override por condomínio (só docs + DDL de referência; sem implementação de produto).
- Spec [planos-e-funcionalidades](funcionalidades/planos-e-funcionalidades.md); SQL [008](sql/008-saas-planos-e-funcionalidades.sql) / [009](sql/009-seed-planos-e-funcionalidades.sql); FAQ [planos-saas](conteudo/faq/planos-saas.md).
- Roadmap **4.2a** + personalização alinhada (flags fora do JSONB puro).
- **Higiene contínua R1–R8** (refactoring, código obsoleto/repetido, docs/DDL fantasma) em [03](plano/03-roadmap-e-entregas.md) e [01](plano/01-boas-praticas-e-funcionalidades.md).

### Adicionado (2026-09-29 — landing HTML)

- Pasta [`landing/`](../landing/README.md): preview da home de marketing (CondoUrban); link no hub [`index.html`](../index.html).

### Adicionado (2026-09-29 — landing × concorrentes)

- [07-landing-page…](plano/07-landing-page-marketing-e-conteudo-comum.md): seção **Ideias a partir dos concorrentes** (padrões, o que pegar/evitar, estrutura Home M0–M1, CTAs).
- Prints landings em [`referencia/concorrentes/`](referencia/concorrentes/README.md) (15 players).

### Alterado (2026-09-29 — consolidação da documentação)

- Fonte única: tudo canônico sob `docs/`; pacote paralelo movido para [`historico/arquivo/gestao-condominio-documentacao`](historico/arquivo/gestao-condominio-documentacao/).
- Folhas de nomes `v1_folha30` / `v2_folha20` / `v3_folha12` → [`design/sugestoes/nomes-marca/`](design/sugestoes/nomes-marca/README.md).
- Índice dos planos agrupado por área (entrada, produto, técnico, GTM).
- Preview local: `scripts/start-local.bat` (links de logos/start.bat quebrados corrigidos).
- Removidos arquivos de teste `_write_test.txt`; `tunnel` no `.gitignore`.

### Adicionado (2026-09-29 — modelos de negócio)

- [17-modelos-de-negocio-e-precificacao.md](plano/17-modelos-de-negocio-e-precificacao.md): como o mercado cobra, tabela de concorrentes, catálogo de modelos (SaaS, B2B, transacional, hardware, marketplace) e híbrido sugerido para o produto.

### Adicionado (2026-09-29 — personalização por condomínio)

- **P5 resolvida:** personalização parcial por condomínio (logo, cores, regras/horários, feature flags); sem white-label total.
- Roadmap Fase 4: itens **4.3–4.3d** + checklist ([03](plano/03-roadmap-e-entregas.md)).
- Spec [personalizacao-por-condominio](funcionalidades/personalizacao-por-condominio.md); catálogo/revisão/inventário alinhados.

### Adicionado (2026-09-29 — varredura mercado → roadmap)

- Pesquisa em sites (Winker, Superlógica, TownSq, uCondo, Condomob, wCond, MyCond, Seu Condomínio, Wecondo).
- Roadmap: itens **2.12–2.18**, **3.6–3.10**, **4.7–4.9**, **5.6**, **9.5–9.6** + tabela fora de escopo ([03](plano/03-roadmap-e-entregas.md)).
- Lacunas §7 e perguntas **F13–F16**, **N2** ([11](plano/11-lacunas-e-complementos.md), [05](plano/05-perguntas-abertas.md)).
- Catálogo [06](plano/06-produto-completo-modulos.md) e inventário [09](plano/09-inventario-referencia-e-versoes.md) §7 atualizados.

### Alterado (2026-09-29 — auth Google/Gmail)

- [ADR-007](decisoes/ADR-007-autenticacao-jwt-aplicacao.md): e-mail/senha **e** Entrar com Google; sem Keycloak.
- DDL `usuario`: `senha_hash` opcional, `google_sub`, `email_verificado`.

### Alterado (2026-09-29 — sem Keycloak)

- [ADR-007](decisoes/ADR-007-autenticacao-jwt-aplicacao.md): autenticação **JWT na aplicação**; Keycloak descartado.
- DDL `usuario`: `email` + `senha_hash` (sem `chave_usuario_keycloak`).

### Adicionado (2026-09-29 — consolidação gestao-condominio-documentacao)

- [`docs/sql/`](sql/README.md): DDL PostgreSQL 001–007 + RLS.
- Planos [15](plano/15-modelo-dados-postgresql.md) e [16](plano/16-api-v1-referencia.md).
- ADRs [006](decisoes/ADR-006-isolamento-rls-postgresql.md)–[010](decisoes/ADR-010-nomenclatura-pt-br.md).
- Spec [cadastro-morador-solicitacao](funcionalidades/cadastro-morador-solicitacao.md).

### Alterado (2026-09-29 — pilares de produto)

- Mapa de **5 pilares** no catálogo [06](plano/06-produto-completo-modulos.md): Cadastro e identidade · Controle de acesso ⭐ · Condomínio · Experiência do morador · Administração.
- Agrupamentos em [14](plano/14-revisao-plano-consolidada.md) §4; coluna Pilar na tabela de domínios em [02](plano/02-arquitetura-tecnica.md).
- Índice por pilar em [funcionalidades/README](funcionalidades/README.md).

### Adicionado (2026-09-29 — logos)

- Pasta [`docs/design/sugestoes/logos/`](design/sugestoes/logos/): símbolos portal/blocos/chave, app icons, wordmark CondoUrban (placeholder T4), amostra HTML.

### Adicionado (2026-09-29 — sugestões visuais)

- Pasta [`docs/design/sugestoes/`](design/sugestoes/README.md): paletas A–D, 3 layouts de home, ícones; hub HTML em `sugestoes/index.html`.
- D1–D3 apontam para o comparativo.

### Alterado (2026-09-29 — revisão consolidada)

- Doc [14](plano/14-revisao-plano-consolidada.md): reorganização de fases, grupos de módulos, infra em escada.
- [ADR-005](decisoes/ADR-005-persistencia-sqlite-para-postgres.md): SQLite (`:memory:`/arquivo) → PostgreSQL.
- Acionamentos: **Fase 4** (não F2). Redes sociais: track **M5** (não “Fase 10” após IA).
- Pets com automóveis na F2; Fale Conosco em M0/F1; F3 sem “financeiro” no título.
- Roadmap 03 / catálogo 06 / perguntas F1/F8–F10/T12 atualizados.

### Adicionado (2026-09-29 — fase 10 redes sociais)

- Perfis oficiais em redes (agora **M5** GTM; checklist no roadmap 03).
- Perguntas **M5–M6** em 05-perguntas-abertas.md.

### Adicionado (2026-09-29 — segurança + domínios)

- Doc [13](plano/13-seguranca-plataforma-logs-e-ddos.md): `AuditLog`, `UsageEvent`, rate-limit buckets, anti-DDoS (CDN/WAF).
- Arquitetura **por domínios** (bounded contexts) em [02](plano/02-arquitetura-tecnica.md); T10/T11 em perguntas abertas.
- Roadmap Fase 1: itens 1.9–1.12; esqueleto por domínios em 1.1.
- FAQ privacidade + política: logs de auditoria/uso e bloqueio por rate limit.

### Adicionado (2026-09-29 — fases 7-9)

- Novas funcionalidades e fases: comunidade (7), IoT/automação (8), inteligência (9).
- Fase 2 ampliada: Convites, Acionamentos piloto, centro de notificações, automóveis.
- Fase 3: mudança, achados e perdidos, pets, Fale Conosco.


### Adicionado (2026-09-29 — design)

- Pasta `docs/design/`: [paleta-cores.md](design/paleta-cores.md), [paleta-amostra.html](design/paleta-amostra.html), [tipografia.md](design/tipografia.md).

### Adicionado (2026-09-29 — lojas)

- Fase 6: publicacao App Store + Google Play via Capacitor ([12-publicacao-lojas-apple-play.md](plano/12-publicacao-lojas-apple-play.md)).
- Perguntas S1-S4 em 05-perguntas-abertas.md.


### Adicionado (2026-09-29 — repo / referência)

- Prints em `docs/referencia/app-concorrente/` (5 JPGs + README).
- `.gitignore`, `.env.example` e `.env` local (gitignored).
- Ritual segurança/FAQ/políticas ([10](plano/10-seguranca-faq-politicas-ritual.md)); rascunhos em `docs/conteudo/`.
- Inventário app concorrente × versões ([09](plano/09-inventario-referencia-e-versoes.md)).

### Planejado

- F1, F2, F7, F10, F11, I1–I5, T4, T8, M1–M4, S1–S4; Django vs FastAPI.

### Adicionado (2026-09-29 — facial / reservas)

- Doc [08-intelbras-facial-e-reservas.md](plano/08-intelbras-facial-e-reservas.md) e [ADR-004](decisoes/ADR-004-integracao-intelbras-facial.md).
- F5/F6 resolvidas: pré-cadastro facial + integração Intelbras; F3 reforçada (reservas obrigatórias Fase 2).
- Roadmap Fase 2: itens 2.3–2.4 (facial + Intelbras); 2.6 reservas.

### Alterado (P3, 2026-09-29)

- Fase 1 **sem** módulo financeiro in-app; pagamentos na contabilidade externa. Item roadmap 1.7 cancelado na Fase 1.

### Adicionado

- ADR-003: estilização (Material/PrimeNG + Tailwind), portabilidade web, VPS.

### Alterado

- Respostas stakeholder em `05-perguntas-abertas.md` (multi-condomínio, ambos pagantes, Fase 2 portaria/reservas, sem chat, LGPD F1, dependentes).
- ADR-002 **Aceito**; arquitetura: **um app Angular** por perfil + `web-marketing`.
- Início da Fase 1 (fundação técnica).

### Alterado

- Visão replanejada: **produto completo** entregue por fases (`docs/plano/06-produto-completo-modulos.md`).
- Arquitetura alvo migrada para **Python + Angular** (`docs/decisoes/ADR-002-stack-python-angular.md`).
- Convenção em `05-perguntas-abertas.md`: **não apagar perguntas**; respostas na coluna **Resposta** (histórico permanente).
- Plano landing de vendas, políticas, FAQ e conteúdo compartilhado com o app (`docs/plano/07-landing-page-marketing-e-conteudo-comum.md`).

---

## [2026-09-29]

### Adicionado

- Estrutura completa de documentação em `docs/` (planos, histórico, decisões).
- Planos: visão geral, funcionalidades, arquitetura, roadmap, status, perguntas abertas.
- ADR-001: documentação versionada e stack inicial provisória.
- Journal da sessão: `historico/journal/2026-09-29-estrutura-documentacao.md`.
- README na raiz apontando para a documentação.

### Contexto

- Projeto iniciado a partir do planejamento do app de condomínio Web + PWA; workspace estava vazio; nenhum código de aplicação ainda.

---

## Template para novas entradas

```markdown
## [AAAA-MM-DD]

### Adicionado / Alterado / Corrigido / Removido

- Descrição objetiva (#issue ou ADR se houver).
```
