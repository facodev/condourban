# Sugestões de layout

Foco na **home do morador** (primeiro viewport do app). Landing tem composição própria (doc 07) — brand em destaque, sem dashboard.

Abra as amostras HTML em [amostras/](amostras/).

---

## Layout 1 — Grade de atalhos (tiles)

Arquivo: [layout-grade.html](amostras/layout-grade.html)

```
[ Logo / condomínio ]
[  tile  ][  tile  ]
[  tile  ][  tile  ]
[  tile  ][  tile  ]
[==== nav inferior ====]
```

**Prós:** igual à referência UX que o time já analisou; descoberta rápida; touch-friendly.  
**Contras:** muitas features = scroll longo; hierarquia fraca entre módulos.  
**Quando usar:** Fase 1–2 com 6–12 módulos.

---

## Layout 2 — Destaques + grade

Arquivo: [layout-destaques.html](amostras/layout-destaques.html)

```
[ Logo / condomínio ]
[  ● Acionamentos ] [ ● Convites ]   ← círculos / ações quentes
Recursos
[ tile ][ tile ]
[ tile ][ tile ]
[==== nav ====]
```

**Prós:** destaca 1–2 ações frequentes (convite, acionamento); resto organizado.  
**Contras:** acionamentos só na Fase 4 — no início os “destaques” podem ser Reservas + Correspondências.  
**Quando usar:** a partir da Fase 2; espelha concorrente “Simple”.

---

## Layout 3 — Lista por seções

Arquivo: [layout-lista.html](amostras/layout-lista.html)

```
[ Header ]
Principal
  › Reservas
  › Correspondências
Acesso
  › Visitantes
  › Convites
[==== nav ====]
```

**Prós:** escala bem com dezenas de módulos; agrupa como o drawer.  
**Contras:** menos “app moderno”; mais toques para achar ícone.  
**Quando usar:** síndico/administradora ou morador com muitos módulos (Fase 7+).

---

## Shell comum (todos os layouts)

| Elemento | Regra |
|----------|--------|
| Header | Nome do condomínio + troca de condomínio (multi-tenant) |
| Nav inferior | Home · Notificações · Perfil (máx. 3–5 itens) |
| Drawer | Categorias: Principal / Acesso / Serviços / Comunicação / Cadastros |
| Cards | Evitar card no hero; tiles só como atalho de ação |

## Landing (lembrete)

Uma composição: marca dominante, 1 headline, 1 frase, 1 CTA, imagem full-bleed — ver regras de design do projeto. Não misturar grade de app na landing.

## Recomendação provisória

- **Morador F1–F2:** Layout 1 (grade); evoluir para **Layout 2** quando houver 2 ações quentes claras.  
- **Síndico:** Layout 3 ou dashboard leve (não no primeiro viewport do morador).
