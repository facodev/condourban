# Referência visual — concorrentes (landings + apps)

Prints das páginas iniciais e das **telas de app** dos players citados em [../../plano/17-modelos-de-negocio-e-precificacao.md](../../plano/17-modelos-de-negocio-e-precificacao.md).

Cada pasta contém:

| Arquivo | Conteúdo |
|---------|----------|
| `01-landing.png` | Viewport do site público |
| `02-app-NN.(png\|jpg)` | Screenshots oficiais da Google Play (ou login web quando não há listagem) |
| `02-app-meta.json` | Package id, título, URL Play e lista de arquivos |

Prints **anonimizados** de apps de referência (UX inventário) continuam em [`../app-concorrente/`](../app-concorrente/) e [`../app-concorrente-2-simple/`](../app-concorrente-2-simple/).

| Pasta | Player | Site | App (Play / observação) |
|-------|--------|------|-------------------------|
| [Superlogica](Superlogica/) | Superlógica | https://superlogica.com/condominios/ | [Área do Condômino](https://play.google.com/store/apps/details?id=com.condor.superlogica) |
| [TownSq](TownSq/) | TownSq | https://www.townsq.com.br/ | [TownSq Community](https://play.google.com/store/apps/details?id=br.socialcondo.app) |
| [Group-Software](Group-Software/) | Group Software | https://www.groupsoftware.com.br/ | [Group Com](https://play.google.com/store/apps/details?id=br.com.comunidadesmobile_1) |
| [uCondo](uCondo/) | uCondo | https://www.ucondo.com.br/ | [uCondo](https://play.google.com/store/apps/details?id=br.com.ucondo.android) |
| [Condomob](Condomob/) | Condomob | https://condomob.net/ | [Condomob](https://play.google.com/store/apps/details?id=agile.ti.mobile.condomob) |
| [Residente-Online](Residente-Online/) | Residente Online | https://residenteonline.com/ | [Residente Online](https://play.google.com/store/apps/details?id=online.residente) |
| [MyCond](MyCond/) | MyCond | https://mycond.com.br/ | [MyCOND](https://play.google.com/store/apps/details?id=br.com.iplanner.mycondapp) |
| [Condominizando](Condominizando/) | Condominizando (wCond / Novitatus) | https://condominizando.com.br/ | Sem Play dedicado — login web [app.condominizando.com.br](https://app.condominizando.com.br/) / [wcond.com](https://www.wcond.com/) |
| [Winker](Winker/) | Winker | https://www.winker.com.br/ | [Winker](https://play.google.com/store/apps/details?id=br.com.winker) |
| [Wecondo](Wecondo/) | Wecondo | https://wecondo.com.br/ | [WeCondo](https://play.google.com/store/apps/details?id=com.wecondo) |
| [Seu-Condominio](Seu-Condominio/) | Seu Condomínio | https://www.seucondominio.com.br/ | [Seu Condomínio](https://play.google.com/store/apps/details?id=br.com.seucondominio) |
| [Condfy](Condfy/) | Condfy (acesso/portaria) | https://condfy.com.br/ | [Condfy](https://play.google.com/store/apps/details?id=br.com.condfy) |
| [Condofy](Condofy/) | Condofy (administradora) | https://www.condofy.com.br/ | [Condofy](https://play.google.com/store/apps/details?id=br.com.condofy) |
| [Morador-Online](Morador-Online/) | Morador Online (Nebbie) | https://www.moradoronline.com.br/ | [Morador Online 2.0](https://play.google.com/store/apps/details?id=br.app.mo.novomo) |
| [Condominio-Dedicado](Condominio-Dedicado/) | Condomínio Dedicado | https://www.condominiodedicado.com/ | [Condomínio Dedicado](https://play.google.com/store/apps/details?id=br.com.condominiodedicado) |

Script de re-download Play: [`_fetch_app_shots.py`](_fetch_app_shots.py) (usa `google-play-scraper`).

Capturado em set/2026. Lojas e sites mudam — tratar como referência, não inventário fechado.
