# Decisões a serem tomadas

Lista **acionável** do que ainda precisa fechar com o stakeholder.  
Histórico detalhado das perguntas (IDs P/T/D/H…): [05-perguntas-abertas.md](05-perguntas-abertas.md).  
Quando decidir: marcar aqui → preencher a **Resposta** no 05 (se houver ID) → espelhar em ADR/plano → CHANGELOG.

**Legenda de prioridade**

| Tag | Significado |
|-----|-------------|
| **P0** | Bloqueia branding, landing ou GTM |
| **P1** | Bloqueia spike técnico / deploy |
| **P2** | Importante antes da fase indicada |
| **P3** | Pode esperar; não trava fundação |

Status: `aberta` · `parcial` · `fechada (AAAA-MM-DD)`

---

## 1. Marca e identidade — **P0**

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 1.1 | **Definir o nome** do produto | T4 · [nomes-marca](../design/sugestoes/nomes-marca/README.md) | **decidida** | **CondoUrban** (`condourban`) — 2026-10-01 |
| 1.2 | **Definir a logo** (primária + favicon + app icon) | T4 · [logos](../design/sugestoes/logos/) | **parcial** | Logo primária: [`oficial/condourban-logo.png`](../design/sugestoes/logos/oficial/condourban-logo.png) (2026-10-01). Favicon / app icon ainda abertos. |
| 1.3 | Definir paleta de cores oficial | D1 · [paleta](../design/paleta-cores.md) | aberta | |
| 1.4 | Definir tipografia (app + landing) | D3 · [tipografia](../design/tipografia.md) | aberta | |
| 1.5 | Definir kit de ícones | D2 · [icones](../design/sugestoes/icones.md) | aberta | |
| 1.6 | Nome do app nas lojas (pode diferir do web) | S4 | aberta | Após 1.1 |

---

## 2. Modelo de negócios e precificação — **P0 / P2**

Catálogo de opções e híbrido sugerido: [17-modelos-de-negocio-e-precificacao.md](17-modelos-de-negocio-e-precificacao.md).  
Entitlement técnico (planos × módulos): [ADR-011](../decisoes/ADR-011-planos-e-funcionalidades.md).

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 2.1 | **Definir o modelo de negócios** oficial (híbrido a adotar) | 17 §4 · P2 | aberta | Ex.: fixo por condo + faixas + add-ons claros |
| 2.2 | Pagador principal no GTM: síndico, administradora ou ambos? | 17 §6 · P2 | parcial | P2 = ambos; falta ênfase de GTM |
| 2.3 | Preço **público** na landing ou só orçamento? | 17 §6 · M2 | aberta | |
| 2.4 | Nomes e faixas dos tiers (Starter / Essencial / Acesso / …) + valores | 17 §4 · 4.2a | aberta | Seed atual é placeholder |
| 2.5 | Facial / Intelbras incluso em qual tier? | 17 §6 | aberta | |
| 2.6 | Taxa de implantação / setup: obrigatória? valor? | 17 §6 | aberta | |
| 2.7 | Fidelidade mínima (mês a mês vs 12 meses)? | 17 §6 | aberta | |
| 2.8 | Desconto anual e de volume (administradora)? | 17 §6 | aberta | |
| 2.9 | Quais add-ons são aceitáveis (SMS, assembleia avulsa, …)? | 17 §6 · ADR-011 | aberta | |
| 2.10 | Trial: dias, cartão obrigatório?, limites? | 17 §6 · M2 | aberta | |
| 2.11 | Quando ativar take rate financeiro in-app? | 17 §6 · P3 | aberta | Só após financeiro in-app |

---

## 3. Hospedagem e infra — **P1**

Decisão macro **VPS + Docker** já fechada (T2). Falta detalhe operacional.

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 3.1 | **Definir hospedagem** — provedor VPS | H1 · [11](11-lacunas-e-complementos.md) | aberta | Hetzner / DO / Contabo / BR… |
| 3.2 | Spec inicial (vCPU, RAM, disco) e região | 11 §2 | aberta | Provisão: 4 vCPU / 8 GB |
| 3.3 | Proxy TLS: Caddy ou Nginx+certbot? | H2 | aberta | |
| 3.4 | Staging: segundo VPS/compose ou só produção no início? | H3 | aberta | |
| 3.5 | CDN/WAF (provedor) no 1º deploy público | T11 · 13 | aberta | |
| 3.6 | Política de backup offsite (onde: R2/S3/outro) | 11 §2 | aberta | |

---

