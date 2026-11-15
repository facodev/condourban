# Onboarding de Conta e Gestão de Membros

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Condomínios sofrem com cadastros desatualizados, fraudes de identidade, perda de acesso a e-mails antigos e dificuldade em conceder acessos diferenciados para proprietários, inquilinos e dependentes de uma mesma unidade. Além disso, existe o risco crítico de privacidade e vazamento (LGPD), onde operadores ou síndicos poderiam usar a consulta de CPF para minerar e recuperar telefones e dados privados de moradores previamente cadastrados em outros condomínios da plataforma.
- **Proposta de Valor:** Centralizar a criação de contas com autenticação segura (JWT próprio e login social Google), permitindo a associação rápida de usuários às suas unidades com controle estrito de papéis (RBAC) e isolamento multi-tenant (RLS). Incorporar mecanismo anti-scraping com validação por Magic Link de 15 minutos para auto-onboarding e envio de e-mail preventivo com link de revogação sumária de 15 minutos em novos vínculos criados pela gestão.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `identidade_cadastro` |
| **Subdomínio** | `usuarios` e `onboarding` (unificação de contas, membros, ocupações e auto-onboarding) |
| **Fase de Entrega** | Fase BC-01 (Identidade e Cadastro Completo) |
| **Tabelas do Banco (pt-BR)** | `pessoa`, `usuario`, `membro_condominio`, `ocupacao_unidade`, `solicitacao_cadastro_morador`, `convite_cadastro_morador`, `evento_auditoria` |
| **Perfis com Acesso** | Todos os perfis autenticados; auto-atendimento para Morador/Dependente e público para Onboarding |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora | Admin Plataforma |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Cadastrar conta (Email ou Google) | Sim | Sim | Sim | Sim | Sim | Sim | Sim |
| Auto-onboarding com validação de CPF | Sim (público) | Sim (público) | — | — | — | — | — |
| Convidar dependente para unidade | Sim (titular) | — | — | — | Sim | Sim | Sim |
| Vincular morador a nova unidade | — | — | — | — | Sim | Sim | Sim |
| Cadastrar pessoa/CPF existente | — | — | — | — | Sim (sem dados) | Sim (sem dados) | Sim |
| Revogar vínculo preventivo (15 min) | Sim (titular) | Sim (titular) | — | — | — | — | — |
| Alterar papel/membro do condomínio | — | — | — | — | Sim | Sim | Sim |
| Redefinir senha de acesso | Próprio | Próprio | Próprio | Próprio | Próprio | Próprio | Próprio |
| Revogar/Desativar usuário | — | — | — | — | Sim (condo) | Sim (condo) | Sim (global) |

---

## 4. Máquina de Estados e Ciclo de Vida

```text
[CONVITE_ENVIADO] ──────(aceite pelo link)─────► [CONTA_CRIADA] ──(validação)──► [ATIVO] ──(desligamento)──► [INATIVO]
        │                                                │
        └──(expiração de 7 dias)──► [EXPIRADO]           └──(bloqueio administrativo)──► [BLOQUEADO]

[CPF_INFORMADO] ──(cpf existente no auto-onboarding)──► [MAGIC_LINK_PENDENTE (15 min)] ──(confirmação morador)──► [SOLICITACAO_ENVIADA]
        │
        └──(novo cpf)─────────────────────────────────────────────────────────────────────────────► [SOLICITACAO_ENVIADA]

[VINCULO_CRIADO_GESTAO] ──(alerta preventivo por e-mail)──► [TITULAR_NOTIFICADO]
        │
        └──(revogação pelo titular em 15 min)────────────► [VINCULO_REVOGADO / INATIVO]
```

| Estado | Descrição Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `CONVITE_ENVIADO` | Token seguro enviado por e-mail/WhatsApp para ingresso na unidade (validade de 7 dias). | Cancelamento pelo síndico ou reenvio. |
| `MAGIC_LINK_PENDENTE` | Token temporário de 15 minutos gerado quando o morador insere um CPF já existente na base. | Confirmação via clique no link recebido no e-mail cadastrado. |
| `ATIVO` | Conta verificada com credencial válida e vínculo ativo a pelo menos uma unidade do condomínio. | Acesso completo aos recursos liberados do condomínio. |
| `BLOQUEADO` | Acesso suspenso por decisão administrativa ou suspeita de invasão. | Bloqueio de login imediato na API (rejeição de JWT). |
| `INATIVO` | Vínculo de ocupação encerrado ou revogado pelo titular. | Somente consulta histórica via auditoria ou solicitação formal à gestão. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Fluxo de Auto-Onboarding e Blindagem LGPD de CPF (Novo vs. Existente)

