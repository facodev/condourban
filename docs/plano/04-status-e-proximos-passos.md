# Status Atual e Próximos Passos

> **Ponto de entrada** ao retomar o projeto em qualquer ambiente.  
> Roadmap reestruturado por Bounded Contexts: [03-roadmap-e-entregas.md](03-roadmap-e-entregas.md).

## Resumo Executivo

| Campo | Valor |
|---|---|
| Visão | Produto **completo**, entrega modular por **10 Fases por Bounded Context (BC-00 a BC-09)** |
| Metodologia | **`tlc-spec-lean`** (`plan.md` com EARS e portas de sentido único → `checks.md` com provas `pytest` → `verification.md` independente) |
| Stack | **FastAPI + Angular 22+ Standalone**, SQLite (dev/testes) → PostgreSQL 16+ RLS (staging/prod) |
| Segurança & RLS | Isolamento multi-tenant estrito por `condominio_id`, `evento_auditoria` imutável e proteção anti-DDoS |
| Fase Atual | **Pilares Essenciais de Dados (BC-01 e BC-02) Concluídos** |
| Status da Suíte | **60 testes automatizados passando com 100% de sucesso** em `pytest` |
| Integração E2E UI | **Frontend Angular 22+ & Backend FastAPI 100% integrados e operacionais (BC-01 & BC-02)** |
| Última Atualização | 2026-10-30 — Integração E2E Frontend-Backend e Validação dos Módulos BC-01 e BC-02 |

---

## Concluído

- [x] **Governança de ADRs:** ADR-001 (stack canônica FastAPI + Angular), ADR-005 (escada de persistência), ADR-006 (isolamento RLS), ADR-008 (separação pessoa/usuário), ADR-010 (pt-BR snake_case), ADR-011 (entitlements SaaS) e **[ADR-013: Organização de Diretórios](../decisoes/ADR-013-organizacao-diretorios.md)** / **[Estrutura.md](../decisoes/Estrutura.md)**.
- [x] **Reorganização de Funcionalidades:** 26 especificações funcionais e documentos de domínio mapeados para os 9 Bounded Contexts em [`docs/funcionalidades/`](../funcionalidades/README.md) e [`MAPA.md`](../funcionalidades/MAPA.md).
- [x] **Reestruturação do Roadmap (doc 03):** Migração definitiva do modelo legado de fases fragmentadas para **10 Fases por Bounded Context unificados**, com matriz topológica e 3 trilhas paralelas independentes.
- [x] **Marco 0: Fundação Transversal & Core Base Concluído (`tlc-spec-lean`):**
  - Autenticação JWT próprio e Google OAuth 2.0 (`identidade_cadastro/auth/`).
  - Injeção de contexto de tenant e ativação de RLS no PostgreSQL via `condominio_id`.
  - Trilha forense imutável de auditoria (`evento_auditoria`).
  - Shell Angular PWA com lazy loading por Bounded Context, guards (`auth.guard`, `papel.guard`) e Service Worker PWA.
  - 30 checks C1–C30 verificados e aprovados sob `.specs/features/fase-1-fundacao/`.
- [x] **Pilares Essenciais de Dados — BC-01: Identidade e Cadastro Completo Concluído (`tlc-spec-lean`):**
  - Unificação de todos os 4 submódulos de `01_identidade_cadastro` (`pessoas/`, `usuarios/`, `onboarding/`, `veiculos_pets/`).
  - Implementação das 5 regras invariantes de ocupação da unidade (posse direta, curtos prazos, retroatividade, expiração automática com CLI e dependência com cascade).
  - Ciclo de auto-onboarding com emissão de convites (7 dias), submissão de cadastro, fila de aprovação e rejeição com motivo obrigatório.
  - Cadastro e controle de veículos com validação de placa em maiúsculas sem hífen e bloqueio de placas duplicadas no mesmo condomínio.
  - Cadastro de animais domésticos para controle comunitário e sanitário.
  - 22 checks C1–C22 verificados e aprovados sob `.specs/features/bc-01-identidade-cadastro/` com veredicto PASS.
- [x] **Pilares Essenciais de Dados — BC-02: Condomínio e Estrutura Física Concluído (`tlc-spec-lean`):**
  - Estrutura física: blocos e unidades habitacionais com validação de unicidade (`UNIDADE_DUPLICADA` com HTTP 400) e importação em lote CSV.
  - Garagens: cadastro, listagem e vinculação de vagas a unidades com restrição de unicidade por condomínio (`VAGA_DUPLICADA` com HTTP 400).
  - Áreas comuns: catálogo de espaços de lazer/convivência, capacidade, regras de aprovação e interdição operacional para manutenção (`PATCH` com `ativo=False`).
  - Perfil e branding: consulta e atualização cadastral do condomínio (`/info`) e parametrização JSON de branding (cores, logos) e regras operacionais/convivência (`/configuracoes`).
  - 18 checks C1–C18 verificados e aprovados sob `.specs/features/bc-02-condominio/` com veredicto PASS.
- [x] **Integração E2E Frontend-Backend e Telas Operacionais (BC-01 & BC-02):**
  - Configuração do proxy Angular dev server (`proxy.conf.json`) conectando a UI (`http://localhost:4200`) à API FastAPI (`http://127.0.0.1:8000`).
  - Fluxo de login autenticado com claims JWT, sincronização de sessão e compatibilidade de rotas.
  - BC-02 na UI: criação e listagem de blocos (`BlockFormComponent`), unidades associadas a blocos com validação (`UnitFormComponent`) e catálogo de áreas comuns com interdição/liberação (`AreasComunsComponent`).
  - BC-01 na UI: gestão de pessoas, visualização de usuários e perfis RBAC, ciclo de auto-onboarding (convites, aprovação e rejeição justificada) e gestão de veículos e pets.
  - Auditoria independente via protocolo TLC-Spec-Lean com veredicto **PASS**.

---

## Em Andamento / Próximas Fases (Trilhas Paralelas Liberadas)

Com a conclusão dos pilares mestres de dados (**BC-01** e **BC-02**), as três trilhas de desenvolvimento estão completamente liberadas para execução paralela:

1. **Trilha A (Hardware & Portaria):**
   - **BC-03: Controle de Acesso IoT** (Dispositivos, biometria facial, tags RFID, sincronização assíncrona tolerante a falhas e trilha forense de passagens).
   - **BC-04: Portaria e Atendimento** (Guarita, atendimento unificado de visitantes, prestadores, delivery com código e encomendas com foto).
2. **Trilha B (Social & Operacional):**
   - **BC-05: Reservas e Espaços Comuns** (Agendamento, concorrência, lista de convidados, termos e vistorias).
   - **BC-06: Comunicação Comunitária** (Comunicados urgentes com push, livro unificado de ocorrências e mural comunitário).
3. **Trilha C (Governança, Finanças & PMO):**
   - **BC-07: Governança e Assembleias** (Assembleias híbridas Lei 14.309, pautas, procurações e votação digital).
   - **BC-08: Financeiro e Faturamento** (Boletos, Pix dinâmico, conciliação e rateio).
   - **BC-09: Manutenção Preventiva PMO** (Cronograma preventivo e ordens de serviço).

## Status deste Documento

| Campo | Valor |
|---|---|
| Status | `vivo` |
| Última revisão | 2026-10-18 — Alinhamento integral ao modelo Bounded-Context-First e método tlc-spec-lean |
