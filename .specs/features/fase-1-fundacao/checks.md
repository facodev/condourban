# Fase 1: Fundação + Convivência Diária checks

Profile: light
Plan: `.specs/features/fase-1-fundacao/plan.md`

30 checks in 7 slices · 6 one-way doors · 0 open questions

## Checks

### S1: Autenticação Segura, Multi-tenancy e Sessão Ativa · 5 files · 45 KB · ~12k

**C1** - Envio de credenciais válidas em `POST /api/v1/auth/login` retorna 200 com claims `sub`, `condominio_id` e `papeis` no JWT (AC 1)
Proof: `pytest tests/test_auth.py -k test_login_sucesso_retorna_jwt_claims`

**C2** - Envio de credenciais inválidas em `POST /api/v1/auth/login` retorna 401 com código `CREDENCIAIS_INVALIDAS` (AC 2)
Proof: `pytest tests/test_auth.py -k test_login_credenciais_invalidas_401`

**C3** - Envio de ID Token do Google em `POST /api/v1/auth/google` retorna 200 com JWT e lista de condomínios vinculados (AC 3)
Proof: `pytest tests/test_auth.py -k test_google_oauth_retorna_token_e_condominios`

**C4** - Requisição autenticada injeta `SET LOCAL app.condominio_id` antes da execução de queries no banco (AC 4)
Proof: `pytest tests/test_auth.py -k test_sessao_injeta_app_condominio_id`

**C5** - Consulta com filtro para outro condomínio retorna conjunto vazio por aplicação de Row-Level Security (AC 5)
Proof: `pytest tests/test_auth.py -k test_rls_bloqueia_acesso_cruzado_condominios`

**C6** - Login e alteração de credencial geram registro imutável em `evento_auditoria` com IP e id_correlacao (AC 6)
Proof: `pytest tests/test_auth.py -k test_evento_auditoria_gravado_no_login`

### S2: Estrutura Física e Gestão de Pessoas e Ocupações · 8 files · 70 KB · ~18k

**C7** - Criação de bloco por síndico em `POST /api/v1/condominio/blocos` retorna 201 com o ID gerado (AC 7)
Proof: `pytest tests/test_condominio.py -k test_criar_bloco_sucesso_201`

**C8** - Criação de unidade vinculada ao bloco em `POST /api/v1/condominio/unidades` retorna 201 (AC 8)
Proof: `pytest tests/test_condominio.py -k test_criar_unidade_sucesso_201`

**C9** - Duplicação de identificação de unidade no mesmo bloco retorna 400 com código `UNIDADE_DUPLICADA` (AC 9)
Proof: `pytest tests/test_condominio.py -k test_unidade_duplicada_no_bloco_retorna_400`

**C10** - Envio de convite para dependente em `POST /api/v1/identidade/convites` gera token com validade de 7 dias e status 201 (AC 10)
Proof: `pytest tests/test_identidade.py -k test_convite_dependente_gerado_com_7_dias`

**C11** - Aceite de convite expirado após 7 dias retorna 400 com código `CONVITE_EXPIRADO` (AC 11)
Proof: `pytest tests/test_identidade.py -k test_convite_expirado_rejeita_ingresso`

**C12** - Registro de `pessoa` civil é criado sem exigência de `usuario` de login correspondente (AC 12)
Proof: `pytest tests/test_identidade.py -k test_pessoa_dependente_sem_usuario_login`

### S3: Mural Oficial de Comunicados com Confirmação Obrigatória · 4 files · 40 KB · ~12k

**C13** - Envio de comunicado pela gestão em `POST /api/v1/comunicacao/comunicados` retorna 201 e enfileira notificação (AC 13)
Proof: `pytest tests/test_comunicacao.py -k test_publicar_comunicado_retorna_201`

**C14** - Comunicado com `urgente = true` sem leitura confirmada aciona modal bloqueante impedindo navegação (AC 14)
Proof: `pytest tests/test_comunicacao.py -k test_comunicado_urgente_bloqueia_navegacao`

**C15** - Confirmação de leitura em `POST /api/v1/comunicacao/comunicados/{id}/confirmar-leitura` grava em `leitura_comunicado` e retorna 200 (AC 15)
Proof: `pytest tests/test_comunicacao.py -k test_confirmar_leitura_grava_ciencia_200`

