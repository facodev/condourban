# Bounded Context 04: Portaria — Atendimento e Correspondências checks

Profile: light
Plan: .specs/features/bc-04-portaria/plan.md

18 checks in 4 slices · 4 one-way doors · 0 open questions

## Checks

Grouped by the spec's slices; numbering runs across the whole feature.

### S1: Correspondências — registro, PIN e baixa (P1)

**C1** - POST /api/v1/portaria/encomendas com papel ENCOMENDAS e unidade_id válido persiste status RECEBIDA, gera codigo_retirada de 4 dígitos e retorna 201
Proof: `pytest backend/tests/test_portaria.py -k "test_encomendas_create_list_baixa_por_encomendas"`

**C2** - GET /api/v1/portaria/encomendas com papel ENCOMENDAS retorna as encomendas do condomínio com status 200
Proof: `pytest backend/tests/test_portaria.py -k "test_encomendas_create_list_baixa_por_encomendas"`

**C3** - POST /api/v1/portaria/encomendas/{id}/baixa com PIN correto por ENCOMENDAS altera status para ENTREGUE, preenche retirada_em e retorna 200
Proof: `pytest backend/tests/test_portaria.py -k "test_encomendas_create_list_baixa_por_encomendas"`

**C4** - POST /api/v1/portaria/encomendas/{id}/baixa com PIN incorreto retorna 400 com detail PIN_INVALIDO
Proof: `pytest backend/tests/test_portaria.py -k "test_baixa_pin_invalido_retorna_400"`

**C5** - POST /api/v1/portaria/encomendas por MORADOR ou só PORTARIA retorna 403
Proof: `pytest backend/tests/test_portaria.py -k "test_post_encomenda_morador_e_portaria_retorna_403"`

### S2: Morador vê só as encomendas da própria unidade (P1)

**C6** - GET /api/v1/portaria/encomendas por MORADOR com ocupação na unidade U retorna apenas encomendas dessa unidade com 200
Proof: `pytest backend/tests/test_portaria.py -k "test_morador_lista_somente_propria_unidade"`

**C7** - GET /api/v1/portaria/encomendas por MORADOR não inclui encomenda de outra unidade do mesmo condomínio
Proof: `pytest backend/tests/test_portaria.py -k "test_morador_lista_somente_propria_unidade"`

**C8** - Componente de encomendas consome a API (sem lista mock embutida) e expõe codigo_retirada para status RECEBIDA
Proof: `pytest backend/tests/test_frontend_contracts.py -k "test_encomendas_sem_mock_e_com_pin"`

**C9** - Morador autenticado tem acesso de menu ao módulo portaria (consulta de encomendas)
Proof: `pytest backend/tests/test_frontend_contracts.py -k "test_menu_morador_inclui_portaria"`

**C10** - Tela de encomendas declara estado vazio legível quando a lista está vazia
Proof: `pytest backend/tests/test_frontend_contracts.py -k "test_encomendas_empty_loading_error_states"`

### S3: Atendimento de visitantes autenticado (P1)

**C11** - POST /api/v1/portaria/visitantes com papel PORTARIA e payload válido persiste e retorna 201
Proof: `pytest backend/tests/test_portaria.py -k "test_visitantes_portaria_cria_e_lista"`

**C12** - GET /api/v1/portaria/visitantes com papel PORTARIA retorna a lista do condomínio com 200
Proof: `pytest backend/tests/test_portaria.py -k "test_visitantes_portaria_cria_e_lista"`

**C13** - POST /api/v1/portaria/visitantes por MORADOR ou só ENCOMENDAS retorna 403
Proof: `pytest backend/tests/test_portaria.py -k "test_post_visitante_morador_e_encomendas_retorna_403"`

**C14** - GET/POST em /api/v1/portaria/encomendas e /api/v1/portaria/visitantes sem Bearer retorna 401
Proof: `pytest backend/tests/test_portaria.py -k "test_portaria_sem_token_retorna_401"`

### S4: Regressão BC-01 e BC-02 + usabilidade mínima (P1)

**C15** - Suíte pytest dos módulos BC-01 e BC-02 permanece verde
Proof: `pytest backend/tests/test_identidade.py backend/tests/test_ocupacao_unidade.py backend/tests/test_onboarding_veiculos.py backend/tests/test_auth.py backend/tests/test_condominio.py`

**C16** - Novos testes de portaria cobrem os critérios 1–14 com provas executáveis nomeadas
Proof: `pytest backend/tests/test_portaria.py --collect-only -q`

**C17** - Tela de encomendas declara estado de erro sem dados fictícios
Proof: `pytest backend/tests/test_frontend_contracts.py -k "test_encomendas_empty_loading_error_states"`

**C18** - Baixa operacional na UI restrita a operador de encomendas; morador vê PIN sem botão de baixa
Proof: `pytest backend/tests/test_frontend_contracts.py -k "test_encomendas_baixa_somente_operador"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| GET /api/v1/portaria/encomendas statuses (2) | `200` C2 · `401` C14 | - |
| POST /api/v1/portaria/encomendas statuses (4) | `201` C1 · `401` C14 · `403` C5 · `422` C1 | - |
| POST /api/v1/portaria/encomendas/{id}/baixa statuses (5) | `200` C3 · `400` C4 · `401` C14 · `403` C5 · `404` C3 | - |
| GET /api/v1/portaria/visitantes statuses (2) | `200` C12 · `401` C14 | - |
| POST /api/v1/portaria/visitantes statuses (4) | `201` C11 · `401` C14 · `403` C13 · `422` C11 | - |
| one-way doors (4) | `Baixa exige PIN` C3/C4 · `Escopo morador por unidade` C6/C7 · `Operação de pacotes ≠ edição civil` C1/C5 · `Papéis portaria vs encomendas` C5/C13 | - |
| Relations entities (4) | `encomenda` C1 · `unidade destino` C6 · `evento/status ENTREGUE` C3 · `visitante` C11 | - |

- Claims naming a status code, route or response shape: C1, C2, C3, C4, C5, C6, C7, C11, C12, C13, C14
- No other check claims more than the single case its proof exercises

## Swept

Where each unwritten requirement landed. All nine, one line each, every time.

- validation: C1, C4, C11
- failure modes: C4, C5, C13, C14
- idempotency: n/a - baixa é transição de estado com PIN; reenvio após ENTREGUE fora deste slice
- authorization: C5, C6, C13, C14, C18
- concurrency: n/a - sem claim de concorrência de baixa neste slice
- data lifecycle: C1, C3
- dependency failure: C17
- state transitions: C3, C4
- observability: n/a - auditoria herdada do middleware transversal; evento_encomenda opcional neste slice

## Test policy

- API FastAPI: proofs are `pytest` HTTP boundary tests with JWT claims (`create_access_token`) asserting status codes and response fields named in each check
- Frontend contracts: proofs are file-content assertions in `test_frontend_contracts.py` for mock removal, menu, empty/error states and role-gated baixa
- Level: boundary for API; source contract for UI obligations without browser harness in this profile

## Handoff

- S1–S4 ≈ 95k tokens de contexto acumulado (encomendas+atendimento+rbac+seed+UI+tests), sob o budget de 150k — one builder
