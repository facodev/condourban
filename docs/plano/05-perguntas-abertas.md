# Perguntas abertas

Registro **permanente** de perguntas de descoberta. O texto da **Pergunta nunca é apagado** — quando houver decisão, preencha a coluna **Resposta** na mesma linha.

## Regras de edição

1. **Não remover** linhas da tabela nem reescrever a pergunta para "sumir" com ela.
2. **Não mover** a resposta para outro arquivo *no lugar* da pergunta; a resposta fica aqui **e** pode ser espelhada nos planos/ADRs.
3. Coluna **Resposta**: substituir `_pendente_` pelo texto da decisão.
4. Coluna **Status**: `aberta` — `resolvida (AAAA-MM-DD)` ou `parcial`.
5. Novas perguntas: **sempre adicionar** nova linha com novo ID.

### Depois de responder

- Espelhar o essencial nos planos (`00`?`07`) ou ADR.
- Entrada no `historico/CHANGELOG.md`.

---

## Produto / negócio

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| P1 | Um condomínio ou administradora com vários? | **Vários condomínios** — plataforma multi-condomínio (administradora ou operação com N prédios). | resolvida (2026-09-29) |
| P2 | Quem é o cliente pagante: síndico, administradora ou ambos? | **Ambos** — síndico e administradora como clientes pagantes (modelo comercial a detalhar). | resolvida (2026-09-29) |
| B1 | Qual o **modelo de negócios** oficial (híbrido de cobrança)? | _pendente_ — opções e híbrido sugerido em [17](17-modelos-de-negocio-e-precificacao.md); fechar em [18](18-decisoes-a-tomar.md) §2 item **2.1**. | aberta |
| P3 | Financeiro na Fase 1: controle/upload ou Pix/boleto registrado (catálogo prevê gateway na Fase 4)? | **Ainda não** — na Fase 1 **não** haverá cobrança, upload de boleto, Pix ou gateway no app; **pagamentos ficam por fora**, feitos na **contabilidade**. Módulo financeiro in-app (consulta, 2ª via, integrações) fica para **fase posterior** (catálogo: evolução até Fase 4). | resolvida (2026-09-29) |
| P4 | Portal portaria na Fase 1 ou a partir da Fase 2 (como no doc 06)? | **A partir da Fase 2** (portal portaria alinhado ao doc 06). | resolvida (2026-09-29) |
| P5 | White-label: logo/cores por condomínio ou só marca única da plataforma? | **Personalização por condomínio** — cada tenant pode customizar **algumas partes** (logo, cores de destaque, nome de exibição, regras/horários). **Módulos on/off** ficam no modelo de planos/entitlement ([ADR-011](../decisoes/ADR-011-planos-e-funcionalidades.md), [planos-e-entitlements](../funcionalidades/10_transversal_plataforma/planos-e-entitlements.md)), não só em JSONB. Marca da plataforma permanece como casca padrão; **não** é white-label total. Entrega UX na **Fase 4** (4.3); `condominio.configuracoes` desde a fundação (branding/regras). Spec branding: [configuracao-condominio](../funcionalidades/02_condominio/configuracao-condominio.md). | resolvida (2026-09-29; refinada 2026-09-30) |
| P8 | Funcionalidades por plano e/ou por condomínio? | **Ambos** — plano define o que está **licenciado**; `condominio_funcionalidade` permite override (desligar operacionalmente ou ligar cortesia/add-on via admin plataforma). Núcleo sempre on. [ADR-011](../decisoes/ADR-011-planos-e-funcionalidades.md). | resolvida (2026-09-30) |
| P6 | Onboarding do morador: convite e-mail/SMS, código da unidade, aprovação do síndico? | _pendente_ | aberta |
| P7 | Inquilino vs proprietário: permissões diferentes no app? | _pendente_ | aberta |

