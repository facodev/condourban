# Fase 6 — Publicação nas lojas Apple e Google Play

O produto começa como **Web + PWA**. A **Fase 6** disponibiliza o aplicativo nas **App Store (Apple)** e **Google Play**, mantendo a mesma base Angular + API Python.

## Estratégia técnica (provisão)

| Opção | Quando usar |
|-------|-------------|
| **Capacitor** (recomendado) | Empacota o Angular em shell iOS/Android; reaproveita UI e API |
| Trusted Web Activity (Play) | Alternativa só Android, mais “PWA na loja” |
| App nativo do zero | **Fora de escopo** — custo alto; só se Capacitor não atender |

Fluxo:

```text
Angular web-app (PWA)
        |
   Capacitor
   /         \
iOS (Xcode)   Android (Android Studio / Gradle)
   |              |
App Store      Google Play
```

## Escopo da fase

1. Contas e compliance: Apple Developer Program, Google Play Console, política de privacidade linkada, declaração de coleta de dados.
2. Projeto Capacitor no monorepo (`apps/mobile` ou dentro de `web-app`).
3. Plugins: push (FCM/APNs), status bar, splash, deep links (`app.` / universal links).
4. Build de produção apontando para API de produção (ou flavor staging).
5. Materiais de loja: ícones 1024, screenshots por tamanho, descrição PT-BR, classificação etária.
6. Testes: TestFlight + trilha interna/fechada Play.
7. Submissão e correção de rejeições (comum: login demo, privacidade, permissões de câmera para facial).
8. Processo de update contínuo (mesma versão semver do app web quando possível).

## Cuidados específicos deste produto

- **Câmera / biometria** (pré-cadastro facial): declarar permissões e finalidade nas lojas e na Política de Privacidade (doc 10 / 08).
- **Login**: Apple pode exigir fluxo de conta demo para review.
- **Push**: Web Push ≠ push nativo; na Fase 6 o backend passa a falar FCM/APNs (ou provedor unificado).
- Portaria/tablet pode continuar via **PWA/browser**; lojas focam no **morador** (e opcionalmente síndico).

## Dependências

- Ideal: módulos críticos estáveis (Fases 1–2+).
- Pode iniciar preparação de contas/assets em paralelo; submit após QA.

## Perguntas

Ver **S1–S4** em [05-perguntas-abertas.md](05-perguntas-abertas.md).

## Status

| Campo | Valor |
|-------|-------|
| Status | `planejado` |
| Última revisão | 2026-09-29 |
