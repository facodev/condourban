# Landing page (preview)

Protótipo estático da home de marketing (**M0**). Marca: **CondoUrban** (`condourban`). Logo: [`assets/condourban-logo.png`](assets/condourban-logo.png).

Três versões para escolher:

| Pasta | Estilo | URL local |
|-------|--------|-----------|
| [index.html](index.html) | **Seletor** — compare as 3 | http://127.0.0.1:8016/landing/ |
| [v1/](v1/) | Atmosférica (hero escuro + fachada) | http://127.0.0.1:8016/landing/v1/ |
| [v2/](v2/) | Clara (inspirada em CondoLiving) | http://127.0.0.1:8016/landing/v2/ |
| [v3/](v3/) | Híbrida (hero escuro + corpo claro) | http://127.0.0.1:8016/landing/v3/ |

## Abrir

1. `scripts\start-local.bat`
2. http://127.0.0.1:8016/landing/  
   ou pelo hub: http://127.0.0.1:8016/ → card **Landing pages**

## Escopo deste preview

Alinhado a [07-landing-page…](../docs/plano/07-landing-page-marketing-e-conteudo-comum.md): CTA demo + WhatsApp, login separado, gestão + acesso, sem preço inventado.

WhatsApp e e-mail são **placeholders** (`wa.me/5500000000000`, `contato@condourban.example`).

Quando existir monorepo: migrar para `apps/web-marketing` (SSR), mantendo tokens em `packages/ui-brand`.