## Funcionalidades

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| F1 | Fase 1 (doc 06) — ajustes no catálogo? | **Sim (revisão 2026-09-29)** — ver [14](14-revisao-plano-consolidada.md): infra em escada, Fale Conosco na F1, CDN/WAF no 1º deploy público. | resolvida (2026-09-29) |
| F2 | Assembleia/votação: Fase 3 (doc 06) ou antecipar? | _pendente_ | aberta |
| F3 | Reservas: Fase 2 (doc 06) ou antecipar? | **Fase 2** — reservas são **obrigatórias** no produto; entrega na Fase 2 (sem antecipar para Fase 1). Ver doc 08. | resolvida (2026-09-29) |
| F4 | Chat ou apenas comunicados + tickets? | **Apenas comunicados** (+ ocorrências/tickets; sem chat). | resolvida (2026-09-29) |
| F5 | Produto deve ter pré-cadastro com reconhecimento facial e liberação de pessoas? | **Sim** — pré-cadastro de pessoas (moradores/visitantes) com facial e liberação de acesso. | resolvida (2026-09-29) |
| F6 | Integração com Intelbras para reconhecimento facial? | **Sim** — integração **Intelbras** (adaptador no backend); detalhes de linha/produto/API em I1–I4. Docs: [08](08-intelbras-facial-e-reservas.md), [ADR-004](../decisoes/ADR-004-integracao-intelbras-facial.md). | resolvida (2026-09-29) |
| F7 | "Mensagem" da referência: descartar (F4) ou mensagens 1:1 sem chat em tempo real? | _pendente_ | aberta |
| F8 | Incluir módulos sociais/cadastros da referência nas versões V2–V5 (classificados, galeria, pets, mudança, achados, vizinho amigo, clube)? | **Sim** — auto+pets **Fase 2**; mudança/achados **Fase 3**; classificados/galeria/vizinho/clube **Fase 7**. | resolvida (2026-09-29) |
| F9 | Confirmar Fases 7–9 (comunidade, IoT, inteligência) no roadmap? | **Sim** — docs 03/06/14. | resolvida (2026-09-29) |
| F10 | Acionamentos (abrir portão pelo app) já na Fase 2 ou só após Intelbras estável? | **Fase 4** — após Intelbras estável (não sobrecarregar F2). | resolvida (2026-09-29) |
| F11 | Câmeras ao vivo entram no produto (Fase 8) ou ficam fora? | _pendente_ | aberta |
| F12 | “Visita discreta” / soft-delete de histórico de visitas no MVP da Fase 2? | **Provisão:** **não** no MVP — só isolamento por unidade + fluxo espontâneo na portaria. Discreta/soft-delete = avaliar depois (risco de culpa no app se o morador esquecer de cadastrar ou achar que “o app escondeu”). Termos §8. | parcial (2026-09-29) |
| F13 | Advertências digitais na Fase 3 **sem** multa financeira (só pós-P3)? | _provisão: sim — modelos + leitura + anexos na F3; valor $ depois_ | parcial (2026-09-29) |
| F14 | Smart locker: provedores piloto (Clique Retire, Meu Locker, Biccateca, Handover…)? | _pendente_ | aberta |
| F15 | Assinatura eletrônica de ata/termos: ClickSign, Autentique ou outro? | _pendente_ | aberta |
| F16 | Confirmar profundidade portaria F2: troca de turno + chaves/objetos + procedimentos? | _provisão: sim — roadmap 2.15–2.17_ | parcial (2026-09-29) |

## Técnico / operação

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| T1 | Stack front/back | **Angular 22+ e Python FastAPI** (API REST assíncrona, SQLAlchemy 2.0 e Alembic). Decisão formalizada em [ADR-001](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md). | resolvida (2026-10-17) |
| T2 | Hosting preferido (Vercel, AWS, on-prem)? | **VPS** (deploy containerizado; controle de custo e dados). | resolvida (2026-09-29) |
| T3 | Apenas PT-BR? | **Por enquanto só PT-BR**; arquitetura preparada para i18n depois. | resolvida (2026-09-29) |
| T4 | Nome do produto e identidade visual? | **Nome: CondoUrban** (`condourban`). **Logo primária** definida ([oficial](../design/sugestoes/logos/oficial/)). Favicon/app icon e tipografia ainda abertos. | parcial (2026-10-01) |
| T5 | Confirmar Python + Angular em vez de Next/Node? | **Confirmado** — stack oficial front/back. | resolvida (2026-09-29) |
| T6 | Um app Angular (lazy modules) ou apps separados morador/portaria/admin? | **Mesmo aplicativo**, com **visão e rotas diferentes por perfil** (guards, layouts lazy-loaded). Landing pode ser app separado `web-marketing` (SSR). | resolvida (2026-09-29) |
| T7 | React seria alternativa interessante? | **Sim, tecnicamente válida** (web + PWA); **não adotada** — stakeholder confirmou Angular (T5). Manter decisão documentada para histórico. | resolvida (2026-09-29) |
| T8 | Qual biblioteca/framework de estilização (landing + componentes)? | _provisão: ver [ADR-003](../decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md)_ — Material + Tailwind ou PrimeNG; confirmar na implementação. | parcial (2026-09-29) |
| T9 | Portabilidade: app deve funcionar na web — qual abordagem? | **Web first**: Angular no **navegador** (desktop/tablet/mobile) + **PWA**; backend Python em **Docker na VPS**. Sem dependência de loja de apps; código TS compila para padrões web abertos. | resolvida (2026-09-29) |
| T10 | Organizar código por camadas genéricas ou por **domínios**? | **Por domínios** (bounded contexts): identity/tenancy, communication, access, amenities, tickets, finance, governance, saas, content_public, audit_usage, etc. Django apps ou pacotes FastAPI + features Angular por domínio. Ver [02](02-arquitetura-tecnica.md). | resolvida (2026-09-29) |
| T11 | Auditoria + logs de uso + anti-DDoS / rate-limit buckets são obrigatórios? | **Sim** — desde a fundação, com **escada**: AuditLog cedo; rate-limit in-process→Redis; CDN/WAF no deploy público. [13](13-seguranca-plataforma-logs-e-ddos.md). | resolvida (2026-09-29) |
| T12 | Banco em memória no início e crescer depois? | **Sim** — testes `:memory:`; **dev = SQLite arquivo**; staging/prod = **PostgreSQL**. ORM+migrations desde o dia 1. [ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md). | resolvida (2026-09-29) |

