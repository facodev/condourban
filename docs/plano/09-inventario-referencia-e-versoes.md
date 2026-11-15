# Inventário de funcionalidades (referência visual) × versões

Análise das telas de referência enviadas (app tipo "Condomínio Dedicado" / Jardim dos Buritis) cruzadas com o nosso catálogo e decisões (P3, F3–F6, F4, fases 7–9, etc.).

**Prints salvos em:** [`../referencia/app-concorrente/`](../referencia/app-concorrente/)

---

## 1. Inventário completo da referência

### Shell / plataforma (visível nas telas)

| Funcionalidade | Onde aparece |
|----------------|--------------|
| Nome do condomínio no header | Home |
| Menu hambúrguer + drawer | Home / menus |
| Notificações (sino) | Home |
| Perfil (nome + unidade, ex. 35F) | Drawer |
| **Trocar de Condomínio** | Drawer |
| Configurações | Home + Cadastros |
| Sair | Drawer |
| Nav inferior (atalhos: home / pet / config) | Home |

### Módulos da home e menus

| # | Funcionalidade (como no app de referência) | Grupo no menu |
|---|--------------------------------------------|---------------|
| 1 | Reservas | Principal |
| 2 | Correspondências | Principal |
| 3 | Livro de ocorrências | Principal |
| 4 | Autorizações | Principal |
| 5 | Assembleia Virtual | Principal |
| 6 | Acessos de Visitantes | Acesso |
| 7 | Log's de Acesso | Acesso |
| 8 | Manutenção | Serviços |
| 9 | Mudança | Serviços |
| 10 | Achados e Perdidos | Serviços |
| 11 | Mensagem | Comunicação |
| 12 | Comunicados | Comunicação |
| 13 | Notificações e multas | Comunicação |
| 14 | Portal da Transparência | Comunicação / home |
| 15 | Enquetes | Participação |
| 16 | Moradores | Comunidade |
| 17 | Vizinho Amigo | Comunidade |
| 18 | Classificados | Comunidade |
| 19 | Clube de Vantagens | Comunidade |
| 20 | Galeria | Comunidade |
| 21 | Automóveis | Cadastros |
| 22 | Prestadores de Serviço | Cadastros / home |
| 23 | Animais de Estimação | Cadastros / home / nav |
| 24 | Configurações | Cadastros |

---

## 2. Cobertura vs nosso plano

Legenda: **OK** = no catálogo / decisão | **PARCIAL** = existe conceito, falta detalhe | **FALTAVA** = não estava explícito (agora incluído) | **FORA** = decisão consciente de não fazer (ainda) | **DIVERGE** = referência tem, nós decidimos diferente

| # | Funcionalidade referência | Status no nosso produto | Observação |
|---|---------------------------|-------------------------|------------|
| — | Trocar condomínio / multi-tenant | **OK** | P1 |
| — | LGPD, exportação/exclusão | **OK** | C1 Fase 1 |
| — | Dependentes/menores | **OK** | C2 |
| — | Landing + políticas + FAQ | **OK** | Doc 07 (não está no app de referência) |
| — | Pré-cadastro facial + Intelbras | **OK** | F5/F6 — **além** da referência |
| 1 | Reservas | **OK** | F3, obrigatório Fase 2 |
| 2 | Correspondências | **OK** | Doc 06 Fase 2 |
| 3 | Livro de ocorrências | **OK** | Fase 1 |
| 4 | Autorizações | **PARCIAL→OK** | Mapeado para pré-autorização + facial (doc 08) |
| 5 | Assembleia Virtual | **OK** | Fase 3 (F2 ainda aberta se antecipar) |
| 6 | Acessos de Visitantes | **OK** | Fase 2 + facial |
| 7 | Log's de Acesso | **OK** | `AccessLog` + Intelbras |
| 8 | Manutenção | **OK** | Fase 3 (OS/prestadores) |
| 9 | Mudança | **FALTAVA** | Incluído no catálogo (bloco V3) |
| 10 | Achados e Perdidos | **FALTAVA** | Incluído (bloco V4 comunitário) |
| 11 | Mensagem | **DIVERGE** | Referência tem chat/msg; **F4 = só comunicados** (sem chat). Confirmar se "Mensagem" = comunicado individual ou chat |
| 12 | Comunicados | **OK** | Fase 1; F4 |
| 13 | Notificações e multas | **PARCIAL** | Notificações push OK; **multas** ligadas a financeiro — pós-P3 / V4+ |
| 14 | Portal da Transparência | **PARCIAL** | Docs públicos na Fase 1; extratos financeiros só quando financeiro in-app (P3) |
| 15 | Enquetes | **OK** | Fase 2 |
| 16 | Moradores | **OK** | Diretório / cadastro (Fase 1–2) |
| 17 | Vizinho Amigo | **FALTAVA** | Social; bloco V4 (confirmar se quer) |
| 18 | Classificados | **FALTAVA** | Bloco V4 |
| 19 | Clube de Vantagens | **FALTAVA** | Bloco V5 / parceiros |
| 20 | Galeria | **FALTAVA** | Bloco V4 |
| 21 | Automóveis | **OK** | Doc 06 (cadastro veículos) |
| 22 | Prestadores de Serviço | **OK** | Manutenção Fase 3 + cadastro |
| 23 | Animais de Estimação | **FALTAVA** | Cadastro; bloco V2/V3 |
| 24 | Configurações | **OK** | Perfil + preferências Fase 1 |
| — | Boletos / pagamentos in-app | **FORA (Fase 1+)** | P3 — contabilidade externa |

