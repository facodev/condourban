# ADR-003: UI, Design System, Arquitetura Tailwind CSS v4 + Angular Material 3 e Portabilidade Web (PWA)

- **Status:** Aceito
- **Data:** 2026-09-29 (Revisado em 2026-10-17 e atualizado em 2026-11-02 para Tailwind CSS v4 + Angular Material 3)
- **Relacionado:** [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md), [ADR-013](ADR-013-organizacao-diretorios.md)
- **Autores:** Arquitetura e Engenharia de Frontend

## Contexto

A plataforma de gestão condominial atende perfis heterogêneos (moradores, porteiros em guaritas, síndicos profissionais e administradoras). O sistema precisa de:
1. **Interface densa e operacional**: Tabelas com filtros rápidos, badges de status, modais de confirmação e formulários complexos.
2. **Coexistência limpa entre Design System e Componentes MDC**: Evitar conflitos de especificidade entre o reset CSS / utilitários e os componentes baseados em MDC do Angular Material 3 (`--mat-sys-*` e `.mdc-notched-outline`).
3. **Portabilidade absoluta e instalação móvel sem atrito**: Acesso via qualquer navegador moderno e instalação direta como PWA (Progressive Web App).

## Decisão

### 1. Arquitetura de Estilos: Tailwind CSS v4 (CSS-First) + Angular Material 3

1. **Tailwind CSS v4 Nativo (Sem `tailwind.config.js`)**:
   - Configurado via `@tailwindcss/postcss` em `frontend/.postcssrc.json` e carregado em `frontend/src/styles.css` através de `@import "tailwindcss";`.
   - É **estritamente proibido** criar ou utilizar arquivos `tailwind.config.js` ou diretivas legadas (`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`).
   - Toda a customização de paleta semântica, tipografia (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`), raios de borda, sombras e curvas de transição é declarada no bloco `@theme` diretamente em `frontend/src/styles.css`.
   - Utilitários compostos reutilizáveis (`tabular-nums`, `text-balance`, `surface-card`, `surface-interactive`, `focus-ring`, `container-page`, `input-control`) são declarados com a diretiva nativa `@utility`.
2. **Integração Bidirecional com Angular Material 3 (`--mat-sys-*`)**:
   - As variáveis de sistema do Material 3 (`--mat-sys-primary`, `--mat-sys-surface`, `--mat-sys-on-surface`, `--mat-sys-outline`, `--mat-sys-error`, `--mat-sys-corner-*`, etc.) são mapeadas em `:root` para os tokens institucionais do CondoUrban e expostas no `@theme` (`--color-mat-*`).
   - O reset global reside obrigatoriamente dentro de `@layer base` para respeitar a cascata de `@layer utilities` do Tailwind v4.
   - Estilizações globais de `input, select, textarea` excluem explicitamente `.mat-mdc-input-element` e `.mdc-text-field__input` via `:where(...)`, prevenindo bordas duplas em `<mat-form-field>`.
3. **Separação Estrita de Arquivos de Componente e `ViewEncapsulation`**:
   - É proibido utilizar `template` ou `styles` inline dentro de arquivos TypeScript (`.component.ts`).
   - Todo componente deve separar estritamente código TypeScript (`.component.ts`), template HTML (`.component.html` via `templateUrl`) e folhas de estilo (`.component.scss` ou `.component.css` via `styleUrls`).
   - Todo componente deve declarar `encapsulation: ViewEncapsulation.Emulated` e definir `:host` (`display: block`, `display: inline-block` ou `display: contents` para modais) a fim de isolar seu escopo visual sem vazar estilos para componentes filhos.
4. **Diretrizes Obrigatórias de Qualidade Visual e Acessibilidade (`frontend-design` & `web-design-guidelines`)**:
   - **Foco acessível**: Uso obrigatório de `:focus-visible` (ou utilitário `focus-ring`) em vez de `:focus { outline: none; }`.
   - **Transições performáticas**: Proibido o uso de `transition: all`; especificar sempre as propriedades exatas (`background-color`, `border-color`, `color`, `box-shadow`, `transform`, `opacity`) e respeitar `@media (prefers-reduced-motion: reduce)`.
   - **Tipografia e Dados**: Aplicar `text-wrap: balance` em títulos (`h1`–`h6`), `font-variant-numeric: tabular-nums` em tabelas/colunas numéricas e caractere de reticências real (`…`) em estados de carregamento.
   - **Semântica e ARIA**: Botões apenas com ícone devem conter `aria-label`; ícones decorativos devem conter `aria-hidden="true"`; modais e drawers devem aplicar `overscroll-behavior: contain`.

### 2. Portabilidade Web e PWA

1. **PWA Oficial com `@angular/service-worker`**:
   - Cache de shell de aplicação, suporte offline básico para portaria e morador, e suporte a notificações push (VAPID).
2. **Compatibilidade Cross-Browser**:
   - Compilação padrão HTML5/CSS3/ES2022 compatível com versões atuais de Google Chrome, Mozilla Firefox, Apple Safari (iOS/macOS) e Microsoft Edge.

## Consequências

### Positivas
- **Zero conflito de especificidade**: CSS Cascade Layers (`@layer base`, `@layer components`, `@layer utilities`) garantem que utilitários do Tailwind v4 funcionem previsivelmente sem `!important` e sem quebrar componentes MDC do Angular Material 3.
- **Manutenibilidade e DX superior**: Separação de `.ts`, `.html` e `.scss` em todos os 38 componentes reduz drasticamente o tamanho dos arquivos TypeScript e habilita suporte completo de intellisense/linting nos templates e estilos.

## Referências

- [ADR-001: Governança e Stack Tecnológica](ADR-001-documentacao-e-stack-tecnologica.md)
- [ADR-013: Organização de Diretórios](ADR-013-organizacao-diretorios.md)
- [docs/decisoes/Estrutura.md](Estrutura.md) — Árvore de componentes frontend
