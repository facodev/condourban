# Bounded Context: Portaria e Atendimento (`portaria`)

Este bounded context é dedicado à operação presencial e remota da portaria, gerenciando o fluxo humanizado de recepção, identificação de visitantes temporários, prestadores de serviços, entregas delivery e encomendas.

---

## 1. Responsabilidade do Domínio

- **Fila de Atendimento**: Registro rápido na recepção de visitantes casuais, prestadores de serviço (técnicos, reformas, limpeza), entregadores de delivery e hóspedes temporários.
- **Convites Prévios**: Validação de convites gerados pelos moradores via app com QR Code ou nome pré-liberado para entrada sem atrito.
- **Interfonia e Autorização**: Registro da autorização expressa do morador via app ou telefone antes de franquear o ingresso.
- **Recepção de Encomendas**: Cadastro de pacotes recebidos pela portaria com foto da etiqueta, registro de transportadora, notificação automática para o morador e geração de código PIN de segurança.
- **Retirada de Encomendas**: Baixa assistida com validação do código de retirada ou assinatura digital do morador/dependente.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/portaria/`)
```text
portaria/
├── __init__.py
├── router.py
├── atendimento/           # Visitantes, prestadores, hóspedes e convites prévios
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── encomendas/            # Recebimento, foto e retirada de pacotes
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/portaria/`)
```text
portaria/
├── components/
│   ├── atendimento/       # Fila da portaria: visitantes, prestadores e convites
│   └── encomendas/        # Recebimento de pacotes com foto e baixa por código
├── services/
│   └── portaria.service.ts
└── portaria.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `visita_portaria`: Atendimento na portaria (`id`, `condominio_id`, `unidade_id`, `visitante_nome`, `documento_numero`, `tipo`: `visitante`, `prestador`, `delivery`, `hospede`, `status`: `aguardando`, `autorizado`, `entrou`, `saiu`, `recusado`, `hora_entrada`, `hora_saida`, `porteiro_usuario_id`).
- `convite_visitante`: Convite prévio emitido por morador (`id`, `unidade_id`, `visitante_nome`, `codigo_qr`, `data_limite`, `limite_usos`, `usos_restantes`, `ativo`).
- `pacote_encomenda`: Encomenda recebida (`id`, `condominio_id`, `unidade_id`, `morador_pessoa_id`, `transportadora`, `codigo_rastreio`, `foto_etiqueta_url`, `codigo_retirada`, `status`: `pendente`, `retirado`, `recebido_em`, `retirado_em`, `entregador_nome`, `recebedor_nome`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/portaria/atendimento` | Fila atual de visitantes aguardando na portaria |
| `POST` | `/api/v1/portaria/atendimento` | Registro de novo visitante ou prestador |
| `POST` | `/api/v1/portaria/atendimento/{id}/autorizar` | Autorização de entrada do visitante |
| `POST` | `/api/v1/portaria/atendimento/{id}/saida` | Registro de saída da pessoa do condomínio |
| `GET` | `/api/v1/portaria/encomendas` | Listagem de pacotes aguardando retirada |
| `POST` | `/api/v1/portaria/encomendas` | Cadastro de pacote recebido com upload de foto |
| `POST` | `/api/v1/portaria/encomendas/{id}/baixa` | Baixa da encomenda com validação do PIN |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-004: Integração Intelbras e Pré-Cadastro](../../decisoes/ADR-004-integracao-intelbras-facial.md)
  - [ADR-009: Idempotência em Integrações](../../decisoes/ADR-009-idempotencia-integracoes.md)
- **Especificações Funcionais**:
  - [atendimento-visitantes-prestadores.md](atendimento-visitantes-prestadores.md)
  - [correspondencias-encomendas.md](correspondencias-encomendas.md)
  - [agendamento-mudancas.md](agendamento-mudancas.md)
  - [achados-e-perdidos.md](achados-e-perdidos.md)
- **Scripts SQL**:
  - [005-portaria.sql](../../sql/005-portaria.sql)