**Conclusão:** a referência é um bom mapa de UX. Já cobríamos o núcleo operacional (ocorrências, comunicados, reservas, acesso, assembleia, manutenção). Faltavam módulos **comunitários/sociais** (classificados, galeria, vizinho amigo, pets, mudança, achados e perdidos, clube). Nosso diferencial: **Intelbras facial** + **landing SaaS** + **sem financeiro in-app no início**.

---

## 3. Blocos de versão (releases)

Cada bloco = versão publicável. Numeração **V1–V9** alinhada às Fases 1?5 do roadmap, com granularidade da referência.

### V1 — Fundação + convivência (Fase 1)

| Funcionalidade | Prioridade |
|----------------|------------|
| Auth, multi-condomínio, trocar condomínio, papéis | P0 |
| Shell app (home grid, drawer, notificações, config, sair) | P0 |
| Unidades, moradores (cadastro básico), dependentes | P0 |
| Comunicados + confirmação de leitura | P0 |
| Documentos / biblioteca (base do Portal Transparência sem financeiro) | P0 |
| Livro de ocorrências | P0 |
| Perfil + preferências de notificação | P0 |
| LGPD (políticas, exportação, exclusão) | P0 |
| PWA (install, push, offline leitura) | P0 |
| Landing M0 (home, contato, políticas, FAQ) | P0 |

**Não entra em V1:** reservas, portaria/facial, financeiro, assembleia, chat.

---

### V2 — Operação do prédio (Fase 2)

| Funcionalidade | Prioridade |
|----------------|------------|
| **Reservas** (áreas comuns) | P0 |
| Correspondências | P0 |
| Autorizações + **Acessos de Visitantes** (pré-cadastro) | P0 |
| Pré-cadastro facial + liberação | P0 |
| Integração **Intelbras** + **Log's de Acesso** | P0 |
| Portal portaria (mesmo app, perfil) | P0 |
| Enquetes | P1 |
| Automóveis (cadastro) | P1 |
| Animais de estimação (cadastro) | P1 |
| Diretório Moradores (visão comunidade) | P1 |

---

### V3 — Governança e serviços (Fase 3)

| Funcionalidade | Prioridade |
|----------------|------------|
| **Assembleia Virtual** (convocação, votação, ata) | P0 |
| Manutenção / OS | P0 |
| Prestadores de serviço | P0 |
| **Mudança** (agendamento entrada/saída) | P1 |
| Portal da Transparência (docs + o que a administradora publicar; sem cobrança in-app) | P1 |

---

### V4 — Comunidade e comunicação expandida

| Funcionalidade | Prioridade |
|----------------|------------|
| Classificados | P1 |
| Galeria | P1 |
| Achados e perdidos | P1 |
| Vizinho Amigo | P2 (confirmar F7) |
| Notificações e **multas** (multas só se houver regra + dados; tipicamente com financeiro) | P2 |
| Mensagem / chat | **Não** — salvo revisão de F4 (ver F7) |

---

### V5 — Escala, parceiros e financeiro in-app (Fases 4–5)

| Funcionalidade | Prioridade |
|----------------|------------|
| Clube de Vantagens | P2 |
| Financeiro in-app / conciliação / gateway (quando sair da contabilidade pura) | P0 quando P3 evoluir |
| Painel administradora SaaS + billing do software | P0 |
| **Personalização por condomínio** (logo, cores, regras, flags) — P5 | P0 |
| MFA, BI | P1 |
| Outros providers de acesso além Intelbras | P2 |

### V6 — Lojas (Fase 6)

| Funcionalidade | Prioridade |
|----------------|------------|
| App iOS (App Store) via Capacitor | P0 |
| App Android (Google Play) via Capacitor | P0 |
| Push nativo FCM/APNs | P0 |
| Materiais e review das lojas | P0 |

---


### V7 — Comunidade (Fase 7)

| Funcionalidade | Prioridade |
|----------------|------------|
| Classificados | P1 |
| Galeria | P1 |
| Vizinho Amigo | P2 |
| Clube de Vantagens | P2 |

