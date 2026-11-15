# Visão geral

## Objetivo

Construir uma **plataforma completa de gestão de condomínios** (moradores, síndico, portaria, administradora), entregue **por fases**, com **Web + PWA** e arquitetura preparada para integrações financeiras, governança e escala multi-condomínio. O sistema terá RAG e os usuários poderão interagir com o sistema por meio de chat.

## Formato

| Aspecto | Decisão provisória |
|---------|-------------------|
| Plataforma | Web responsiva + PWA; **Fase 6**: apps nas lojas Apple e Google Play (Capacitor) |
| Portais | Morador (mobile-first), portaria, síndico/conselho, administradora |
| Site público | Landing de vendas + políticas/FAQ compartilhados com o app ([07](07-landing-page-marketing-e-conteudo-comum.md)) |
| Idioma | PT-BR |
| Tenancy | Multi-condomínio / administradora desde o desenho |
| Arquitetura | **Por 9 Bounded Contexts** ([ADR-013](../decisoes/ADR-013-organizacao-diretorios.md)); persistência SQLite→Postgres ([ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md)) |
| Segurança | Auditoria, uso, buckets, anti-DDoS em escada — [13](13-seguranca-plataforma-logs-e-ddos.md) |
| Entrega | **Fases 1–9** + GTM/redes **M5**; revisão [14](14-revisao-plano-consolidada.md) |

## Princípios de produto

1. **Produto completo, entrega incremental** — arquitetura e dados pensados para o catálogo final; fases ligam módulos, não descartam fundação.
2. **Mobile-first** no portal morador.
3. **Papéis e permissões** em todos os fluxos.
4. **LGPD, auditoria e segurança de borda** desde a Fase 1 ([13](13-seguranca-plataforma-logs-e-ddos.md)).
5. **API como contrato** entre front (Angular) e back (Python FastAPI).
6. **Estrutura por 9 Bounded Contexts** — backend (`backend/app/modulos/`) e features Angular (`frontend/src/app/features/`) organizados por bounded context conforme [ADR-013](../decisoes/ADR-013-organizacao-diretorios.md), não por monólito desordenado sem fronteiras ([02](02-arquitetura-tecnica.md)).

## Escopo do produto (referência)

Tudo em [06-produto-completo-modulos.md](06-produto-completo-modulos.md): estruturado nos **9 Bounded Contexts** (`identidade_cadastro`, `condominio`, `controle_acesso` ⭐, `portaria`, `reservas`, `comunicacao`, `governanca`, `financeiro`, `manutencao` + camada `transversal`) mapeados aos **5 pilares de negócio** (cadastro, controle de acesso ⭐, condomínio, experiência do morador, administração) — com **datas de entrega por fase**, não "talvez nunca".

## Fora de escopo inicial (Fase 1 apenas)

- Gateway bancário automático (previsto Fase 4)
- Publicação nas lojas Apple/Play (previsto **Fase 6** — [12](12-publicacao-lojas-apple-play.md)); até lá: Web + PWA
- Hardware específico de interfonia (adaptadores na Fase 4)
- Comunidade / IoT / inteligência (Fases **7–9**); redes da marca = **M5** (paralelo) — [14](14-revisao-plano-consolidada.md)

## Referências internas

- Catálogo e fases: [06-produto-completo-modulos.md](06-produto-completo-modulos.md)
- Funcionalidades e práticas: [01-boas-praticas-e-funcionalidades.md](01-boas-praticas-e-funcionalidades.md)
- Arquitetura: [02-arquitetura-tecnica.md](02-arquitetura-tecnica.md)
- Roadmap: [03-roadmap-e-entregas.md](03-roadmap-e-entregas.md)
- Stack definitiva Python FastAPI + Angular: [ADR-001](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md)
- Organização de Bounded Contexts: [ADR-013](../decisoes/ADR-013-organizacao-diretorios.md) e [Estrutura.md](../decisoes/Estrutura.md)

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-10-17 — alinhamento aos 9 Bounded Contexts |
