# Agente Conversacional Multicanal (In-App & WhatsApp) checks

Profile: light
Plan: .specs/features/agente-conversacional/plan.md

23 checks in 5 slices · 6 one-way doors · 0 open questions

## Checks

Grouped by the spec's slices; numbering runs across the whole feature.

### S1: Governança de Permissões do Chatbot pelo Síndico e Motor de Opções Numeradas (P1) · 4 files · 32 KB · ~8k

**C1** - A atualização em PATCH /api/v1/chat/configuracoes pelo síndico persiste funcionalidades_ativas e prazo_cancelamento_reserva_horas e GET /api/v1/chat/configuracoes retorna os dados com status 200 (AC 1)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_configuracoes_chatbot_sindico_crud"`

**C2** - Requisições a /api/v1/chat/mensagens ou /api/v1/chat/sessoes/ativa quando funcionalidade_habilitada para agente_conversacional é false retornam status 403 com código FEATURE_DISABLED (AC 2)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_bloqueado_quando_entitlement_desabilitado"`

**C3** - Solicitar no chat uma intenção desativada pelo síndico em configuracao_chatbot.funcionalidades_ativas retorna status 200 informando o bloqueio operacional sem invocar a tool de domínio (AC 3)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_intencao_desativada_pelo_sindico_nao_executa_tool"`

**C4** - A resposta de POST /api/v1/chat/mensagens com escolhas numera as opções sequencialmente a partir de 1 e GET /api/v1/chat/sessoes/ativa expõe opcoes_pendentes com status 200 (AC 4)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_geracao_e_consulta_opcoes_pendentes_sessao"`

**C5** - Responder com o identificador numérico "1" ou "2" em POST /api/v1/chat/mensagens ou POST /api/v1/chat/webhooks/whatsapp resolve deterministicamente os parâmetros da opção ativa e avança o fluxo com status 200 (AC 5)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_resolucao_deterministica_opcao_numerada"`

**C6** - Mensagem recebida em POST /api/v1/chat/webhooks/whatsapp com assinatura HMAC inválida ou celular sem vínculo de morador ativo retorna status 401 ou 403 sem criar sessão (AC 6)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_webhook_whatsapp_rejeita_hmac_invalido_ou_celular_desconhecido"`

### S2: Reserva e Cancelamento de Espaços via Chat com Regra de Antecedência (P1) · 3 files · 28 KB · ~7k

**C7** - Solicitar reserva informando área comum e data em POST /api/v1/chat/mensagens retorna taxa_reserva, regras e lista numerada de horários livres naquela data com status 200 (AC 7)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_consulta_horarios_disponiveis_reserva"`

**C8** - Selecionar a opção numérica do horário disponível e confirmar o aceite das regras cria o registro em reserva com status CONFIRMADA ou SOLICITADA retornando protocolo com status 200 (AC 8)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_confirmacao_reserva_por_opcao_numerada"`

**C9** - Quando o slot selecionado já foi ocupado por outra unidade antes da confirmação final, o chat impede a duplicidade e devolve as opções remanescentes com status 200 (AC 9)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_reserva_conflito_concorrencia_retorna_novas_opcoes"`

**C10** - Solicitar cancelamento de reserva própria pelo chat com antecedência maior ou igual a prazo_cancelamento_reserva_horas (72h) altera reserva.status para CANCELADA com status 200 (AC 10)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_cancelamento_reserva_dentro_do_prazo_72h"`

**C11** - Tentar cancelar reserva pelo chat faltando menos horas que prazo_cancelamento_reserva_horas (72h) para inicio_em preserva reserva.status ativa e informa o limite regimental com status 200 (AC 11)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_cancelamento_reserva_fora_do_prazo_72h_bloqueado"`

### S3: Autocadastro de Visitantes, Hóspedes e Prestadores com QR Code e Biometria Facial (P1) · 4 files · 36 KB · ~9k

**C12** - Solicitar liberação de acesso no chat retorna opções numeradas para os 4 perfis (1: Visitante, 2: Hóspede, 3: Hóspede Temporário, 4: Prestador de Serviço) e modos de cadastro com status 200 (AC 12)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_opcoes_perfis_liberacao_acesso"`

**C13** - Confirmar geração de link de autocadastro no chat emite token único retornando a URL /autocadastro/{token} e GET /api/v1/portaria/autocadastro/{token} retorna os metadados do convite com status 200 (AC 13)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_gera_link_autocadastro_e_consulta_token"`

**C14** - Submeter POST /api/v1/portaria/autocadastro/{token} com dados civis, foto_facial_base64 e consentimento_lgpd=true cria credencial_acesso dos tipos QRCODE e FACIAL e enfileira sincronizacao_acesso retornando status 201 (AC 14)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_submissao_autocadastro_provisiona_qrcode_e_facial_iot"`

**C15** - Consultar ou submeter token expirado, inexistente ou já utilizado em GET ou POST /api/v1/portaria/autocadastro/{token} retorna status 404 ou 410 com CONVITE_EXPIRADO_OU_UTILIZADO (AC 15)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_autocadastro_token_expirado_ou_utilizado_retorna_410"`

### S4: Consulta de Documentos Normativos e Regras via RAG com `pgvector` (P2) · 3 files · 24 KB · ~6k

