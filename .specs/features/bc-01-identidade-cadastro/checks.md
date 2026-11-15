# Bounded Context 01: Identidade e Cadastro checks

Profile: light
Plan: .specs/features/bc-01-identidade-cadastro/plan.md

22 checks in 5 slices · 4 one-way doors · 0 open questions

## Checks

Grouped by the spec's slices; numbering runs across the whole feature.

### S1: Gestão Civil de Pessoas e Separação de Contas de Acesso (P1)

**C1** - A criação de pessoa civil em POST /api/v1/identidade/pessoas persiste o registro sem conta de usuário retornando status 201
Proof: `pytest backend/tests/test_identidade.py -k "test_pessoa_dependente_sem_usuario_login"`

**C2** - O registro de conta em POST /api/v1/identidade/usuarios/registrar associa a pessoa e autentica em POST /api/v1/identidade/usuarios/login com status 200
Proof: `pytest backend/tests/test_identidade.py -k "test_usuarios_registro_e_login"`

**C3** - Tentativa de registrar usuário com e-mail duplicado em POST /api/v1/identidade/usuarios/registrar retorna status 400
Proof: `pytest backend/tests/test_identidade.py -k "test_usuarios_registro_e_login"`

**C4** - A listagem em GET /api/v1/identidade/pessoas e consulta em GET /api/v1/identidade/pessoas/me retornam os dados civis cadastrados com status 200
Proof: `pytest backend/tests/test_identidade.py -k "test_residentes_crud"`

### S2: Regras Invariantes de Ocupação da Unidade e Posse Direta (P1)

**C5** - Cadastro de PROPRIETARIO com mora_no_local=True em unidade com INQUILINO ativo em POST /api/v1/identidade/ocupacoes retorna status 400 com CONFLITO_POSSE_DIRETA
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_1_proprietario_morador_bloqueado_com_inquilino_ativo"`

**C6** - A ativação de um INQUILINO com mora_no_local=True altera automaticamente mora_no_local do PROPRIETARIO morador para False
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_1_ativacao_inquilino_desmarca_moradia_do_proprietario"`

**C7** - Vínculo TEMPORARIO ou HOSPEDE submetido sem datas em POST /api/v1/identidade/ocupacoes retorna status 400 ou 422
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_2_curto_prazo_temporario_e_hospede_exige_datas"`

**C8** - Vínculo submetido com data_fim menor ou igual a data_inicio em POST /api/v1/identidade/ocupacoes retorna status 400 ou 422
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_3_retroatividade_data_fim_maior_que_inicio"`

**C9** - Disparo de POST /api/v1/identidade/ocupacoes/rotina-expiracao transita ocupações vencidas para INATIVO com status 200
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_4_bloqueio_automatico_rotina_expiracao"`

**C10** - Cadastro de DEPENDENTE em unidade sem morador responsável residente ativo em POST /api/v1/identidade/ocupacoes retorna status 400 com DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_5_dependente_exige_responsavel_residente_ativo"`

**C11** - Inativação de ocupação do titular em POST /api/v1/identidade/ocupacoes/{id}/inativar propaga status INATIVO aos dependentes vinculados com status 200
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_5_inativacao_inquilino_cascadeia_dependentes"`

**C12** - Consultas em GET /api/v1/identidade/ocupacoes e GET /api/v1/identidade/ocupacoes/{id} retornam a ocupação com status 200
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_1_proprietario_morador_bloqueado_com_inquilino_ativo"`

**C13** - Atualização parcial de ocupação em PATCH /api/v1/identidade/ocupacoes/{id} altera campos permitidos retornando status 200
Proof: `pytest backend/tests/test_ocupacao_unidade.py -k "test_regra_1_ativacao_inquilino_desmarca_moradia_do_proprietario"`

### S3: Auto-onboarding, Convites e Validação Documental/Facial (P2)

**C14** - Geração de convite em POST /api/v1/identidade/convites cria token com validade estrita de 7 dias e retorna status 201
Proof: `pytest backend/tests/test_identidade.py -k "test_convite_dependente_gerado_com_7_dias"`

**C15** - Aceite em POST /api/v1/identidade/convites/{token}/aceitar após a validade ou em reuso retorna status 400 com CONVITE_EXPIRADO
Proof: `pytest backend/tests/test_identidade.py -k "test_convite_expirado_rejeita_ingresso"`

**C16** - Submissão de onboarding em POST /api/v1/identidade/onboarding/solicitar cria registro com status ENVIADA retornando status 201
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_solicitar_cadastro_morador_onboarding"`

**C17** - Listagem em GET /api/v1/identidade/onboarding/solicitacoes retorna as solicitações do condomínio com status 200
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_listar_solicitacoes_onboarding"`

**C18** - Aprovação em POST /api/v1/identidade/onboarding/solicitacoes/{id}/aprovar transita status para APROVADA e cria ocupacao_unidade retornando status 200
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_aprovar_solicitacao_gera_ocupacao"`

