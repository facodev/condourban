# Bounded Context: Controle de Acesso e IoT (`controle_acesso`)

Este bounded context é o núcleo de integração física, telemetria de hardware e segurança perimetral do condomínio, orquestrando equipamentos IoT, catracas, cancelas, leitoras faciais e fechaduras eletromagnéticas.

---

## 1. Responsabilidade do Domínio

- **Dispositivos e Topologia de Acesso**: Cadastro e monitoramento do estado operacional de controladoras, leitoras faciais (ex.: terminais Intelbras), antenas RFID (tags veiculares/pedestres) e botoeiras.
- **Credenciais de Acesso**: Gerenciamento do ciclo de vida de credenciais (senhas numéricas, cartões/tags RFID Mifare, QR Codes dinâmicos com expiração e biometria facial).
- **Regras de Autorização e Níveis de Acesso**: Associação de permissões de horários e portas autorizadas para moradores, prestadores com janelas pré-definidas e colaboradores.
- **Sincronização Idempotente com Hardware**: Comunicação resiliente com equipamentos locais via rede interna/MQTT/Webhooks, com garantia de entrega, fila de retentativas e tolerância a quedas temporárias de internet.
- **Trilha de Passagens e Eventos de Pânico**: Registro forense de passagens, fotos de captura na abertura, detecção de arrombamento de portas e alarmes de pânico silencioso.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/controle_acesso/`)
```text
controle_acesso/
├── __init__.py
├── router.py
├── dispositivos/          # Controladoras, leitoras faciais, cancelas e tags
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   ├── service.py
│   └── adapters/          # Adaptadores de hardware (Intelbras, Control iD, etc.)
│       ├── base.py
│       └── intelbras.py
├── autorizacoes/          # Perfis de acesso, regras de horário e credenciais
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── eventos/               # Logs de passagem, alertas e webhooks de hardware
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/controle_acesso/`)
```text
controle_acesso/
├── components/
│   ├── dispositivos/      # Painel de status e sincronização de hardware
│   ├── credenciais/       # Gestão de tags, biometria e senhas
│   └── eventos/           # Monitoramento de passagens em tempo real
├── services/
│   └── controle-acesso.service.ts
└── controle-acesso.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `dispositivo_acesso`: Equipamento IoT (`id`, `condominio_id`, `identificador`, `tipo`: `catraca`, `leitora_facial`, `cancela`, `fechadura_eletromagnetica`, `ip`, `porta`, `ativo`, `ultimo_ping`).
- `credencial_acesso`: Credencial de identificação (`id`, `pessoa_id`, `tipo`: `rfid_tag`, `senha_numerica`, `qr_code_dinamico`, `template_facial_url`, `valor_identificador`, `ativo`, `data_expiracao`).
- `autorizacao_acesso`: Regra de horário (`id`, `credencial_id`, `dispositivo_id`, `dias_semana`, `hora_inicio`, `hora_fim`, `valido_ate`).
- `evento_passagem_acesso`: Log de passagem (`id`, `condominio_id`, `dispositivo_id`, `pessoa_id`, `sentido`: `entrada`, `saida`, `autorizado`, `motivo_negativa`, `foto_captura_url`, `timestamp`).
- `sincronizacao_dispositivo`: Fila de sync idempotente (`id`, `dispositivo_id`, `credencial_id`, `operacao`: `incluir`, `alterar`, `remover`, `status`: `pendente`, `processado`, `falha`, `tentativas`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/controle-acesso/dispositivos` | Painel de status dos dispositivos de acesso |
| `POST` | `/api/v1/controle-acesso/dispositivos/{id}/sincronizar` | Forçar sincronização de dados com hardware |
| `GET` | `/api/v1/controle-acesso/credenciais` | Consulta de credenciais ativas por pessoa |
| `POST` | `/api/v1/controle-acesso/credenciais` | Atribuição de tag, biometria ou senha |
| `POST` | `/api/v1/controle-acesso/acionamentos/remoto` | Abertura emergencial remota de portão/cancela |
| `GET` | `/api/v1/controle-acesso/eventos` | Feed em tempo real dos logs de acesso |
| `POST` | `/api/v1/controle-acesso/webhooks/hardware` | Receptor de eventos de passagem do hardware |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-004: Integração Intelbras Facial e Pré-Cadastro](../../decisoes/ADR-004-integracao-intelbras-facial.md)
  - [ADR-009: Idempotência em Integrações e Webhooks](../../decisoes/ADR-009-idempotencia-integracoes.md)
- **Especificações Funcionais**:
  - [biometria-facial-intelbras.md](biometria-facial-intelbras.md)
  - [credenciais-e-dispositivos.md](credenciais-e-dispositivos.md)
  - [acionamentos-e-eventos.md](acionamentos-e-eventos.md)
- **Scripts SQL**:
  - [004-controle-acesso.sql](../../sql/004-controle-acesso.sql)