1. **Entrada do Candidato:** O morador acessa o auto-onboarding público do condomínio e informa seu CPF.
2. **Checagem de Existência (`/onboarding/verificar-cpf`):** O backend calcula o hash SHA-256 do CPF e consulta a tabela `pessoa`.
   - **Cenário A — CPF Não Encontrado (`NOVO_CADASTRO`):** O sistema libera o formulário limpo para preenchimento de nome completo, e-mail, celular e upload de documentos.
   - **Cenário B — CPF Já Cadastrado (`EXISTENTE_CONFIRMACAO_PENDENTE`):**
     - O sistema **não** exibe dados sensíveis na tela.
     - O e-mail cadastrado é ofuscado (ex: `r***a@email.com`).
     - Um **Magic Link** com token criptográfico de expiração estrita de **15 minutos** é gerado e despachado para o e-mail do titular.
     - A interface exibe a mensagem amigável: *"Detectamos um cadastro existente associado a este CPF. Enviamos um link de validação de 15 minutos para r\*\*\*a@email.com. Por favor, clique no link recebido para confirmar sua identidade."*
3. **Validação pelo Morador (`/onboarding/confirmar-magic-link`):**
   - O morador clica no link recebido no seu e-mail pessoal.
   - O sistema valida o token de 15 minutos, confirma a titularidade e carrega os dados civis cadastrados na tela para conferência do próprio morador.
   - O morador revisa seus contatos, anexa os dados da unidade/comprovante e submete a solicitação de ingresso.

---

### 5.2 Fluxo de Cadastro Manual pelo Síndico com E-mail Preventivo e Revogação em 15 Minutos

1. **Inclusão pela Gestão:** O síndico ou administradora cadastra uma nova pessoa em `Identidade & Cadastro > Vínculos & Ocupações`.
2. **Reuso Civil Transparente (Sem Vazamento de Dados):** Se o CPF informado já existir na tabela `pessoa` (pertencente a outro condomínio), a API reutiliza o registro civil sem criar duplicidade, **mas não devolve telefones, e-mails ou dados privados prévios para a tela do síndico**, prevenindo ataques de scraping e mineração de dados.
3. **Disparo Preventivo de Segurança:**
   - O backend cria o vínculo em `membro_condominio` e gera um token criptográfico de revogação de **15 minutos**.
   - É disparado imediatamente um e-mail de alerta preventivo para o e-mail registrado do morador:
     > *"Você foi vinculado ao Condomínio [Nome]. Se você reconhece este vínculo, nenhuma ação é necessária. Se você NÃO autorizou ou não reconhece este condomínio, clique no link abaixo dentro de 15 minutos para revogar imediatamente o vínculo."*
4. **Revogação pelo Titular (`/onboarding/revogar-vinculo`):**
   - Caso o titular não reconheça o vínculo e clique no link dentro dos 15 minutos:
     - O `MembroCondominio` é marcado imediatamente como `INATIVO`.
     - Eventuais registros abertos em `OcupacaoUnidade` para aquele morador naquele condomínio são cancelados (`status = 'INATIVO'`).
     - É gerado um evento de auditoria forense imutável com a tag `VINCULO_REVOGADO_PELO_TITULAR`.
   - Se o token expirar (mais de 15 minutos), o link torna-se inválido e qualquer alteração posterior deve seguir o processo de cancelamento formal via gestão.

---

### 5.3 Fluxo de Criação de Conta de Usuário (Login Social ou E-mail/Senha)

1. **Entrada:** Usuário acessa o app Angular e seleciona "Entrar com Google" ou "Cadastrar com e-mail".
2. **Validação Google:** Caso escolha Google, a API valida o token OIDC emitido pelo Google Identity Services, extrai `email`, `google_sub`, `nome` e verifica se já existe conta.
3. **Criação de Conta:** Se nova, cria registro em `usuario` (com `google_sub` ou hash `senha_hash` gerado com argon2/bcrypt).
4. **Resolução de Pessoa:** Localiza ou cria registro civil em `pessoa` e conecta `usuario.pessoa_id`.
5. **Associação ao Condomínio:** Verifica se há convite ou aprovação pendente; se houver, vincula em `membro_condominio` (papel: `MORADOR`) e `ocupacao_unidade`.
6. **Emissão de Sessão:** A API emite token JWT com claims de `sub` (user id), `condominio_id` ativo, e `papeis`.

---

### 5.4 Tratamento de Exceções

