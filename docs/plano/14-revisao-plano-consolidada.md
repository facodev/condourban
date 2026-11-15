# Revisão consolidada do plano (2026-09-29)

Revisão de **tudo documentado** até aqui: melhorias, agrupamentos e mudanças de fase. Fonte viva; detalhes operam nos docs 02/03/06.

## 1. O que estava disperso / pesado demais

| Problema | Ajuste |
|----------|--------|
| Fase 1 com Postgres + Redis + Celery + CDN/WAF + Usage + Audit todos “dia 1” | **Escada de infra**: leve no spike/dev; endurecer no 1º deploy público |
| Fase 2 sobrecarregada (facial + Intelbras + reservas + acionamentos + …) | **Acionamentos piloto → Fase 4** (após Intelbras estável — F10) |
| “Fase 3 — Governança e financeiro” com P3 sem financeiro in-app | Renomear para **Governança e operações**; financeiro só quando sair de P3 |
| Fase 10 (redes) numerada depois de IoT/IA | Redes = **track Marketing / GTM** (M5), paralelo cedo — não “depois da inteligência” |
| Cadastros soltos (auto, pets, mudança, achados) | **Grupo Cadastros** (auto+pets na F2) e **Serviços do prédio** (mudança/achados na F3) |
| Fale Conosco na F3 | Antecipar para **M0 / Fase 1** (landing + in-app mínimo) |
| Docs 03 vs 06 vs 01 desalinhados em nomes | Esta revisão + sync |

## 2. Escada de infraestrutura (começar simples)

Ver [ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md).

```text
Spike/dev     → SQLite (arquivo) + rate-limit in-process + jobs síncronos/thread
Testes        → SQLite :memory:
1º staging    → PostgreSQL + Redis (rate limit / cache)
Produção      → Postgres + Redis + Celery + CDN/WAF + object storage
```

**Domínios, RBAC, AuditLog e OpenAPI** continuam desde o início — o que muda é *onde* os dados e filas moram.

## 3. Mapa de fases revisado (produto)

| Fase | Nome | Conteúdo (resumo) | Pode paralelizar com |
|------|------|-------------------|----------------------|
| **0** | Documentação | Planos, ADRs | — |
| **1** | Fundação + convivência | Domínios, auth/RBAC, AuditLog, comunicados, docs, ocorrências, PWA leve, Fale Conosco; persistência SQLite→Postgres | Marketing M0, **GTM redes (M5)** |
| **2** | Operação do prédio | Portaria, visitantes/QR/convites, facial+Intelbras, reservas, correspondências, enquetes, notificações, **cadastros auto+pets** | Contas loja (S3) |
| **3** | Governança e operações | Assembleias, manutenção/OS, mudança, achados e perdidos | — |
| **4** | Escala B2B + acesso maduro | Gateway pagamentos (pós-P3), SaaS administradora, **personalização por condomínio** (P5), **acionamentos**, multi-provider | — |
| **5** | Maturidade | MFA, BI/uso, PWA endurecido, limiares SIEM | — |
| **6** | Lojas | Capacitor App Store / Play | Após PWA estável (ideal pós-F2) |
| **7** | Comunidade | Classificados, galeria; Vizinho/Clube opcional | — |
| **8** | IoT avançado | Cenas, multi-dispositivo, consumo, câmeras opcional | — |
| **9** | Inteligência | Busca, OCR, alertas, moderação assistida | — |

**Marketing / GTM** (não é “fase 10 de produto”):

| Marco | Conteúdo |
|-------|----------|
| M0–M3 | Landing, políticas, FAQ, planos, cases |
| **M5 redes** | Perfis oficiais (Instagram, LinkedIn, …) — assim que T4/D1 existirem |

## 4. Agrupamentos de módulos (catálogo)

### 4.1 Pilares de produto (navegação / negócio)

Fonte canônica detalhada: [06](06-produto-completo-modulos.md) § Mapa de produto.

