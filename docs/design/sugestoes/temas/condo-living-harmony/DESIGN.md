---
name: Condo Living Harmony
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#3f4945'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#6f7975'
  outline-variant: '#bfc9c4'
  surface-tint: '#21695a'
  primary: '#004337'
  on-primary: '#ffffff'
  primary-container: '#0d5c4d'
  on-primary-container: '#8dd2bf'
  inverse-primary: '#8fd4c1'
  secondary: '#416656'
  on-secondary: '#ffffff'
  secondary-container: '#c3ecd7'
  on-secondary-container: '#476c5b'
  tertiary: '#003e61'
  on-tertiary: '#ffffff'
  tertiary-container: '#005684'
  on-tertiary-container: '#8fcbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#aaf0dc'
  primary-fixed-dim: '#8fd4c1'
  on-primary-fixed: '#00201a'
  on-primary-fixed-variant: '#005143'
  secondary-fixed: '#c3ecd7'
  secondary-fixed-dim: '#a8cfbc'
  on-secondary-fixed: '#002115'
  on-secondary-fixed-variant: '#294e3f'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '800'
    lineHeight: 44px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 30px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-sm: 0.75rem
  margin: 1.25rem
  margin-desktop: 2.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system crafts a calm, trustworthy, and welcoming digital sanctuary for condominium communities. It caters to residents and property managers navigating day-to-day community life, including visitor management, amenity reservations, delivery alerts, and announcements. 

The aesthetic is Modern Tactile Minimalism: warm, human, and grounded. It balances crisp operational clarity with organic warmth, steering clear of cold corporate property software. Friendly rounded geometry, soft ambient shadows, tactile squishy-tile surfaces, and clean botanical tones evoke security, serene community living, and effortless daily access.

## Colors

The palette draws heavily from lush botanical greens and restorative ambient tones:
- **Primary (`#0D5C4D`)**: Deep forest teal that acts as the anchor for key actions, brand marks, active navigation indicators, and primary header elements. It signals security, stability, and elegance.
- **Secondary (`#D1FAE5` & `#ECFDF5`)**: Soft, fresh mint tones used as supportive tinted backgrounds for category icon badges, pill selections, and friendly highlights.
- **Tertiary (`#0284C7`)**: Crisp aquatic blue dedicated to secondary interactive states, notifications, and informational signals.
- **Backgrounds**: Rooted in warm, crisp neutral surfaces (`#F8FAFC` and soft tinted canvas `#F0FDF4`), preserving generous contrast and breathing room without harsh true whites.
- **Text & Content**: Deep slate (`#0F172A`) for high-contrast primary typography, supported by medium slate (`#475569`) for metadata and microcopy.

## Typography

Typography relies entirely on **Plus Jakarta Sans**, chosen for its friendly geometric curves, high legibility, and humanist undertones that resonate within Brazilian residential apps. 

- **Display & Headlines**: Bold, confident weights (`700` and `800`) provide structured visual anchor points for welcome greetings, modal headers, and section transitions.
- **Body**: Regular weights (`400`) deliver effortless scanning across notices, parcel descriptions, and resident rules.
- **Labels & Interactive UI**: Semibold (`600`) guarantees instant recognition on tile cards, chips, and bottom navigation labels.

## Layout & Spacing

The layout model is driven by an ergonomic mobile-first tile grid. The primary dashboard centers on a balanced 2-column tactile tile arrangement designed for thumb accessibility:
- **Margins & Gutters**: Outer canvas margins maintain `1.25rem` (`20px`) on mobile devices, expanding to `2.5rem` (`40px`) on desktop viewports. Grid gutters settle on `1rem` (`16px`) to produce breathable tile separations.
- **Tile Proportions**: Action tiles use aspect-ratio scaling (roughly 1:1 to 1:1.15) to maintain generous vertical touch targets of at least 110px.
- **Breakpoints**: 
  - Mobile (< 640px): 2-column tile grid, pinned bottom navigation bar.
  - Tablet (640px – 1024px): 3 to 4-column tile grid with expanded utility side panels.
  - Desktop (> 1024px): Max container width capped at 1200px, utilizing a responsive card layout flanked by management dashboards.

## Elevation & Depth

Visual hierarchy uses soft ambient diffusion paired with subtle border containment:
- **Card Surfaces**: Pure white cards (`#FFFFFF`) float on soft-tinted backgrounds (`#F8FAFC` to `#F0FDF4`).
- **Tactile Shadows**: Low-opacity, warm forest-tinted drop shadows create physical lift without visual clutter (`box-shadow: 0 8px 24px -4px rgba(13, 92, 77, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.03)`).
- **Subtle Perimeter Contours**: Every tile features an ultra-delicate outline (`1px solid rgba(226, 232, 240, 0.8)`) to maintain distinct edges on all displays.
- **Active & Pressed Depth**: Interactive tiles respond with gentle scale compression (`transform: scale(0.97)`) and reduced elevation on tap, simulating physical push switches.

## Shapes

The design system embraces an ultra-soft, friendly visual vocabulary using **Pill-shaped (level 3)** radius tokens:
- **Tiles and Primary Cards**: Generously radiused using `rounded-3xl` (`1.5rem` to `1.75rem` / `24px` to `28px`), giving them a tactile, pebble-like quality.
- **Pills, Chips, & Badges**: Fully rounded (`border-radius: 9999px`) for resident tags, condominium selectors, and status notifications.
- **Icon Pods**: Rounded squares (`1rem` / `16px`) tinted in gentle mint green (`#ECFDF5`) that cradle central icon vectors.

## Components

### Action Tiles (Grid Hub)
- **Structure**: White base (`#FFFFFF`), `rounded-3xl` (24px radius), soft ambient drop shadow, and delicate border.
- **Content**: Centered vertical stack featuring a 52x52px soft mint rounded icon pod (`#ECFDF5`) hosting deep teal vector icons (`#0D5C4D`), followed by semibold label text (`label-md`).
- **States**: Hover/press initiates soft primary tint glow and micro-scale down (`0.98`).

### Buttons
- **Primary Button**: Deep forest teal fill (`#0D5C4D`), crisp white text, pill-shaped (`9999px`), 48px to 54px touch height, semibold label.
- **Secondary / Ghost Button**: Translucent mint tint (`#ECFDF5`) with primary teal text (`#0D5C4D`), no harsh border, completely rounded.

### Chips & Selectors
- **Condo / Unit Switcher**: Compact pill capsule with a live indicator dot (`#10B981`), light mint surface (`#ECFDF5`), deep teal text, and subtle down chevron.
- **Category Filter Chips**: Fully rounded pill capsules; inactive states use pure white with faint borders, active states switch to solid forest teal with white typography.

### Form Inputs
- **Fields**: Extra-plush 52px height, 16px radius, neutral off-white surface (`#F8FAFC`), deep slate typography, focusing to a solid forest teal rim glow with soft mint outline expansion.

### Checkboxes & Radios
- **Selection Controls**: Smooth rounded boxes (for checkboxes) and circles (for radios) in deep forest teal fill when checked, displaying crisp white checkmarks. Unchecked states use soft muted borders on off-white backgrounds.

### Floating Bottom Navigation Bar
- **Bar Container**: Elevated pill dock or softly rounded card anchored to the bottom edge (`rounded-3xl`), finished in pure white with diffused top-shadow.
- **Nav Items**: Active destination is highlighted via a soft mint pill backdrop (`#D1FAE5`) enclosing a deep forest teal icon and label. Inactive items use muted neutral slate (`#64748B`).