# Paleta de cores

Fonte da verdade visual do produto (tokens). Landing e app devem usar as **mesmas variáveis**; implementação futura em `packages/ui-brand`.

**Status:** provisão — confirmar em **D1** ([05-perguntas-abertas.md](../plano/05-perguntas-abertas.md)).
**Última revisão:** 2026-09-29

---

## Opção A — Brand verde-azulado (recomendada)

Diferencia do concorrente laranja; tom sério e condominial; evita roxo/indigo genérico.

| Token CSS | Hex | RGB | Uso |
|-----------|-----|-----|-----|
| `--color-brand` | `#0F6B5C` | 15, 107, 92 | Primária: CTAs, links, foco, ícones ativos |
| `--color-brand-strong` | `#0A4F44` | 10, 79, 68 | Hover / header escuro / drawer ativo |
| `--color-brand-soft` | `#D8EFEA` | 216, 239, 234 | Fundos suaves de icone, chips |
| `--color-accent` | `#E8A317` | 232, 163, 23 | Badge Novo, destaque, aviso amigável |
| `--color-accent-soft` | `#FFF4D6` | 255, 244, 214 | Fundo de badge / alerta leve |

### Neutros

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-surface` | `#F4F6F5` | Fundo da tela |
| `--color-card` | `#FFFFFF` | Cards, tiles, sheets |
| `--color-border` | `#D5DCD9` | Bordas, divisores |
| `--color-ink` | `#1A1F1E` | Texto principal |
| `--color-ink-muted` | `#5C6763` | Texto secundário / labels |
| `--color-drawer` | `#1E2A28` | Menu lateral escuro |
| `--color-drawer-ink` | `#F0F4F3` | Texto no drawer |

### Semanticos

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-success` | `#2E7D32` | Sucesso, confirmação |
| `--color-warning` | `#ED6C02` | Atenção |
| `--color-danger` | `#C62828` | Erro, urgente, exclusão |
| `--color-info` | `#0277BD` | Informativo |

### Amostra (referência visual)

```
Brand     [======= #0F6B5C =======]
Strong    [======= #0A4F44 =======]
Soft      [======= #D8EFEA =======]
Accent    [======= #E8A317 =======]
Surface   [======= #F4F6F5 =======]
Ink       [======= #1A1F1E =======]
Danger    [======= #C62828 =======]
```

---

## Opção B — Brand laranja (proximo a referência UX)

Se preferir proximidade com o app concorrente.

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-brand` | `#E85D04` | Primária |
| `--color-brand-strong` | `#C44D00` | Hover / header |
| `--color-brand-soft` | `#FFE8D6` | Fundos de icone |
| `--color-accent` | `#0F6B5C` | Contraste (verde como secundário) |

Neutros e semânticos: **iguais a Opção A** (exceto drawer pode usar `#2B211C` se quiser harmonia com laranja).

---

## CSS variables (snippet)

Copiar para `packages/ui-brand/tokens.css` quando o monorepo existir:

```css
:root {
  /* Opção A (padrão provisão) */
  --color-brand: #0F6B5C;
  --color-brand-strong: #0A4F44;
  --color-brand-soft: #D8EFEA;
  --color-accent: #E8A317;
  --color-accent-soft: #FFF4D6;
  --color-surface: #F4F6F5;
  --color-card: #FFFFFF;
  --color-border: #D5DCD9;
  --color-ink: #1A1F1E;
  --color-ink-muted: #5C6763;
  --color-drawer: #1E2A28;
  --color-drawer-ink: #F0F4F3;
  --color-success: #2E7D32;
  --color-warning: #ED6C02;
  --color-danger: #C62828;
  --color-info: #0277BD;
  --radius-card: 12px;
  --radius-tile: 16px;
  --shadow-card: 0 1px 3px rgb(26 31 30 / 8%);
}
```

---

## Regras de uso

1. Não usar cores soltas no código — so tokens.
2. Contraste texto/fundo: meta **WCAG AA** (4.5:1 corpo; 3:1 texto grande).
3. Landing e app compartilham brand; landing pode usar gradiente `brand` -> `brand-strong`.
4. White-label futuro (P5): sobrescrever `--color-brand*` por condomínio sem quebrar semânticos.
5. Dark mode: adiado; quando existir, mapear tokens em `[data-theme=dark]`.

---

## Arquivos relacionados

| Arquivo | Papel |
|---------|-------|
| [tipografia.md](tipografia.md) | Fontes |
| [../plano/11-lacunas-e-complementos.md](../plano/11-lacunas-e-complementos.md) | Contexto das lacunas |
| [../decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md](../decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md) | UI kit |
| Pergunta **D1** em `05-perguntas-abertas.md` | Escolha A vs B |

---

## Histórico

| Data | Mudança |
|------|---------|
| 2026-09-29 | Criação; Opção A verde + Opção B laranja |