**C16** - Acionar POST /api/v1/chat/documentos/{documento_id}/indexar fragmenta o documento normativo, gera vetores via ProvedorLLM e grava documento_chunk isolado por condominio_id retornando total_chunks com status 200 (AC 16)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_indexacao_documento_chunks_pgvector"`

**C17** - Perguntar no chat sobre normas ou taxas consulta documento_chunk por similaridade vetorial no condominio_id e area_comum retornando resposta com citação do documento ou artigo e status 200 (AC 17)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_consulta_rag_documentos_com_citacao"`

**C18** - Perguntar no chat sobre tema ausente nos documentos indexados do condomínio informa que a norma não consta no acervo e oferece opção de mensagem à administração com status 200 (AC 18)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_rag_sem_similaridade_oferece_fale_conosco"`

### S5: Abertura de Ocorrências, Encomendas, Boletos e Ranking de Prestadores (P2) · 4 files · 36 KB · ~9k

**C19** - Confirmar abertura de ocorrência pelo chat persiste registro em ocorrencia com origem MORADOR e retorna o identificador de protocolo com status 200 (AC 19)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_abertura_ocorrencia_gera_protocolo"`

**C20** - Consultar encomendas pelo chat retorna os pacotes da unidade_id com status RECEBIDA exibindo transportadora, data e codigo_retirada com status 200 (AC 20)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_consulta_encomendas_pendentes_unidade"`

**C21** - Solicitar boletos ou Pix pelo chat retorna as cobranças da unidade_id em cobranca_condominial com status PENDENTE ou VENCIDO contendo valor, vencimento, linha_digitavel e codigo_pix com status 200 (AC 21)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_chat_consulta_boletos_e_pix_unidade"`

**C22** - Submeter avaliação com nota de 1 a 5 em POST /api/v1/portaria/prestadores/{prestador_id}/avaliacoes persiste em avaliacao_prestador e retorna nota_media_atualizada e total_avaliacoes com status 201 (AC 22)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_avaliar_prestador_calcula_nota_media"`

**C23** - Consultar prestadores no chat ou em GET /api/v1/portaria/prestadores/ranking retorna os profissionais filtrados por atividade e ordenados de forma decrescente por nota_media e total_avaliacoes com status 200 (AC 23)
Proof: `pytest backend/tests/test_agente_conversacional.py -k "test_ranking_prestadores_ordenado_por_nota_moradores"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| POST /api/v1/chat/mensagens statuses (5) | `200` C5 · `400` C4 · `401` C2 · `403` C2 · `422` C4 | - |
| GET /api/v1/chat/sessoes/ativa statuses (3) | `200` C4 · `401` C2 · `404` C4 | - |
| POST /api/v1/chat/webhooks/whatsapp statuses (4) | `200` C5 · `400` C6 · `401` C6 · `403` C6 | - |
| GET /api/v1/chat/configuracoes statuses (3) | `200` C1 · `401` C1 · `403` C2 | - |
| PATCH /api/v1/chat/configuracoes statuses (5) | `200` C1 · `400` C1 · `401` C1 · `403` C1 · `422` C1 | - |
| POST /api/v1/chat/documentos/{documento_id}/indexar statuses (4) | `200` C16 · `401` C16 · `403` C16 · `404` C16 | - |
| GET /api/v1/portaria/autocadastro/{token} statuses (4) | `200` C13 · `400` C15 · `404` C15 · `410` C15 | - |
| POST /api/v1/portaria/autocadastro/{token} statuses (5) | `201` C14 · `400` C14 · `404` C15 · `410` C15 · `422` C14 | - |
| POST /api/v1/portaria/prestadores/{prestador_id}/avaliacoes statuses (5) | `201` C22 · `400` C22 · `401` C22 · `403` C22 · `422` C22 | - |
| GET /api/v1/portaria/prestadores/ranking statuses (2) | `200` C23 · `401` C23 | - |
| one-way doors (6) | `Door 1: configuracao_chatbot` C1 · `Door 2: opcoes_pendentes` C5 · `Door 3: ProvedorLLM` C17 · `Door 4: documento_chunk pgvector` C16 · `Door 5: avaliacao_prestador` C22 · `Door 6: autocadastro QR Code e Facial` C14 | - |
| perfis de autocadastro no chat (4) | `Visitante` C12 · `Hospede` C12 · `Hospede Temporario` C12 · `Prestador de Servico` C12 | - |
| funcionalidades governadas pelo sindico (7) | `reservas` C3 · `visitantes_autocadastro` C12 · `ocorrencias` C19 · `documentos_rag` C17 · `encomendas` C20 · `boletos` C21 · `prestadores_ranking` C23 | - |

- Claims naming a status code, route or response shape: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22, C23 - each has a proof that crosses the boundary
- No other check claims more than the single case its proof exercises

## Swept

Where each unwritten requirement landed. All nine, one line each, every time.

- validation: C1, C14, C22
- failure modes: C9, C11, C15, C18
- idempotency: C5, C14
- authorization: C1, C2, C3, C6
- concurrency: C9
- data lifecycle: C10, C15
- dependency failure: C14, C18
- state transitions: C8, C10, C11, C15
- observability: C4, C14, C19

## Handoff

- S1-S5 = 39k tokens estimados (S1 = 8k, S2 = 7k, S3 = 9k, S4 = 6k, S5 = 9k), abaixo do budget de 150k - one builder
