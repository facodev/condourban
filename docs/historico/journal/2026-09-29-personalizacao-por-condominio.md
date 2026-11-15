# Journal — personalização por condomínio (P5)

**Data:** 2026-09-29  
**Foco:** Decidir e colocar no roadmap a personalização multi-tenant por condomínio.

## Decisão

- **P5 resolvida:** cada condomínio personaliza **algumas partes** (logo, cores, nome de exibição, regras/horários, feature flags).
- Marca da plataforma permanece; **não** white-label total (sem app/build por tenant).
- Entrega na **Fase 4** (itens 4.3–4.3d); `condominio.configuracoes` JSONB já no DDL.

## Entregas de doc

- `05-perguntas-abertas.md` — P5
- `03-roadmap-e-entregas.md` — checklist 4.3a–d
- `funcionalidades/personalizacao-por-condominio.md`
- Alinhamento: 01, 04, 06, 09, 11, 14, CHANGELOG
