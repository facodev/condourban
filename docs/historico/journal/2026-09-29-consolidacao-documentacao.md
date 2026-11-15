# Journal — 2026-09-29 — Consolidação da documentação

## Objetivo

Deixar docs, planos e arquivos **numa estrutura única e navegável**, sem pastas duplicadas na raiz.

## O que foi feito

1. Arquivado `gestao-condominio-documentacao/` (desatualizado / Keycloak) em `docs/historico/arquivo/`.
2. Movidas folhas de nomes `v1–v3` para `docs/design/sugestoes/nomes-marca/`.
3. Corrigidos links quebrados (`design/logos` → `design/sugestoes/logos`; hub HTML; scripts).
4. Reescritos `README.md` (raiz), `docs/README.md`, `docs/plano/INDICE.md` com mapa por área.
5. Restaurado preview local como `scripts/start-local.bat`.

## Decisões

- Uma fonte da verdade: **`docs/`**.
- Histórico substituído fica em `docs/historico/arquivo/` (não editar).
- Planos 00–17 permanecem flat em `plano/` (evita quebrar dezenas de links); o INDICE agrupa por seção.

## Referências

- [INDICE](../../plano/INDICE.md)
- [arquivo/README](../arquivo/README.md)
- [CHANGELOG](../CHANGELOG.md)
