# Bounded Context 02: Condomínio e Estrutura Física checks

Profile: light
Plan: .specs/features/bc-02-condominio/plan.md

18 checks in 4 slices · 4 one-way doors · 0 open questions

## Checks

Grouped by the spec's slices; numbering runs across the whole feature.

### S1: Estrutura Física — Blocos e Unidades Habitacionais (P1)

**C1** - A criação de bloco em POST /api/v1/condominio/blocos persiste o registro estrutural com status ATIVO retornando status 201
Proof: `pytest backend/tests/test_condominio.py -k "test_blocos_crud"`

**C2** - A consulta em GET /api/v1/condominio/blocos retorna a lista de blocos do condomínio com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_blocos_crud"`

**C3** - A criação de unidade em POST /api/v1/condominio/unidades vincula ao bloco pai e persiste a unidade com status 201
Proof: `pytest backend/tests/test_condominio.py -k "test_unidades_crud"`

**C4** - Tentativa de cadastrar unidade com identificação já existente no mesmo bloco em POST /api/v1/condominio/unidades retorna status 400 com UNIDADE_DUPLICADA
Proof: `pytest backend/tests/test_condominio.py -k "test_unidade_duplicada_no_bloco_retorna_400"`

**C5** - A carga massiva em POST /api/v1/condominio/unidades/importar processa planilha CSV e cria blocos e unidades retornando total com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_importar_unidades_csv"`

**C6** - A consulta em GET /api/v1/condominio/unidades retorna a lista de unidades cadastradas com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_unidades_crud"`

### S2: Mapeamento de Vagas de Garagem e Vinculação Habitacional (P1)

**C7** - O cadastro de vaga em POST /api/v1/condominio/vagas persiste os dados de tipo e cobertura retornando status 201
Proof: `pytest backend/tests/test_condominio.py -k "test_cadastrar_e_listar_vagas_garagem"`

**C8** - Tentativa de cadastrar vaga com identificação duplicada no mesmo condomínio em POST /api/v1/condominio/vagas retorna status 400 com VAGA_DUPLICADA
Proof: `pytest backend/tests/test_condominio.py -k "test_vaga_duplicada_no_condominio_retorna_400"`

**C9** - A listagem em GET /api/v1/condominio/vagas retorna as vagas de garagem cadastradas no condomínio com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_cadastrar_e_listar_vagas_garagem"`

**C10** - A atualização em PATCH /api/v1/condominio/vagas/{id} vincula ou altera a unidade habitacional associada retornando status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_atualizar_vinculo_vaga_garagem"`

### S3: Catálogo de Áreas Comuns, Lotação e Ciclo de Vida (P2)

**C11** - O cadastro de espaço compartilhado em POST /api/v1/condominio/areas-comuns persiste capacidade e horários retornando status 201
Proof: `pytest backend/tests/test_condominio.py -k "test_areas_comuns_crud"`

**C12** - A consulta de catálogo em GET /api/v1/condominio/areas-comuns lista os espaços de convivência com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_areas_comuns_crud"`

**C13** - A consulta de detalhes em GET /api/v1/condominio/areas-comuns/{id} retorna as informações completas e regras com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_areas_comuns_detalhe_e_interdicao"`

**C14** - A alteração de estado em PATCH /api/v1/condominio/areas-comuns/{id} transita o status para INTERDITADO retornando status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_areas_comuns_detalhe_e_interdicao"`

### S4: Informações Institucionais, Branding e Parâmetros Operacionais (P2)

**C15** - A consulta institucional em GET /api/v1/condominio/info retorna dados cadastrais e endereço com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_condominio_info_crud"`

**C16** - A atualização cadastral em PUT /api/v1/condominio/info persiste alterações de razão social e endereço com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_condominio_info_crud"`

**C17** - A consulta em GET /api/v1/condominio/configuracoes retorna parâmetros de branding e regras operacionais com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_condominio_configuracoes_branding_regras"`

**C18** - A personalização em PATCH /api/v1/condominio/configuracoes grava novos valores de identidade visual e horários com status 200
Proof: `pytest backend/tests/test_condominio.py -k "test_condominio_configuracoes_branding_regras"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| GET /api/v1/condominio/info statuses (3) | `200` C15 · `401` C15 · `404` C15 | - |
| PUT /api/v1/condominio/info statuses (4) | `200` C16 · `400` C16 · `403` C16 · `422` C16 | - |
| GET /api/v1/condominio/configuracoes statuses (2) | `200` C17 · `401` C17 | - |
| PATCH /api/v1/condominio/configuracoes statuses (4) | `200` C18 · `400` C18 · `403` C18 · `422` C18 | - |
| GET /api/v1/condominio/blocos statuses (2) | `200` C2 · `401` C2 | - |
| POST /api/v1/condominio/blocos statuses (4) | `201` C1 · `400` C1 · `403` C1 · `422` C1 | - |
| GET /api/v1/condominio/unidades statuses (2) | `200` C6 · `401` C6 | - |
| POST /api/v1/condominio/unidades statuses (4) | `201` C3 · `400` C4 · `403` C3 · `422` C3 | - |
| POST /api/v1/condominio/unidades/importar statuses (3) | `200` C5 · `400` C5 · `422` C5 | - |
| GET /api/v1/condominio/vagas statuses (2) | `200` C9 · `401` C9 | - |
| POST /api/v1/condominio/vagas statuses (4) | `201` C7 · `400` C8 · `403` C7 · `422` C7 | - |
| PATCH /api/v1/condominio/vagas/{id} statuses (4) | `200` C10 · `400` C10 · `404` C10 · `422` C10 | - |
| GET /api/v1/condominio/areas-comuns statuses (2) | `200` C12 · `401` C12 | - |
| POST /api/v1/condominio/areas-comuns statuses (4) | `201` C11 · `400` C11 · `403` C11 · `422` C11 | - |
| GET /api/v1/condominio/areas-comuns/{id} statuses (3) | `200` C13 · `401` C13 · `404` C13 | - |
| PATCH /api/v1/condominio/areas-comuns/{id} statuses (4) | `200` C14 · `400` C14 · `404` C14 · `422` C14 | - |
| one-way doors (4) | `Unidades vinculadas a blocos` C3 · `Unicidade de unidade por bloco` C4 · `Unicidade condominial de vagas` C8 · `Isolamento de parametros operacionais em JSONB` C18 | - |

- Claims naming a status code, route or response shape: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18
- No other check claims more than the single case its proof exercises

## Swept

Where each unwritten requirement landed. All nine, one line each, every time.

- validation: C4, C8
- failure modes: C4, C8
- idempotency: C5
- authorization: existing - JWT Middleware e RLS no PostgreSQL via condominio_id
- concurrency: C4, C8
- data lifecycle: C14
- dependency failure: n/a - sem dependências de serviços externos neste módulo
- state transitions: C14
- observability: n/a - auditoria herdada do middleware transversal da plataforma

## Handoff

- S1-S4 = 36k tokens de contexto acumulado, sob o budget de 150k - one builder