**C16** - Tentativa de publicação de comunicado oficial por morador retorna 403 com código `PERMISSAO_NEGADA` (AC 16)
Proof: `pytest tests/test_comunicacao.py -k test_morador_publicar_comunicado_retorna_403`

### S4: Livro Digital Unificado de Ocorrências e Sigilo Anti-Retaliação · 6 files · 60 KB · ~16k

**C17** - Registro de ocorrência por morador em `POST /api/v1/comunicacao/ocorrencias` grava `origem = 'MORADOR'` com status `ABERTA` e retorna 201 (AC 17)
Proof: `pytest tests/test_comunicacao.py -k test_criar_ocorrencia_morador_origem_morador`

**C18** - Registro de ocorrência na portaria em `POST /api/v1/comunicacao/ocorrencias` grava `origem = 'PORTARIA'` e status 201 (AC 18)
Proof: `pytest tests/test_comunicacao.py -k test_criar_ocorrencia_guarita_origem_portaria`

**C19** - Ocorrência gravada com `sigilosa = true` oculta dados do autor para consultas de terceiros (AC 19)
Proof: `pytest tests/test_comunicacao.py -k test_ocorrencia_sigilosa_oculta_dados_autor`

**C20** - Tramitação de status pela gestão em `PATCH /api/v1/comunicacao/ocorrencias/{id}/status` grava histórico imutável em `historico_ocorrencia` e retorna 200 (AC 20)
Proof: `pytest tests/test_comunicacao.py -k test_tramitar_status_ocorrencia_grava_historico`

**C21** - Consulta a detalhe de ocorrência sigilosa por morador que não seja o autor retorna 404 (AC 21)
Proof: `pytest tests/test_comunicacao.py -k test_consulta_ocorrencia_sigilosa_alheia_retorna_404`

### S5: Repositório Regulatório e Documental com Controle de Acesso · 4 files · 35 KB · ~10k

**C22** - Envio de documento pela gestão em `POST /api/v1/governanca/documentos` grava metadados e retorna 201 (AC 22)
Proof: `pytest tests/test_governanca.py -k test_upload_documento_metadados_201`

**C23** - Pasta com visibilidade `ADMINISTRADORES` permite download apenas para síndico e administradora (AC 23)
Proof: `pytest tests/test_governanca.py -k test_download_documento_administradores_permitido`

**C24** - Tentativa de download de documento restrito por morador retorna 403 com código `ACESSO_RESTRITO` (AC 24)
Proof: `pytest tests/test_governanca.py -k test_morador_download_documento_restrito_retorna_403`

**C25** - Documento com vencimento a menos de 30 dias gera sinalização no painel da gestão (AC 25)
Proof: `pytest tests/test_governanca.py -k test_alerta_vencimento_documento_seguranca_30_dias`

### S6: Canal Fale Conosco Morador ↔ Administração · 4 files · 35 KB · ~10k

**C26** - Envio de mensagem em `POST /api/v1/comunicacao/fale-conosco` registra chamado com SLA de 48 horas úteis e status 201 (AC 26)
Proof: `pytest tests/test_comunicacao.py -k test_fale_conosco_mensagem_sla_48h_201`

**C27** - Consulta em `GET /api/v1/comunicacao/fale-conosco` retorna apenas conversas da própria unidade do morador e status 200 (AC 27)
Proof: `pytest tests/test_comunicacao.py -k test_fale_conosco_listagem_isolada_por_unidade`

### S7: Shell Angular PWA, Proteção de Rotas e Web Push · 5 files · 50 KB · ~15k

**C28** - Tentativa de navegação sem JWT ativo redireciona para `/auth/login` via `authGuard` (AC 28)
Proof: `pytest tests/test_frontend_contracts.py -k test_auth_guard_redireciona_para_login`

**C29** - Tentativa de acesso a rota administrativa por morador redireciona para `/comunicacao` via `papelGuard` (AC 29)
Proof: `pytest tests/test_frontend_contracts.py -k test_papel_guard_bloqueia_rota_admin`

