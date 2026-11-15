# Lacunas e complementos (pós-descoberta)

Revisão de tudo já decidido versus o que ainda falta. Detalhes e tokens de design abaixo; perguntas novas em [05-perguntas-abertas.md](05-perguntas-abertas.md) (IDs D*, H*, P5+, F7+, N1, I5).

---

## 1. Design system (T4 / T8 ainda abertos)

> **Fonte da verdade das cores:** [docs/design/paleta-cores.md](../design/paleta-cores.md) · [amostra HTML](../design/paleta-amostra.html) · [tipografia](../design/tipografia.md)

### Paleta sugerida (provisão)

Diferenciar da referência laranja do concorrente; evitar roxo/indigo genérico de IA.

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-brand` | `#0F6B5C` | Primária: CTAs, header, foco |
| `--color-brand-strong` | `#0A4F44` | Hover / header escuro |
| `--color-accent` | `#E8A317` | Badges, destaques |
| `--color-danger` | `#C62828` | Erros, urgências |
| `--color-success` | `#2E7D32` | Confirmações |
| `--color-surface` | `#F4F6F5` | Fundo do app |
| `--color-card` | `#FFFFFF` | Cards / tiles |
| `--color-ink` | `#1A1F1E` | Texto |
| `--color-ink-muted` | `#5C6763` | Texto secundário |
| `--color-drawer` | `#1E2A28` | Menu lateral |

Alternativa: brand laranja `#E85D04` (mais próximo da referência). Decidir em **D1**.

### Tipografia

- Landing: fonte expressiva (ex. Fraunces / Literata)
- App: Source Sans 3 ou IBM Plex Sans (legível para faixa etária ampla)
- Evitar Inter/Roboto/Arial como identidade de marca

### Estilo UI

- Home em **grade de atalhos** (referência UX), não dashboard de métricas no primeiro viewport do morador
- Drawer por categorias (Principal / Acesso / Serviços / Comúnicação / Cadastros)
- Tema claro padrão; dark mode adiado
- Ícones unificados (Material Symbols ou Lucide) na cor brand
- Motion discreto: rota, feedback de botão, prompt PWA
- Touch target mínimo 44px; acessibilidade WCAG AA como meta

### Componentes (T8)

PrimeNG (calendário/reservas/tabelas) **ou** Angular Material + Tailwind na landing (ADR-003). Fechar no spike (**D2**).

---

## 2. Hospedagem VPS (T2 parcial)

Decidido: VPS + Docker. Falta fechar:

| Tema | Provisao / pergunta |
|------|---------------------|
| Provedor | Hetzner / DO / Contabo / BR — **H1** |
| Spec inicial | 4 vCPU, 8 GB RAM, SSD 160 GB+ |
| SO | Ubuntu 24.04 LTS |
| TLS | Caddy (auto) ou Nginx+certbot — **H2** |
| Backup | pg_dump diario + offsite (R2/S3), 30 dias — obrigatório na Fase 1 |
| Monitoramento | Healthcheck externo + logs rotativos |
| Staging | Segundo ambiente — **H3** |
| Intelbras | VPN/WireGuard/agent — depende **I2** |

---

## 3. Produto / funcionalidades frouxas

| Gap | Acao |
|-----|------|
| F1 / F2 | Confirmar Fase 1 e assembleia |
| F7 | Mensagem 1:1 sem chat? |
| F8 | Sociais: provisão Fase 3 (pets/mudança/achados) + Fase 7 (classificados/galeria/…) |
| F9 | Confirmar Fases 7–9 no roadmap (provisão: sim) |
| F10 | Acionamentos já na Fase 2 ou após Intelbras estável? |
| F11 | Câmeras ao vivo na Fase 8 ou fora? |
| P5 | ~~White-label ou marca única?~~ → **resolvida:** personalização parcial por condomínio (Fase 4) |
| P6 | Onboarding: convite e-mail/SMS, codigo unidade, aprovação? |
| P7 | Inquilino vs proprietario: permissões diferentes? |
| N1 | Push+e-mail na Fase 1; SMS depois? |
| I5 | Portaria/Intelbras se a VPS cair? |

---

## 4. Engenharia a detalhar