## Conformidade

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| C1 | Termos LGPD, exportação e exclusão já na Fase 1? | **Sim, já na Fase 1** — políticas, exportação e exclusão no escopo da fundação. | resolvida (2026-09-29) |
| C2 | Cadastro inclui dependentes/menores na unidade? | **Sim, inclui** dependentes/menores vinculados à unidade (com cuidados LGPD). | resolvida (2026-09-29) |

## Integração Intelbras / acesso facial

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| I1 | Qual linha/produto Intelbras (ex.: Control iD, InControl, SS, outro) e documentação/API disponível? | _pendente_ | aberta |
| I2 | Dispositivos ficam na rede local do condomínio — VPS na nuvem precisa de VPN/túnel/on-prem agent? | _pendente_ | aberta |
| I3 | Captura da face: webcam no app (morador), tablet na portaria, ou ambos? | _pendente_ | aberta |
| I4 | Visitante: só facial, facial + QR, ou QR como fallback obrigatório? | _provisão: facial + QR fallback (ADR-004)_ | parcial (2026-09-29) |
| I5 | Se a VPS/API cair, a liberação facial local (Intelbras) continua? Qual modo degradado? | _pendente_ | aberta |

## Notificações

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| N1 | Canais na Fase 1: push + e-mail; SMS só depois? | _pendente_ | aberta |
| N2 | WhatsApp Business API: na Fase 4 (canal) ou só após push estável / F9 assistente? | _provisão: canal notificações F4; assistente conversacional F9_ | parcial (2026-09-29) |

## Marketing / landing

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| M1 | Domínio: `www` + `app` (subdomínios) ou outro esquema? | _pendente_ | aberta |
| M2 | Trial self-service na landing ou só demo/contato comercial? | _pendente_ | aberta |
| M3 | Edição de FAQ/políticas: Django Admin, CMS na admin plataforma ou Markdown no repo? | _pendente_ | aberta |
| M4 | Landing: Angular SSR no monorepo (doc 07) ou site estático separado? | _pendente_ | aberta |
| M5 | Quais redes sociais oficiais (Instagram, LinkedIn, Facebook, outras)? | _provisão: Instagram + LinkedIn no mínimo; Facebook opcional — track **M5** (GTM), paralelo à F1+_ | parcial (2026-09-29) |
| M6 | Quem opera as redes (interno vs agência) e tom de voz da marca? | _pendente_ | aberta |

## Lojas (App Store / Google Play)

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| S1 | Confirmar publicação nas lojas via **Capacitor** (empacotar Angular) na Fase 6? | _provisão: sim — doc 12_ | parcial (2026-09-29) |
| S2 | Lojas para qual público primeiro: só morador, ou também síndico/portaria? | _pendente_ | aberta |
| S3 | Contas Apple Developer / Google Play: pessoa física, MEI ou empresa (CNPJ)? | _pendente_ | aberta |
| S4 | Nome do app nas lojas (pode diferir do nome web — T4)? | _pendente_ | aberta |

## Design / identidade

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| D1 | Paleta: A verde, B laranja, C ardósia, D oliva, **E roxo ameixa** `#5B3A6E`, **F azul cobalto** `#1565C0`? Ver [sugestoes](../design/sugestoes/README.md). | _pendente_ | aberta |
| D2 | Confirmar UI kit: PrimeNG ou Angular Material (+ Tailwind na landing)? Ícones: Lucide / Material / Phosphor — [sugestoes/icones.md](../design/sugestoes/icones.md). | _pendente_ | aberta |
| D3 | Tipografia: Source Sans 3 / IBM Plex no app + fonte display na landing — ok? Layout home: Grade / Destaques / Lista — [sugestoes/layouts.md](../design/sugestoes/layouts.md). | _pendente_ | aberta |

## Hospedagem (detalhe VPS)

| ID | Pergunta | Resposta | Status |
|----|----------|----------|--------|
| H1 | Qual provedor VPS (Hetzner, DigitalOcean, Contabo, outro BR)? | _pendente_ | aberta |
| H2 | Proxy TLS: Caddy ou Nginx+certbot? | _pendente_ | aberta |
| H3 | Staging: segundo VPS/compose ou só produção no início? | _pendente_ | aberta |

---

## Status deste documento

| Campo | Valor |
|-------|-------|
| Última revisão | 2026-09-30 — B1 modelo de negócios; checklist [18](18-decisoes-a-tomar.md) |
| Convenção | Perguntas não são apagadas; respostas na coluna **Resposta** |
