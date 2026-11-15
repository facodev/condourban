# Sugestões de design (agrupado)

Tudo de **logos** e **sugestões de telas/UI** fica nesta pasta.

## Estrutura

```
sugestoes/
├── logos/            ← SVG + Stitch (galeria)
├── telas/            ← protótipos HTML + Stitch
├── temas/            ← DESIGN.md Harmony / Modern
├── nomes-marca/      ← folhas de nomes (v1/v2/v3)
├── assets/
├── paletas.md
├── layouts.md
├── icones.md
├── index.html
└── README.md
```

## Abrir no navegador

Na raiz do projeto:

```bat
scripts\start-local.bat
```

→ http://127.0.0.1:8016/ (hub na raiz) → sugestões em `/docs/design/sugestoes/`

Tunel público (Cloudflare):

```bat
scripts\start-cloudflare-tunnel.bat
```

Alternativa manual:

```bash
python -m http.server 8016 --bind 127.0.0.1
```

| Página | Conteúdo |
|--------|----------|
| [index.html](../../../../index.html) (raiz) | Hub geral do preview |
| [index.html](index.html) | Hub de sugestões (logos + telas) |
| [logos/index.html](logos/index.html) | Todas as logos (SVG + Stitch) |
| [telas/index.html](telas/index.html) | Todas as telas (HTML + Stitch) |
| [telas/html/index.html](telas/html/index.html) | Só protótipos HTML |
| [logos/amostra-svg.html](logos/amostra-svg.html) | Só logos SVG CondoUrban |
| [nomes-marca/](nomes-marca/README.md) | Folhas de nomes de produto (T4) |

## Logos

### SVG (`logos/svg/`) — preferidos

| Arquivo | Conceito |
|---------|----------|
| `mark-casa.svg` | **Casa** (prioridade) |
| `mark-predio.svg` | **Prédio** / condomínio |
| `mark-chave.svg` | **Chave** / acesso à unidade |
| `mark-casa-chave.svg` | Combo casa + chave |
| `app-icon-casa.svg` / `predio` / `chave` | Ícones de app |
| `wordmark-habitar-casa.svg` / `chave` | Nome + símbolo |

Portal (`mark-a-portal*`) permanece só como alternativa — menos alinhado ao feedback.

### Stitch (`logos/stitch/`)
| Pasta | Tema |
|-------|------|
| harmony-emerald | Verde esmeralda |
| smart-modern | Moderno |
| verde-petroleo | Verde petróleo |
| condoviva | CondoViva |
| minimal-arcos-azul | Arcos azul |
| minimal-linhas-verde | Linhas verde |
| minimal-silhueta-verde | Silhueta verde |

## Telas / sugestões de app

### HTML (`telas/html/`)
Layouts grade / destaques / lista; comparar paletas A–F; ícones.

### Stitch (`telas/stitch/`)
| Pasta | Tela |
|-------|------|
| home-dashboard-morador | Dashboard morador |
| home-grade-tiles-verde | Home grade verde |
| correspondencias-encomendas | Correspondências |
| visitas-convites | Visitas / convites |
| reservas-areas-comuns | Reservas |

## Decisão

| Tema | Escolhido | Data |
|------|-----------|------|
| Logo | _pendente_ (casa / prédio / chave / casa+chave) | |
| Layout home | _pendente_ | |
| Paleta | _pendente_ (A–F) | |
| Ícones | _pendente_ | |

Registre também em D1/D2/D3/T4: [05-perguntas-abertas.md](../../plano/05-perguntas-abertas.md).