1. **Cadastro e identidade** — Pessoa, Morador, Visitante, Prestador, Documentos, Solicitação de cadastro  
2. **Controle de acesso** ⭐ — Credencial, Autorização, Dispositivo, Grupo de acesso, Eventos, Intelbras  
3. **Condomínio** — Blocos, Unidades, Vagas, Áreas comuns  
4. **Experiência do morador** — Encomendas, Reservas, Comunicados, Ocorrências, Enquetes, Assembleias  
5. **Administração** — Financeiro, Usuários, Permissões, Auditoria, Relatórios  

Expansão (fora dos 5): comunidade F7, IoT F8, inteligência F9, marketing M0–M5.

### 4.2 Domínios técnicos (9 Bounded Contexts em pt-BR)

Alinhados a [02](02-arquitetura-tecnica.md), formalizados no [ADR-013](../decisoes/ADR-013-organizacao-diretorios.md) e mapeados aos 5 pilares de negócio:

1. **`identidade_cadastro`** — Modelagem civil de pessoas, contas de acesso, membros, unidades residenciais, veículos e animais de estimação → Pilar 1  
2. **`condominio`** — Estrutura física (blocos, unidades, vagas), catálogo de áreas comuns, parametrização operacional e branding → Pilar 3  
3. **`controle_acesso`** ⭐ — Credenciais RFID/QR/LPR, biometria facial com adapter Intelbras, eventos periciais de passagem e acionamentos remotos → Pilar 2  
4. **`portaria`** — Terminal da guarita, atendimento de visitantes/prestadores, encomendas com foto/PIN, agendamento de mudanças e achados/perdidos → Pilares 2 e 4  
5. **`reservas`** — Agendamento de áreas comuns, regras anti-conflito, lista de convidados na portaria e vistorias pré/pós-uso → Pilares 3 e 4  
6. **`comunicacao`** — Mural oficial com leitura confirmada, livro de ocorrências, enquetes públicas, canal direto Fale Conosco e mural da comunidade → Pilar 4  
7. **`governanca`** — Assembleias digitais/híbridas (Lei 14.309/2022), votações por fração ideal, procurações, atas e repositório normativo → Pilar 4  
8. **`financeiro`** — Cobrança in-app (pós-P3 na Fase 4; contabilidade externa antes), boletos, Pix dinâmico, balancetes e conciliação → Pilar 5  
9. **`manutencao`** — Chamados corretivos, triagem, ordens de serviço (OS zelador), PMO preventivo (NBR 5674) e gestão de prestadores → Pilares 4 e 5  
10. **`transversal`** — RBAC unificado, auditoria imutável (`evento_auditoria`), catálogo SaaS (planos e entitlements), rate-limit Redis e anti-DDoS → Pilar 5 e Plataforma  

> **Higiene contínua (R1–R8):** trabalho permanente em todas as releases ([03](03-roadmap-e-entregas.md)); não é módulo de produto.

## 5. Decisões finas desta revisão

| ID | Decisão |
|----|---------|
| T12 | Persistência: memória/SQLite → PostgreSQL com RLS ([ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md), [ADR-006](../decisoes/ADR-006-isolamento-rls-postgresql.md)) |
| F10 | Acionamentos **não** na F2; piloto na **Fase 4** após Intelbras estável |
| F1 | Catálogo Fase 1 alinhado a esta revisão (parcial → ver 05) |
| Redes | Track **M5**, não depender das Fases 7–9 |

## 6. O que *não* muda

- Stack Python FastAPI + Angular 22+; PWA com visões por perfil ([ADR-001](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md))  
- Multi-condomínio com isolamento nativo; P3 sem financeiro in-app antecipado  
- Reservas obrigatórias na F2; facial + Intelbras na F2  
- Sem chat livre não moderado (F4); ritual segurança/FAQ/políticas (doc 10)  
- Estrutura estrita por **9 Bounded Contexts** ([ADR-013](../decisoes/ADR-013-organizacao-diretorios.md), [Estrutura.md](../decisoes/Estrutura.md))  

## Status

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-10-17 — alinhamento integral aos 9 Bounded Contexts (ADR-013) e 26 specs |
