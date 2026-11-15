# Bounded Context: Reservas de Espaços Comuns (`reservas`)

Este bounded context gere todo o ciclo de agendamento, validação de regras de uso, vistorias técnicas de conservação e custódia de cauções para as áreas de lazer e convivência do condomínio.

---

## 1. Responsabilidade do Domínio

- **Agendamento e Calendário**: Interface interativa de consulta de disponibilidade de datas/horários para salões de festas, churrasqueiras, quadras e quiosques.
- **Regras de Negócio de Reserva**: Validação automática de antecedência mínima/máxima de agendamento, limite de reservas simultâneas por unidade, prazos de cancelamento sem multa e regras de adimplência do solicitante.
- **Lista de Convidados**: Cadastro antecipado de participantes pelo morador solicitante, com exportação e sincronização em tempo real com a tela da portaria para controle de recepção no dia do evento.
- **Vistorias Pré e Pós-Uso**: Checklist estruturado realizado pela equipe de zeladoria/portaria antes do início e após o término da reserva, com fotos comprobatórias do estado do espaço e dos equipamentos.
- **Controle de Caução**: Registro da retenção de garantia ou taxa de limpeza, estorno após vistoria pós-uso aprovada ou direcionamento de retenção em caso de avarias.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/reservas/`)
```text
reservas/
├── __init__.py
├── router.py
├── agendamentos/          # Reservas, calendário e gestão de convidados
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── vistorias/             # Vistoria pré/pós evento e controle de caução
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/reservas/`)
```text
reservas/
├── components/
│   ├── agendamentos/      # Calendário de reservas e lista de convidados embutida
│   └── vistorias/         # Vistorias pré/pós evento e conferência de caução
├── services/
│   └── reservas.service.ts
└── reservas.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `reserva_area_comum`: Agendamento formal (`id`, `area_comum_id`, `unidade_id`, `solicitante_pessoa_id`, `data_evento`, `hora_inicio`, `hora_fim`, `valor_taxa`, `status`: `pendente`, `aprovado`, `cancelado`, `concluido`, `criado_em`).
- `convidado_reserva`: Lista de convidados autorizados (`id`, `reserva_id`, `nome_completo`, `documento_numero`, `entrou`, `hora_entrada`).
- `vistoria_reserva`: Laudo de inspeção (`id`, `reserva_id`, `tipo`: `pre_uso`, `pos_uso`, `responsavel_pessoa_id`, `observacoes`, `status_caucao`: `retido`, `devolvido`, `retido_parcial`, `fotos_urls` JSONB, `realizado_em`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/reservas/calendario` | Consulta de datas ocupadas e disponíveis por espaço |
| `GET` | `/api/v1/reservas/agendamentos` | Listagem de reservas da unidade ou gerais |
| `POST` | `/api/v1/reservas/agendamentos` | Solicitação de nova reserva de espaço |
| `DELETE` | `/api/v1/reservas/agendamentos/{id}` | Cancelamento de agendamento de reserva |
| `GET` | `/api/v1/reservas/agendamentos/{id}/convidados` | Lista de convidados da reserva para a portaria |
| `POST` | `/api/v1/reservas/agendamentos/{id}/convidados` | Inclusão de nomes na lista de convidados |
| `GET` | `/api/v1/reservas/vistorias` | Histórico de vistorias realizadas |
| `POST` | `/api/v1/reservas/vistorias` | Registro de laudo de vistoria pré ou pós evento |

---

## 5. Rastreabilidade com Documentação Canônica

- **Especificações Funcionais**:
  - [agendamento-espacos.md](agendamento-espacos.md)
  - [lista-convidados.md](lista-convidados.md)
  - [vistorias-checkin-checkout.md](vistorias-checkin-checkout.md)
- **Scripts SQL**:
  - [002-condominio.sql](../../sql/002-condominio.sql) (`area_comum`)
  - [006-reservas.sql](../../sql/006-reservas.sql) (`reserva`, `convidado_reserva`, `vistoria_reserva`)