**C30** - Shell Angular disponibiliza `manifest.webmanifest` e registro de Service Worker para PWA (AC 30)
Proof: `pytest tests/test_frontend_contracts.py -k test_manifest_e_service_worker_presentes`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| `POST /api/v1/auth/login` statuses (3) | 200 C1 · 401 C2 · 422 C2 | - |
| `POST /api/v1/auth/google` statuses (3) | 200 C3 · 401 C3 · 422 C3 | - |
| `POST /api/v1/auth/selecionar-condominio` statuses (3) | 200 C4 · 403 C5 · 422 C4 | - |
| `GET /api/v1/identidade/pessoas/me` statuses (2) | 200 C1 · 401 C2 | - |
| `POST /api/v1/identidade/convites` statuses (4) | 201 C10 · 400 C11 · 403 C10 · 422 C10 | - |
| `POST /api/v1/condominio/blocos` statuses (4) | 201 C7 · 400 C7 · 403 C7 · 422 C7 | - |
| `POST /api/v1/condominio/unidades` statuses (4) | 201 C8 · 400 C9 · 403 C8 · 422 C8 | - |
| `POST /api/v1/condominio/unidades/importar` statuses (4) | 200 C8 · 400 C9 · 403 C8 · 422 C8 | - |
| `GET /api/v1/comunicacao/comunicados` statuses (2) | 200 C13 · 401 C2 | - |
| `POST /api/v1/comunicacao/comunicados` statuses (4) | 201 C13 · 400 C13 · 403 C16 · 422 C13 | - |
| `POST /api/v1/comunicacao/comunicados/{id}/confirmar-leitura` statuses (3) | 200 C15 · 404 C15 · 422 C15 | - |
| `GET /api/v1/comunicacao/ocorrencias` statuses (2) | 200 C17 · 401 C2 | - |
| `POST /api/v1/comunicacao/ocorrencias` statuses (4) | 201 C17 · 400 C17 · 403 C17 · 422 C17 | - |
| `POST /api/v1/comunicacao/ocorrencias/{id}/eventos` statuses (4) | 201 C20 · 403 C20 · 404 C20 · 422 C20 | - |
| `PATCH /api/v1/comunicacao/ocorrencias/{id}/status` statuses (5) | 200 C20 · 400 C20 · 403 C20 · 404 C21 · 422 C20 | - |
| `GET /api/v1/governanca/documentos` statuses (2) | 200 C22 · 401 C2 | - |
| `POST /api/v1/governanca/documentos` statuses (4) | 201 C22 · 400 C22 · 403 C24 · 422 C22 | - |
| `POST /api/v1/comunicacao/fale-conosco` statuses (4) | 201 C26 · 400 C26 · 403 C26 · 422 C26 | - |
| `GET /api/v1/comunicacao/fale-conosco` statuses (2) | 200 C27 · 401 C2 | - |
| máquina de estados da ocorrência (5) | `ABERTA` C17 · `EM_ANALISE` C20 · `EM_ANDAMENTO` C20 · `RESOLVIDA` C20 · `FECHADA` C20 | - |
| níveis de urgência do comunicado (3) | `INFORMATIVO` C13 · `IMPORTANTE` C13 · `URGENTE` C14 | - |
| visibilidade de documento regulatório (2) | `PUBLICO` C22 · `ADMINISTRADORES` C23 | - |

- Claims nomeando códigos de status HTTP, rotas ou schemas possuem provas que cruzam as fronteiras do subsistema
- Nenhuma outra verificação alega escopo superior ao exercido por sua prova correspondente

## Swept

- validation: C2, C9, C11
- failure modes: C2, C5, C16, C21, C24
- idempotency: C4, C15
- authorization: C4, C5, C16, C24, C28, C29
- concurrency: C9
- data lifecycle: n/a - retenção permanente para conformidade civil, prestação de contas condominiais e auditoria LGPD
- dependency failure: C3
- state transitions: C14, C20
- observability: C6

## Handoff

Under the budget — one builder, no ask:

- S1 = ~12k tokens (autenticação JWT/Google e RLS); S2 = ~18k (estrutura física e membros); S3 = ~12k (comunicados); S4 = ~16k (livro de ocorrências); S5 = ~10k (documentos); S6 = ~10k (fale conosco); S7 = ~15k (Angular shell e PWA). Total estimado = ~93k tokens, inferior ao limite de 150k — one builder.
