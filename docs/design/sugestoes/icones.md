# Sugestões de ícones

Uma única família no app + landing. Evitar misturar Material + Font Awesome + PNG soltos.

Amostra: [amostras/icones-amostra.html](amostras/icones-amostra.html).

---

## Opção I1 — Lucide (recomendada)

- Estilo: outline, 24px, stroke ~1.75–2
- Licença: ISC
- Pacote: `lucide-angular` / SVG
- **Prós:** limpo, consistente, leve; combina com brand verde/azul
- **Contras:** menos “filled” nativo (pode dual tone manual)

## Opção I2 — Material Symbols (Outlined)

- Estilo: Google Material Symbols Outlined
- **Prós:** enorme catálogo; familiar Android
- **Contras:** visual genérico; peso se carregar fonte completa

## Opção I3 — Phosphor Icons

- Estilo: regular / duotone opcional
- **Prós:** mais personalidade que Material; weights variados
- **Contras:** duotone pode poluir se usado em tudo

---

## Mapa mínimo (home) — ícone = significado óbvio

| Módulo | Ideia visual | Lucide | Material Symbols |
|--------|--------------|--------|------------------|
| Comunicados / Mural | Megafone (aviso) | `megaphone` | `campaign` |
| Ocorrências | Alerta | `triangle-alert` | `report_problem` |
| Documentos | Folha / arquivo | `file-text` | `description` |
| Reservas | Calendário | `calendar-days` | `event` |
| **Correspondências** | **Carta / envelope** | **`mail`** | **`mail`** |
| Convites | Ticket / ingresso | `ticket` | `confirmation_number` |
| Visitantes | Pessoa na porta | `user-round` + `door-open` | `badge` |
| Portaria / Acesso | Porta | `door-open` | `door_front` |
| Acionamentos | Controle remoto | `smartphone` / `radio` | `settings_remote` |
| Enquetes | Urna / voto | `vote` | `ballot` |
| Automóveis | Carro | `car` | `directions_car` |
| Pets | Pata | `paw-print` | `pets` |
| Configurações | Engrenagem | `settings` | `settings` |
| Notificações | Sino | `bell` | `notifications` |
| Perfil | Pessoa | `user` | `person` |

> Evitar: avião de papel para comunicados; caixa/`package` para correspondência (usar **carta**); “sol/broadcast” genérico para reservas.

## Regras de uso

1. Cor do ícone = `--color-brand` em tiles; `--color-ink-muted` em lista inativa.
2. Tamanho tile: 28–32px ícone + label 14px.
3. Não usar emoji como ícone de produto.
4. Estado ativo na nav: ícone brand + fundo soft (`--color-brand-soft`).

## Recomendação provisória

**Lucide (I1)** no app; Material só se o time já padronizar Angular Material + ícones Google.