## 4. Domínio, presença e marketing — **P0 / P2**

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 4.1 | Comprar / definir domínio (ex.: `www` + `app`) | M1 | aberta | Após nome (1.1) |
| 4.2 | Trial self-service vs só demo/contato | M2 | aberta | Liga a 2.3 / 2.10 |
| 4.3 | Landing: Angular SSR no monorepo ou site estático? | M4 | aberta | |
| 4.4 | Onde editar FAQ/políticas (Admin / CMS / Markdown) | M3 | aberta | |
| 4.5 | Redes oficiais (Instagram, LinkedIn, …) | M5 | parcial | Provisão: IG + LinkedIn |
| 4.6 | Quem opera as redes e tom de voz | M6 | aberta | Após marca |

---

## 5. Stack e engenharia — **P1**

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 5.1 | Django vs FastAPI | T1 | **fechada (2026-10-01)** | **FastAPI** + SQLAlchemy 2 — [ADR-001](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md) e [ADR-012](../decisoes/ADR-012-backend-fastapi.md) |
| 5.2 | UI kit: PrimeNG vs Material (+ Tailwind landing) | T8 · D2 · ADR-003 | **fechada (2026-10-01)** | **Angular Material** no `web-app`; Tailwind na landing |
| 5.3 | Confirmar Capacitor para lojas (Fase 6) | S1 | parcial | Provisão: sim |
| 5.4 | Público das lojas primeiro (morador / síndico / portaria) | S2 | aberta | |
| 5.5 | Contas Apple / Google Play (PF, MEI, CNPJ) | S3 | aberta | |

---

## 6. Produto e fluxos — **P2**

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 6.1 | Onboarding do morador (convite, código, aprovação) | P6 | aberta | |
| 6.2 | Inquilino vs proprietário: permissões diferentes? | P7 | aberta | |
| 6.3 | Assembleia na Fase 3 ou antecipar? | F2 | aberta | |
| 6.4 | Mensagens 1:1 sem chat em tempo real? | F7 | aberta | Chat full = fora |
| 6.5 | Câmeras ao vivo na F8 ou fora do produto? | F11 | aberta | |
| 6.6 | Canais F1: push + e-mail; SMS depois? | N1 | aberta | |
| 6.7 | Timing WhatsApp Business | N2 | parcial | Canal F4; assistente F9 |
| 6.8 | Provedor smart locker piloto | F14 | aberta | |
| 6.9 | Assinatura eletrônica (ClickSign, Autentique, …) | F15 | aberta | |
| 6.10 | Fechar provisões F12/F13/F16 (visita discreta, advertências, portaria) | F12–F16 | parcial | |

---

## 7. Intelbras / acesso facial — **P1** (antes da F2)

| # | Decisão | Ref. | Status | Decisão / notas |
|---|---------|------|--------|-----------------|
| 7.1 | Linha/produto Intelbras + docs de API | I1 | aberta | |
| 7.2 | Conectividade condo ↔ VPS (VPN / túnel / agent) | I2 | aberta | |
| 7.3 | Captura da face: app, portaria ou ambos? | I3 | aberta | |
| 7.4 | Visitante: facial + QR (confirmar fallback) | I4 | parcial | Provisão ADR-004 |
| 7.5 | Modo degradado se a API cair | I5 | aberta | |

---

## 8. Ordem sugerida (desbloqueio)

```text
1. Nome (1.1) → Logo (1.2) → Paleta/tipo (1.3–1.5)
2. Modelo de negócios (2.1) + preço público vs orçamento (2.3) → tiers (2.4)
3. Domínio (4.1) + hospedagem provedor (3.1)
4. Django vs FastAPI (5.1) + UI kit (5.2)
5. Onboarding/papéis (6.1–6.2) · Intelbras (7.*) antes da Fase 2
```

---

## Como fechar uma linha

1. Preencher a coluna **Decisão / notas** e mudar **Status** para `fechada (AAAA-MM-DD)`.
2. Atualizar [05-perguntas-abertas.md](05-perguntas-abertas.md) (mesma resposta, nunca apagar a pergunta).
3. Se for arquitetura/produto durável → ADR em `docs/decisoes/`.
4. Atualizar [04-status](04-status-e-proximos-passos.md) e [CHANGELOG](../historico/CHANGELOG.md).

---

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Criado | 2026-09-30 |
| Última revisão | 2026-09-30 |
| Complementa | [05](05-perguntas-abertas.md) (histórico) · [17](17-modelos-de-negocio-e-precificacao.md) (opções comerciais) |
