# Documentação do projeto

**Fonte da verdade** do planejamento e do histórico. Versionar no Git; não depende de chat ou máquina específica.

## Estrutura canônica

```
docs/
├── README.md              ← você está aqui
├── funcionalidades/       ← 9 Bounded Contexts (arquitetura de domínio + specs de features + MAPA.md)
├── plano/                 ← planos vivos (00–18) + INDICE.md
├── sql/                   ← DDL PostgreSQL de referência (001–009)
├── decisoes/              ← ADRs
├── conteudo/              ← FAQ e políticas (rascunho)
├── design/                ← tokens oficiais + sugestões
│   └── sugestoes/         ← logos, telas, temas, nomes-marca
├── referencia/            ← prints de apps concorrentes
└── historico/
    ├── CHANGELOG.md
    ├── journal/
    └── arquivo/           ← pacotes substituídos (não editar)
```

## Por onde navegar

| Precisa de… | Abra |
|-------------|------|
| Estado atual / o que fazer agora | [plano/04-status-e-proximos-passos.md](plano/04-status-e-proximos-passos.md) |
| **Documentação por domínio (bounded context)** | [funcionalidades/README.md](funcionalidades/README.md) |
| **Matriz de Rastreabilidade Técnica** | [funcionalidades/MAPA.md](funcionalidades/MAPA.md) |
| **Decisões ainda abertas** (nome, logo, hospedagem, modelo de negócios…) | [plano/18-decisoes-a-tomar.md](plano/18-decisoes-a-tomar.md) |
| Mapa de todos os planos | [plano/INDICE.md](plano/INDICE.md) |
| Spec de uma feature ou domínio | [funcionalidades/README.md](funcionalidades/README.md) |
| Por que decidimos X | [decisoes/README.md](decisoes/README.md) |
| Schema do banco | [sql/README.md](sql/README.md) |
| Visual / marca | [design/README.md](design/README.md) |
| Histórico do dia | [historico/CHANGELOG.md](historico/CHANGELOG.md) |

Pacotes antigos (ex.: `gestao-condominio-documentacao`) ficam em [historico/arquivo/](historico/arquivo/README.md) — **não** são canônicos.

## Como manter a documentação

### Ao terminar uma sessão de trabalho

1. **CHANGELOG** — uma ou mais linhas em `historico/CHANGELOG.md` (data, o quê, por quê).
2. **Status** — ajustar `plano/04-status-e-proximos-passos.md` (feito / em andamento / próximo).
3. **Journal** (recomendado para sessões longas) — criar `historico/journal/AAAA-MM-DD-titulo-curto.md`.
4. **Segurança + FAQ + Políticas** — obrigatório a cada feature: ver [plano/10-seguranca-faq-politicas-ritual.md](plano/10-seguranca-faq-politicas-ritual.md). Rascunhos em `conteudo/faq/` e `conteudo/politicas/`.

### Ambiente local

- Copiar `.env.example` → `.env` (o `.env` **não** vai para o Git — ver `.gitignore`).
- Nunca commitir secrets, chaves Intelbras ou VAPID reais.

### Ao decidir arquitetura ou produto

- Copiar `decisoes/ADR-000-template.md` → `ADR-NNN-titulo-kebab.md`.
- Referenciar o ADR no plano afetado (ex.: arquitetura).

### Ao responder perguntas abertas / fechar decisões

- Checklist acionável: [plano/18-decisoes-a-tomar.md](plano/18-decisoes-a-tomar.md).
- **Manter** o texto da pergunta em `plano/05-perguntas-abertas.md`; preencher a coluna **Resposta** na mesma linha (nunca apagar a pergunta).
- Atualizar **Status** para `resolvida (AAAA-MM-DD)` ou `parcial`.
- **Espelhar** a decisão no plano ou ADR correspondente (o arquivo 05 continua sendo o histórico das perguntas).
- Registrar no `CHANGELOG` quando fechar ou alterar uma resposta importante.

### Migração para outra máquina

1. Clonar ou copiar o repositório inteiro (incluindo `docs/`).
2. Ler `plano/INDICE.md` → `04-status-e-proximos-passos.md` → últimas entradas do `CHANGELOG`.
3. Continuar de onde parou; registrar nova sessão no CHANGELOG.

## Convenções

- Idioma dos planos: **português (BR)**.
- Datas: **AAAA-MM-DD** (ISO).
- Status nos planos: `planejado` | `em andamento` | `concluído` | `adiado` | `cancelado`.
- Versão do produto ainda não definida; marcos usam **Fase / Etapa** do roadmap.