- Django vs FastAPI (esqueleto por **domínios** — T10; persistência ADR-005)
- CI (lint, test, build, deploy SSH)
- Ambientes: SQLite local → Postgres staging/prod
- Seed demo para vendas
- Testes de isolamento multi-tenant + e2e
- Segurança em escada ([13](13-seguranca-plataforma-logs-e-ddos.md), [14](14-revisao-plano-consolidada.md))
- `/healthz` + observabilidade mínima

---

## 5. Marketing / marca

- Nome do produto (**T4**)
- Domínio (**M1**), trial vs demo (**M2**)
- Revisão jurídica das políticas antes do go-live
- **Fase 6 — lojas** Apple + Play ([12](12-publicacao-lojas-apple-play.md)); perguntas **S1–S4**
- **M5 redes** (GTM paralelo); perguntas **M5–M6**
- Persistência: SQLite→Postgres ([ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md))

---

## 6. Ordem sugerida antes do codigo

1. **D1** paleta + **T4** nome
2. **D2/T8** PrimeNG vs Material
3. Django vs FastAPI
4. **H1-H3** VPS + backup + staging
5. **I1-I2** Intelbras (paralelo; não bloqueia V1)
6. **F7/F8/P5-P7** escopo fino
7. Contas Apple/Google (S3) podem ser abertas cedo; submit na Fase 6

---

## 7. Varredura de mercado 2026 → gaps absorvidos

Pesquisa em sites/comparativos: **Winker**, **Superlógica**, **TownSq**, **uCondo**, **Condomob**, **wCond**, **MyCond**, **Seu Condomínio**, **Wecondo** (+ checklists de mercado). Cruzamento com [09](09-inventario-referencia-e-versoes.md) e catálogo [06](06-produto-completo-modulos.md). Itens entraram no [roadmap](03-roadmap-e-entregas.md).

### Já cobríamos bem (não é gap)

Acesso facial / Intelbras (diferencial vs vários), visitantes+QR, reservas, comunicados, ocorrências, encomendas, assembleias, enquetes, pets/veículos, mudança, achados e perdidos, manutenção/OS, multi-tenant SaaS, LGPD, PWA→lojas.

### Gap → roadmap (priorizado)

| Gap de mercado | Onde entrou | Prioridade |
|----------------|-------------|------------|
| Lista de convidados da reserva na portaria | **2.12** | Alta (F2) |
| Vistoria pré/pós área comum | **2.13** | Alta (F2) |
| PIN/assinatura retirada encomenda + lembrete | **2.14** | Alta (F2) |
| Troca de turno / passagem de serviço | **2.15** | Média (F2) |
| Controle de chaves e objetos | **2.16** | Média (F2) |
| Procedimentos / checklists emergência portaria | **2.17** | Média (F2) |
| Telefones úteis | **2.18** | Baixa (F2) |
| Advertências digitais (sem depender de boleto) | **3.6** | Alta (F3) |
| Manutenção preventiva periódica | **3.7** | Alta (F3) |
| Contratos/orçamentos fornecedores | **3.8** | Média (F3) |
| Assinatura eletrônica ata/termos | **3.9** | Média (F3) |
| Calendário de eventos | **3.10** | Baixa (F3) |
| Assembleia: fração ideal + Lei 14.309/22 | **3.1** (aprofundamento) | Alta |
| Smart locker | **4.7** | Média (F4) |
| WhatsApp como canal (notificação + fluxos) | **4.8** | Alta tendência |
| Bloqueio inadimplente em reservas | **4.9** | Pós-P3 |
| Régua de cobrança / acordos | **5.6** | Pós financeiro |
| Assistente conversacional (app/WhatsApp) | **9.5** | Diferencial F9 |
| IA rascunho ata/comunicado | **9.6** | Opcional F9 |

### Explicitamente fora (não copiar Superlógica/wCond ERP)

Conta digital Bacen, folha/DP, mídia indoor, chat 1:1 livre — ver tabela “Fora de escopo” no roadmap.

### Perguntas novas (abrir em 05 se necessário)

| ID | Tema |
|----|------|
| **N2** | WhatsApp Business API cedo (F4) ou só após push estável? |
| **F12** | Advertências na F3 sem multa financeira — OK? (provisão: sim) → ver **F13** em [05](05-perguntas-abertas.md) |
| **F13** | Smart locker: quais provedores piloto? → **F14** |
| **F14** | Assinatura: ClickSign / Autentique / outro? → **F15** |

---

## Status

| Campo | Valor |
|-------|-------|
| Status | vivo |
| Última revisão | 2026-09-29 — §7 varredura mercado → roadmap |