**C19** - Rejeição em POST /api/v1/identidade/onboarding/solicitacoes/{id}/rejeitar sem motivo_rejeicao retorna status 400 ou 422
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_rejeitar_solicitacao_validacao_motivo"`

### S4: Cadastro e Controle de Veículos e Vagas de Garagem (P2)

**C20** - Cadastro em POST /api/v1/identidade/veiculos-pets/veiculos grava placa em caixa alta com status 201 e GET /api/v1/identidade/veiculos-pets/veiculos lista veículos com status 200
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_cadastrar_e_listar_veiculo_placa_maiuscula"`

**C21** - Tentativa de cadastrar a mesma placa veicular para unidades distintas no mesmo condomínio em POST /api/v1/identidade/veiculos-pets/veiculos retorna status 400
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_duplicidade_placa_no_condominio_rejeitada"`

### S5: Registro de Animais Domésticos e Segurança Coletiva (P3)

**C22** - Cadastro de animal em POST /api/v1/identidade/veiculos-pets/pets persiste registro com status 201 e GET /api/v1/identidade/veiculos-pets/pets lista pets ativos com status 200
Proof: `pytest backend/tests/test_onboarding_veiculos.py -k "test_cadastrar_e_listar_pets"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| POST /api/v1/identidade/pessoas statuses (3) | `201` C1 · `400` C1 · `422` C1 | - |
| GET /api/v1/identidade/pessoas statuses (2) | `200` C4 · `401` C4 | - |
| GET /api/v1/identidade/pessoas/me statuses (3) | `200` C4 · `401` C4 · `404` C4 | - |
| POST /api/v1/identidade/usuarios/registrar statuses (3) | `201` C2 · `400` C3 · `422` C2 | - |
| POST /api/v1/identidade/usuarios/login statuses (3) | `200` C2 · `401` C2 · `422` C2 | - |
| GET /api/v1/identidade/ocupacoes statuses (2) | `200` C12 · `401` C12 | - |
| POST /api/v1/identidade/ocupacoes statuses (3) | `201` C5 · `400` C5 · `422` C7 | - |
| GET /api/v1/identidade/ocupacoes/{id} statuses (3) | `200` C12 · `401` C12 · `404` C12 | - |
| PATCH /api/v1/identidade/ocupacoes/{id} statuses (4) | `200` C13 · `400` C13 · `404` C13 · `422` C13 | - |
| POST /api/v1/identidade/ocupacoes/{id}/inativar statuses (3) | `200` C11 · `404` C11 · `422` C11 | - |
| POST /api/v1/identidade/ocupacoes/rotina-expiracao statuses (2) | `200` C9 · `401` C9 | - |
| POST /api/v1/identidade/convites statuses (4) | `201` C14 · `400` C14 · `403` C14 · `422` C14 | - |
| POST /api/v1/identidade/convites/{token}/aceitar statuses (3) | `200` C15 · `400` C15 · `404` C15 | - |
| POST /api/v1/identidade/onboarding/solicitar statuses (3) | `201` C16 · `400` C16 · `422` C16 | - |
| GET /api/v1/identidade/onboarding/solicitacoes statuses (3) | `200` C17 · `401` C17 · `403` C17 | - |
| POST /api/v1/identidade/onboarding/solicitacoes/{id}/aprovar statuses (4) | `200` C18 · `400` C18 · `403` C18 · `404` C18 | - |
| POST /api/v1/identidade/onboarding/solicitacoes/{id}/rejeitar statuses (4) | `200` C19 · `400` C19 · `403` C19 · `404` C19 | - |
| POST /api/v1/identidade/veiculos-pets/veiculos statuses (4) | `201` C20 · `400` C21 · `403` C20 · `422` C20 | - |
| GET /api/v1/identidade/veiculos-pets/veiculos statuses (2) | `200` C20 · `401` C20 | - |
| POST /api/v1/identidade/veiculos-pets/pets statuses (4) | `201` C22 · `400` C22 · `403` C22 · `422` C22 | - |
| GET /api/v1/identidade/veiculos-pets/pets statuses (2) | `200` C22 · `401` C22 | - |
| one-way doors (4) | `Pessoa vs Usuario` C1 · `Posse direta inquilino vs proprietario` C5 · `Dependente vinculado a titular residente` C10 · `Unicidade de placa no condominio` C21 | - |

- Claims naming a status code, route or response shape: C1, C2, C3, C4, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22
- No other check claims more than the single case its proof exercises

## Swept

Where each unwritten requirement landed. All nine, one line each, every time.

- validation: C7, C8
- failure modes: C3, C5, C10
- idempotency: C15
- authorization: existing - JWT Middleware e RLS no PostgreSQL via condominio_id
- concurrency: C21
- data lifecycle: C9
- dependency failure: n/a - sem dependências de serviços externos neste módulo
- state transitions: C6, C11, C18
- observability: n/a - auditoria herdada do middleware transversal da plataforma

## Handoff

- S1-S5 = 48k tokens de contexto acumulado, sob o budget de 150k - one builder