### V8 — IoT / automação (Fase 8)

| Funcionalidade | Prioridade |
|----------------|------------|
| Cenas e multi-dispositivo | P0 |
| Consumo água/energia | P2 |
| Câmeras | P2 |

### V9 — Inteligência (Fase 9)

| Funcionalidade | Prioridade |
|----------------|------------|
| Busca inteligente / OCR / alertas | P1 |

### V10 — Redes / GTM (M5)

| Entrega | Prioridade |
|---------|------------|
| Perfis oficiais da marca + links na landing | P0 (GTM, paralelo à F1+) |
| Calendário editorial e diretrizes | P1 |
| Pixels/embeds (se houver) com política | P1 |


## 4. Home sugerida (espelhando a referência)

Organização de atalhos por versão (o que o morador vê cresce com o release):

**V1 home:** Ocorrências · Comunicados · Documentos/Transparência (docs) · Configurações · Moradores (básico)

**V2 home (+):** Reservas · Correspondências · Autorizações · Acessos · Enquetes · Automóveis · Pets

**V3 home (+):** Assembleia · Manutenção · Mudança · Prestadores

**V4 home (+):** Classificados · Galeria · Achados e perdidos · (Vizinho Amigo)

Drawer agrupado como na referência: Principal · Acesso · Serviços · Comunicação · Participação · Comunidade · Cadastros.

---

## 5. Perguntas abertas geradas por esta análise

Registradas em [05-perguntas-abertas.md](05-perguntas-abertas.md):

- **F7** — "Mensagem" da referência: descartar (F4) ou permitir mensagens 1:1 sem chat em tempo real?
- **F8** — Incluir Vizinho Amigo, Classificados, Galeria, Clube, Achados e Perdidos, Pets, Mudança conforme blocos V2–V5?
- **F1** — Ajustes Fase 1 após este inventário?

---



---

## 6. Concorrente 2 — Simple Services (prints anonimizados)

Pasta: [../referencia/app-concorrente-2-simple/](../referencia/app-concorrente-2-simple/)

### Funcionalidades vistas

| Funcionalidade | No nosso plano? | Nota |
|----------------|-----------------|------|
| Cadastro | OK / parcial | Cadastro pessoas/unidade; aprofundar UX |
| Histórico de Acessos | OK | AccessLog + Intelbras (Fase 2) |
| Agendamentos | OK | Mapeia para **Reservas** (F3) |
| Mural de avisos | OK | Comunicados |
| Entregas | OK | Correspondências Fase 2 |
| Boletos | FORA Fase 1+ | P3 — contabilidade externa |
| Documentos | OK | Biblioteca Fase 1 |
| Ocorrências | OK | Fase 1 |
| **Acionamentos** (remoto/controle) | FALTAVA | Incluir no catálogo acesso — Fase 2/4 |
| **Convites** (destaque) | PARCIAL | Coberto por pré-cadastro/autorizações; UX de convite a detalhar |
| Notificações (feed acessos) | OK / parcial | Push + centro de notificacoes |
| Perfil + papel (Morador responsável) | OK | Memberships/roles |
| Fale Conosco | PARCIAL | Suporte/landing; canal in-app a definir |
| Configurações / Sair | OK | |
| Nav inferior Home / Notificações / Perfil | UX | Adotar padrão similar no web-app |

### Conclusão

Cobertura boa no nucleo. Gaps relevantes deste concorrente: **Acionamentos** (abrir portão/dispositivo pelo app) e UX forte de **Convites** + feed de acessos nas notificacoes. Boletos alinhados a P3 (fora por enquanto).


## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-09-29 — + §7 mercado BR 2026 |
| Fonte | Screenshots WhatsApp 2026-09-29 (app referência) + varredura sites |

---

## 7. Varredura de mercado BR 2026 (sites)

Além das referências visuais (§1 e §6), pesquisa pública em: Winker, Superlógica, TownSq, uCondo, Condomob, wCond, MyCond, Seu Condomínio, Wecondo.

| Tendência / feature | Nosso plano |
|---------------------|-------------|
| WhatsApp + IA conversacional | Canal **4.8**; assistente **9.5–9.6** (não ERP Bacen) |
| Advertências digitais | **3.6** |
| Chaves / objetos / troca de turno / procedimentos | **2.15–2.17** |
| Vistoria reserva + lista convidados | **2.12–2.13** |
| Smart locker | **4.7** |
| Assinatura eletrônica / manutenção preventiva | **3.7–3.9** |
| Conta digital / folha / DP | **Fora** (roadmap) |
| Facial / acesso físico | Nosso diferencial (Intelbras F2) vs vários ERPs fracos nisso |

Detalhe e priorização: [11](11-lacunas-e-complementos.md) §7 · [03](03-roadmap-e-entregas.md).