- **Token Expirado (> 15 minutos):** Requisições a Magic Link ou Revogação após 15 minutos retornam HTTP 400 `TOKEN_INVALIDO_OU_EXPIRADO`, orientando o usuário a solicitar novo código.
- **E-mail já existente na criação de conta:** Se o usuário tentar criar conta com e-mail já cadastrado via outro método (ex: cadastrou senha e agora clica Google), a API exige confirmação de vínculo com envio de código OTP de 6 dígitos.
- **Conta sem Vínculo:** Se o usuário se cadastrar sem convite ou aprovação prévia, o app o direciona para a fila de solicitação de ingresso ([cadastro-morador-solicitacao.md](cadastro-morador-solicitacao.md)).

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01 (Unicidade de Identidade):** O CPF é único na entidade civil `pessoa` (armazenado com hash SHA-256 e criptografia AES-256). O e-mail de acesso é único na tabela `usuario`.
- **RN-02 (Sessão e RLS Multi-Tenant):** Um usuário pode possuir vínculos com múltiplos condomínios, mas a sessão ativa opera sempre sob um único `condominio_id`. Toda consulta aplica Row-Level Security (`FORCE ROW LEVEL SECURITY`), impedindo que membros de outros condomínios sejam visualizados.
- **RN-03 (Anti-Scraping / Blindagem LGPD de CPF Existente):** A API nunca devolve dados de contato (telefones, e-mails, dados prévios) de um CPF já existente para síndicos ou administradores de outros condomínios durante o cadastro manual.
- **RN-04 (Auto-Onboarding com Magic Link de 15 Minutos):** Se um candidato a morador inserir um CPF já cadastrado no auto-onboarding, a exibição e conferência de seus dados exige obrigatoriamente validação via clique no Magic Link de 15 minutos enviado ao e-mail registrado.
- **RN-05 (Revogação Preventiva pelo Titular em 15 Minutos):** Ao cadastrar manualmente um CPF já existente, a plataforma despacha e-mail preventivo ao titular contendo link de revogação de 15 minutos. O acionamento do link inativa sumariamente o membro e suas ocupações no respectivo condomínio.
- **RN-06 (Auditoria Forense de Vínculos):** A criação de vínculo de pessoa existente e a revogação pelo titular registram eventos imutáveis em `evento_auditoria` (`VINCULO_PESSOA_EXISTENTE_CRIADO` e `VINCULO_REVOGADO_PELO_TITULAR`).
- **RN-07 (Convites de Unidade):** Tokens de convite enviados a dependentes possuem validade de 7 dias e expiram imediatamente após o primeiro uso.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/identidade/`)

#### Onboarding e Magic Links
- `POST /api/v1/identidade/onboarding/verificar-cpf`: Valida se o CPF existe na base; se existir, gera Magic Link de 15 minutos e retorna e-mail mascarado.
- `POST /api/v1/identidade/onboarding/confirmar-magic-link`: Valida o token de 15 minutos e devolve os dados civis para conferência do próprio morador.
- `POST /api/v1/identidade/onboarding/revogar-vinculo`: Recebe o token preventivo de 15 minutos e inativa o vínculo de condomínio criado pela gestão.
- `GET /api/v1/identidade/onboarding/revogar-vinculo?token={token}`: Endpoint amigável para clique direto via navegador a partir do e-mail.
- `POST /api/v1/identidade/onboarding/solicitar`: Submissão de solicitação de auto-onboarding pelo morador.
- `GET /api/v1/identidade/onboarding/solicitacoes`: Listagem de solicitações para análise da gestão.
- `POST /api/v1/identidade/onboarding/solicitacoes/{id}/aprovar`: Aprovação pela gestão (cria `MembroCondominio` e `OcupacaoUnidade`).
- `POST /api/v1/identidade/onboarding/solicitacoes/{id}/rejeitar`: Rejeição fundamentada da solicitação.

#### Autenticação e Gestão de Contas
- `POST /api/v1/auth/login`: Autenticação e-mail/senha retornando JWT + refresh token.
- `POST /api/v1/auth/google`: Validação de ID Token do Google e emissão de sessão.
- `POST /api/v1/identidade/usuarios/registrar`: Registro de novas contas de usuário.
- `POST /api/v1/identidade/convites`: Envio de convite de ingresso para dependente/morador (validade de 7 dias).

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Notificação |
| :--- | :--- | :--- | :--- |
| `onboarding.magic_link` | Morador (Candidato) | E-mail | "Validação de Cadastro: Clique aqui para confirmar sua identidade. Este link expira em 15 minutos." |
| `vinculo.alerta_preventivo` | Titular do CPF | E-mail | "Alerta de Segurança: Você foi vinculado ao Condomínio X. Se não reconhecer este vínculo, clique aqui para revogar em até 15 minutos." |
| `convite.enviado` | Convidado | E-mail | "Você foi convidado para ingressar na Unidade X do Condomínio Y. Link válido por 7 dias." |
| `membro.adicionado` | Síndico e Titular | Push + In-app | "Novo morador/dependente vinculado à Unidade X." |
| `senha.redefinida` | Usuário | E-mail | "Sua senha de acesso ao CondoUrban foi alterada com sucesso." |

---

## 9. Segurança, Auditoria e LGPD

- **Separação Arquitetural ([ADR-008](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-008-pessoa-e-usuario.md)):** Dados civis e biométricos (`pessoa`) são totalmente dissociados de credenciais de login (`usuario`).
- **Isolamento Multi-Tenant ([ADR-006](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-006-isolamento-rls-postgresql.md)):** Todas as consultas operam sob `condominio_id` com Row-Level Security forçado (`FORCE ROW LEVEL SECURITY`) e usuário de banco sem privilégios de bypass (`condourban_app`).
- **Minimização de Dados (Art. 6º, III da LGPD):** O operador do sistema só tem acesso aos contatos fornecidos explicitamente no escopo do seu condomínio.
- **Trilha Forense de Auditoria:** Eventos `VINCULO_PESSOA_EXISTENTE_CRIADO` e `VINCULO_REVOGADO_PELO_TITULAR` gravam IP, User-Agent, ID de Correlação, Timestamp UTC e payload anterior/posterior na tabela `evento_auditoria`.
