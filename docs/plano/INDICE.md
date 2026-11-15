# Índice dos planos

Ponto de entrada da pasta `docs/plano/`. Status do dia: **[04-status-e-proximos-passos.md](04-status-e-proximos-passos.md)**.

## Entrada e estado

| # | Arquivo | Descrição |
|---|---------|-----------|
| 0 | [00-visao-geral.md](00-visao-geral.md) | Produto completo, princípios, 9 Bounded Contexts, portais |
| 4 | [04-status-e-proximos-passos.md](04-status-e-proximos-passos.md) | **Estado atual** |
| 5 | [05-perguntas-abertas.md](05-perguntas-abertas.md) | Pendências stakeholder (histórico Q&A) |
| 18 | [18-decisoes-a-tomar.md](18-decisoes-a-tomar.md) | **Checklist** de decisões (nome, logo, hospedagem, modelo de negócios…) |
| 14 | [14-revisao-plano-consolidada.md](14-revisao-plano-consolidada.md) | Revisão: fases, 9 Bounded Contexts, infra em escada |

## Produto e roadmap

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | [01-boas-praticas-e-funcionalidades.md](01-boas-praticas-e-funcionalidades.md) | Práticas transversais, engenharia e fases |
| 3 | [03-roadmap-e-entregas.md](03-roadmap-e-entregas.md) | Releases Fase 1–9 tagueadas por Bounded Context + GTM/M5 |
| 6 | [06-produto-completo-modulos.md](06-produto-completo-modulos.md) | Catálogo completo por 9 Bounded Contexts + matriz de 5 pilares |
| 8 | [08-intelbras-facial-e-reservas.md](08-intelbras-facial-e-reservas.md) | Adaptador Intelbras facial (`controle_acesso`) e reservas (`reservas`) |
| 9 | [09-inventario-referencia-e-versoes.md](09-inventario-referencia-e-versoes.md) | App concorrente × versões |
| 11 | [11-lacunas-e-complementos.md](11-lacunas-e-complementos.md) | Design, hosting, gaps e prioridades |

## Técnico

| # | Arquivo | Descrição |
|---|---------|-----------|
| 2 | [02-arquitetura-tecnica.md](02-arquitetura-tecnica.md) | FastAPI + Angular, 9 Bounded Contexts, dados, segurança |
| 13 | [13-seguranca-plataforma-logs-e-ddos.md](13-seguranca-plataforma-logs-e-ddos.md) | Auditoria, uso, buckets, anti-DDoS |
| 15 | [15-modelo-dados-postgresql.md](15-modelo-dados-postgresql.md) | Modelo de dados PostgreSQL por Bounded Context + glossário pt-BR |
| 16 | [16-api-v1-referencia.md](16-api-v1-referencia.md) | Rotas `/api/v1` por Bounded Context |

Schema SQL: [docs/sql/](../sql/README.md) (DDL 001–014).

## Documentação por bounded context e funcionalidades

Navegação canônica por domínio de código, arquitetura e especificações:

- **Especificações funcionais e documentos de domínio:** [../funcionalidades/README.md](../funcionalidades/README.md)
- **Mapa de rastreabilidade:** [../funcionalidades/MAPA.md](../funcionalidades/MAPA.md)
- **Estrutura de diretórios e ADR-013:** [../decisoes/Estrutura.md](../decisoes/Estrutura.md)

## Go-to-market e negócio

| # | Arquivo | Descrição |
|---|---------|-----------|
| 7 | [07-landing-page-marketing-e-conteudo-comum.md](07-landing-page-marketing-e-conteudo-comum.md) | Landing, políticas, FAQ |
| 10 | [10-seguranca-faq-politicas-ritual.md](10-seguranca-faq-politicas-ritual.md) | Ritual permanente segurança/FAQ/políticas |
| 12 | [12-publicacao-lojas-apple-play.md](12-publicacao-lojas-apple-play.md) | Fase 6 — App Store e Google Play |
| 17 | [17-modelos-de-negocio-e-precificacao.md](17-modelos-de-negocio-e-precificacao.md) | Modelos de negócio e precificação |

> Fechar o híbrido comercial: item **2.1** em [18-decisoes-a-tomar.md](18-decisoes-a-tomar.md).

## Design

- **[Landing page (preview)](../../landing/index.html)** — home de marketing CondoUrban
- [Paleta de cores](../design/paleta-cores.md) — tokens + CSS
- [Amostra visual](../design/paleta-amostra.html)
- [Tipografia](../design/tipografia.md)
- **[Sugestões](../design/sugestoes/README.md)** — logos, telas, temas, [nomes de marca](../design/sugestoes/nomes-marca/README.md)

## Referência e conteúdo

- [App concorrente (prints)](../referencia/app-concorrente/README.md)
- [FAQ / políticas](../conteudo/README.md)
- [CHANGELOG](../historico/CHANGELOG.md)
- [ADRs](../decisoes/README.md)
- [Arquivo histórico](../historico/arquivo/README.md) — pacotes substituídos

## Última atualização

- **Data:** 2026-10-17
- **Nota:** Alinhamento completo aos 9 Bounded Contexts (ADR-013) e 26 specs em `docs/funcionalidades/`.
