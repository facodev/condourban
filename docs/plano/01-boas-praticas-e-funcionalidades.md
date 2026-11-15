# Boas práticas e funcionalidades

O escopo funcional **completo** está em [06-produto-completo-modulos.md](06-produto-completo-modulos.md). Este arquivo resume práticas transversais e como as fases se relacionam ao catálogo.

## Boas práticas (Web + PWA)

### UX e produto

- Papéis claros em **cada portal** (morador, portaria, síndico, administradora).
- Fluxos críticos da portaria otimizados para **tablet** e **celular** (toque, poucos cliques).
- Notificações push, e-mail e (opcional) SMS para eventos configuráveis por condomínio.
- Offline parcial no morador: comunicados e documentos já baixados; fila de ocorrências.

### Segurança e compliance

- MFA para perfis sensíveis (Fase 5 ou antes se exigido).
- Isolamento tenant em **100%** das queries e testes automatizados de vazamento cross-tenant.
- **Auditoria** imutável (append-only) para auth, papéis, votação, financeiro, liberação de visitantes e acionamentos.
- **Logs de uso** (produto/API) separados da auditoria — capacidade, SaaS e detecção de abuso.
- **Buckets de rate limit** (Redis) por IP, usuário, tenant e endpoints sensíveis; 429 + `Retry-After`.
- **Anti-DDoS**: CDN/WAF na frente da VPS + limites no proxy; detalhe em [13](13-seguranca-plataforma-logs-e-ddos.md).
- Uploads: validação, limite, scan em produção.
- Ritual permanente: [10](10-seguranca-faq-politicas-ritual.md).

### PWA (Angular)

- Service worker com estratégias por tipo de recurso (shell, API read-only, assets).
- Web Push via backend Python (VAPID).
- Atualização controlada da app (prompt ao usuário).

### Geração de código Angular com IA

Fonte oficial: [LLM prompts and AI IDE setup](https://angular.dev/ai/develop-with-ai).

| Recurso | Uso neste repo |
|---------|----------------|
| Prompt / best practices Angular | Regra Cursor [`.cursor/rules/angular-ai-best-practices.mdc`](../../.cursor/rules/angular-ai-best-practices.mdc) (aplica em arquivos do front) |
| Contexto ampliado | [llms.txt](https://angular.dev/llms.txt) · [llms-full.txt](https://angular.dev/llms-full.txt) |
| MCP do Angular CLI (experimental) | Habilitar no IDE quando o app Angular existir (`ng mcp`) |

Convenções que a regra reforça (resumo): componentes **standalone** (sem `standalone: true` em v20+); **signals** + `input()`/`output()`/`model()`; control flow nativo (`@if`/`@for`/`@switch`); Signal Forms (v22+) ou Reactive Forms; acessibilidade WCAG AA / AXE; lazy load de rotas; `inject()`; sem `ngClass`/`ngStyle`/`CommonModule` genérico.

### Engenharia

- **Estrutura por 9 Bounded Contexts** no backend (`backend/app/modulos/`) e features Angular (`frontend/src/app/features/`) — [ADR-013](../decisoes/ADR-013-organizacao-diretorios.md), [Estrutura.md](../decisoes/Estrutura.md) e [02](02-arquitetura-tecnica.md).
- OpenAPI como fonte de verdade da API FastAPI; client Angular gerado no CI; tags por Bounded Context.
- Testes: unitários por Bounded Context; integração API + tenant isolado; e2e nos fluxos críticos por fase.
- Observabilidade: logs estruturados, tracing, métricas de filas Celery.
- **Refactoring e limpeza contínuos** (abaixo e itens **R1–R8** no [03](03-roadmap-e-entregas.md)).

### Refactoring e limpeza contínua

Higiene **não é fase futura** — entra no Pronto de cada entrega, junto com o ritual de segurança/FAQ ([10](10-seguranca-faq-politicas-ritual.md)).

| Objetivo | Exemplos |
|----------|----------|
| Código obsoleto | Feature flags eternas, ramos de chat/Keycloak, stubs nunca ligados |
| Código repetido | Copiar-colar de checagem de tenant, serializers, DTOs quase iguais |
| Docs / DDL fantasma | Tabelas adiadas ainda “vivas” sem uso; specs duplicadas; links mortos |
| Dependências mortas | Pacotes no lockfile sem import; polyfills desnecessários |
| Dívida nomeada | Comentário `TODO` sem ticket → virar item R* ou ADR |

**Como fazer**

1. Em todo PR de feature: remover o que o PR tornou morto (não deixar “por enquanto”).
2. Sprints de fundação / entre fases: dedicar fatia a **R1–R8** (roadmap).
3. Antes de grande mudança de domínio: extrair e apagar duplicatas no perímetro tocado.
4. Nunca reintroduzir o pacote em `historico/arquivo/` no canônico.
5. Mudança de contrato público → ADR + CHANGELOG; só limpeza interna → nota curta no journal.

Itens rastreáveis: [03 § Higiene contínua](03-roadmap-e-entregas.md#higiene-contínua--refactoring-e-limpeza).

---

## Relação fases — funcionalidades por Bounded Context

| Fase | Foco de valor | Bounded Contexts e Módulos envolvidos |
|------|---------------|---------------------------------------|
| 1 | Fundação + convivência | `transversal` (auth, AuditLog, PWA), `identidade_cadastro` (pessoas, usuários, membros, unidades), `comunicacao` (comunicados, Fale Conosco), `governanca` (documentos), `manutencao` (ocorrências); persistência SQLite→Postgres |
| 2 | Operação do prédio | `portaria` (atendimento visitantes, encomendas), `controle_acesso` (facial/Intelbras, credenciais), `reservas` (áreas comuns, vistorias), `comunicacao` (enquetes), `identidade_cadastro` (veículos e pets) |
| 3 | Governança + operações | `governanca` (assembleias, votações, atas), `manutencao` (chamados, OS zelador, PMO preventivo), `portaria` (mudanças, achados e perdidos) |
| 4 | Escala B2B + acesso | `financeiro` (boletos, Pix, conciliação pós-P3), `transversal` (SaaS planos × funcionalidades, personalização/branding P5), `controle_acesso` (acionamentos remotos, multi-provider) |
| 5 | Maturidade | `transversal` (MFA, BI/uso, PWA endurecido, integração SIEM) |
| 6 | Lojas | `transversal` (App Store + Google Play via Capacitor) |
| 7 | Comunidade | `comunicacao` (mural da comunidade, classificados, galeria) |
| 8 | IoT | `controle_acesso` / `transversal` (cenas IoT, telemetria, sensores avançados) |
| 9 | Inteligência | `transversal` (busca semântica, OCR de documentos/etiquetas, moderação assistida) |
| GTM | Marketing / redes | `transversal` (Landing M0–M3 + M5 redes sociais paralelo à F1+) |

Detalhamento módulo a módulo: [06-produto-completo-modulos.md](06-produto-completo-modulos.md).  
Especificações funcionais: [`docs/funcionalidades/`](../funcionalidades/README.md).

---

## O que **não** fazemos

- Entregar "protótipo" sem tenant, sem auditoria ou sem API versionada na Fase 1.
- Acoplar regra de negócio crítica só no front (Angular é UI; Python é decisão).
- Tratar fases futuras como "nice to have" no modelo de dados — entidades futuras podem ser migradas tarde, mas **tenancy e identidade** são completos desde o início.

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-10-17 — alinhamento aos 9 Bounded Contexts e 26 specs |
