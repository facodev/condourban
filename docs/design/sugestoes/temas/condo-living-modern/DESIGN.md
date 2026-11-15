---
name: Condo Living Modern
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#006242'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d55'
  on-tertiary-container: '#bdffdb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 26px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
  currency-display:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '800'
    lineHeight: 36px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system establishes a premium, tranquil, and dependable visual environment tailored for modern residential condominium management. The interface bridges the gap between functional utility (paying condo dues, authorizing visitors, booking barbecue areas) and community living (announcements, package delivery alerts, direct concierge communication).

### Brand Personality & Tone
- **Trustworthy & Secure:** High visual stability, explicit system feedback, and institutional clarity inspire confidence in financial and domestic security matters.
- **Effortless & Cordial:** Microcopy and visual cues in Brazilian Portuguese (PT-BR) adopt an approachable, polite, and respectful tone ("Bom dia", "Autorização confirmada", "Encomenda na portaria").
- **Organized & Uncluttered:** Heavy cognitive load is reduced through chunked visual information, clear categorical chips, and distinct visual priorities.

### Design Movement: Modern Corporate Clean
The aesthetic combines crisp Neo-Corporate precision with Scandinavian-inspired soft ergonomics:
- Pure whites layered over faint slate backgrounds for razor-sharp visual hygiene.
- Generous micro-radii on interactive items paired with larger rounded enclosures for cards.
- Hairline architectural borders (`border-slate-100` and `border-slate-200`) providing structural definition without visual weight.
- Functional color gating: colors are strictly operational—never decorative without intent.

## Colors

The system uses a functional, high-contrast light mode palette engineered for readability under harsh sunlight in condo common areas and swift legibility at night.

### Color Tokens & Semantic Roles
- **Primary (`#2563EB` - Royal Cobalt):** Drives actionable paths, interactive buttons, primary toggles, active bottom navigation tabs, and prominent step progressions.
- **Secondary (`#0F172A` - Deep Slate Navy):** The structural anchor. Used for primary typography, titles, dark modal sheets, high-priority notifications, and solid contrast elements.
- **Tertiary (`#10B981` - Mint Emerald):** Dedicated validation and positive state tracking. Designates collected/arrived deliveries, authorized guest entries, settled condo fees (boletos pagos), and active facility bookings.
- **Warning Accent (`#F59E0B` - Warm Amber):** Reserved for actionable delays, pending approvals, upcoming maintenance alerts, or boletos expiring today.
- **Destructive Accent (`#EF4444` - Crimson Coral):** Reserved for overdue payments, canceled visitor passes, rejected entries, and emergency alerts (Pânico/Portaria).
- **Surface & Backgrounds:**
  - Base canvas: `#F8FAFC` (Slate-50) gives natural depth under white cards.
  - Surface Primary: `#FFFFFF` (Pure White) for cards, dialogs, and sheets.
  - Surface Secondary: `#F1F5F9` (Slate-100) for nested input containers, inactive chips, and avatar backdrops.
- **Borders & Dividers:**
  - Subtle: `#E2E8F0` (Slate-200) for hairline card borders and horizontal dividers.
  - Subtle Muted: `#F1F5F9` (Slate-100) for interior nested separations.

## Typography

The design system relies on **Plus Jakarta Sans** across all roles to ensure geometric balance, open letter apertures, and friendly structural clarity.

### Hierarchy & Mobile Behavior
- **Displays & Headlines:** Set in bold and extra-bold weights with tight negative tracking (`-0.02em`) to maintain editorial punch in greeting headers (e.g., "Olá, Roberto", "Apto 402 - Bloco B").
- **Body:** Uses regular (`400`) and medium (`500`) weights with neutral tracking (`0em`) to ensure legibility when reading condo assembly minutes (atas), notices, or package details.
- **Labels & Micro-indicators:** Rendered in semi-bold (`600`) or bold (`700`) with slight positive tracking (`+0.01em`) to preserve legibility on small badge pills, timestamps, and metadata chips.
- **Numeric & Financial Content:** The custom token `currency-display` ensures bold, tabular-like numeric weights for monthly fees ("R$ 845,00") and unit identifiers.

## Layout & Spacing

The layout is built mobile-first, optimizing for one-thumb reachability and rapid vertical scanning.

### Layout Rhythm & Fluid Grid
- **Screen Margins:** Horizontal gutters default to `1.25rem` (20px) on mobile viewports (≤ 390px) to maximize card width, expanding to `1.5rem` (24px) on wider devices.
- **Column Mechanics:** Mobile views rely on a single continuous vertical stack or an asymmetric 2-column quick-action matrix (e.g., "Liberar Visitante", "Reservar Espaço", "Minhas Encomendas", "2ª Via Boleto").
- **Thumb Zone Optimization:** Primary actions, quick-release buttons, and bottom sheets reside within the lower 40% of the screen.

### Breakpoints
- **Mobile (`< 640px`):** Single-column stack, full-width action sheets, fixed bottom navigation bar (`height: 64px` plus safe-area-inset).
- **Tablet / Large Mobile Foldables (`≥ 640px`):** Max container width bound to `580px` centered with persistent margins to prevent horizontal card stretching.

## Elevation & Depth

This system intentionally relies on layered tonal contrast rather than heavy drop shadows to create a clean, high-clarity atmosphere.

### Surface Tiers
1. **Level 0 (Canvas Base):** Background `#F8FAFC`. Houses the ambient workspace.
2. **Level 1 (Cards & Lists):** Pure White `#FFFFFF` with a crisp structural hairline border (`1px solid #E2E8F0`). Shadow is ultra-diffused: `0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.02)`.
3. **Level 2 (Interactive Modules & Active Cards):** Elevated cards (e.g., incoming delivery banners, urgent warnings) use `0 8px 16px -4px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.03)` with `border-slate-200`.
4. **Level 3 (Sticky Nav, Floating Buttons, Action Sheets):** Bottom navigation and bottom-sheets utilize a slight frosted backdrop filter (`backdrop-blur-md bg-white/90`) paired with an upward diffuse shadow: `0 -4px 12px 0 rgba(15, 23, 42, 0.05)` and `border-t border-slate-100`.

## Shapes

The shape system balances modern architectural geometry with soft, approachable mobile ergonomics.

### Curvature Values
- **Primary Surfaces & Content Cards:** Built with `rounded-2xl` (`1rem` / 16px). This creates distinct, pillowy enclosures for delivery notices, access logs, and reservation grids.
- **Buttons & Text Fields:** Built with `rounded-xl` (`0.75rem` / 12px) to provide defined, tap-friendly geometry.
- **Badges, Status Chips & Floating Indicators:** Fully circular or pill-shaped (`rounded-full` / `9999px`) to immediately signal interactive or status-driven metadata.
- **Touch Target Minimums:** All interactive controls enforce a minimum footprint of `48px × 48px` regardless of their visual boundary.

## Components

### Buttons
- **Primary Action:** Solid Royal Cobalt (`#2563EB`), text white, `min-height: 48px`, font weight `600`, shape `rounded-xl`. Active state uses `#1D4ED8`.
- **Secondary / Subtle:** Surface `#F1F5F9`, text `#0F172A`, border `1px solid transparent`. Hover/Active: `#E2E8F0`.
- **Destructive:** Soft background `#FEE2E2`, text `#DC2626`.
- **Floating Action Bar / Button:** Fixed above bottom navigation, featuring high visual presence for emergency access or visitor pass creation.

### Status Badges & Chips
- **Success / Received ("Entregue", "Aprovado", "Pago"):** Background `#ECFDF5`, text `#065F46`, left-aligned dot `#10B981`.
- **Pending / In Transit ("Na Portaria", "Aguardando", "Em Aberto"):** Background `#FFFBEB`, text `#92400E`, left-aligned dot `#F59E0B`.
- **Critical / Overdue ("Vencido", "Cancelado"):** Background `#FEF2F2`, text `#991B1B`.
- **Structure:** `rounded-full`, padding `4px 10px`, typography `label-sm`.

### Input Fields & Controls
- **Text Inputs:** Height `52px`, background `#FFFFFF`, border `1.5px solid #E2E8F0`, padding `0 16px`, corner radius `rounded-xl`. On focus: border `#2563EB` with `ring-2 ring-blue-500/10`.
- **Labels:** Set in `label-md` (`#0F172A`) positioned directly above the input with a 6px gap.
- **Checkboxes & Radios:** Native touch targets padded to `48px`, active state filled with `#2563EB`, rounded for checkboxes (`6px`), circular for radios.

### Cards
- **Condo Metric / Payment Card:** `#FFFFFF`, `rounded-2xl`, `border border-slate-200/80`, internal padding `20px`. Top section contains payment status badge and period; middle houses `currency-display`; bottom houses action button ("Pagar via PIX" or "Copiar Código de Barras").
- **Visitor / Access Log Card:** Horizontal layout with visitor photo/initials avatar (`44px` circle), visitor name, scheduled time, and quick action toggle ("Revogar", "Liberar").

### Navigation & Sheets
- **Bottom Navigation Bar:** Height `64px` + device safe-area, 4 to 5 slots ("Início", "Portaria", "Reservas", "Mural", "Menu"). Active tab tinted `#2563EB` with subtle 4px dot below icon; inactive tabs `#64748B`.
- **Action Bottom Sheet:** Draggable handle (`36px × 4px`, `#CBD5E1`, `rounded-full`), white background, top-rounded `24px`, shadow level 3. Used for rapid visitor registration and amenity slot selection.