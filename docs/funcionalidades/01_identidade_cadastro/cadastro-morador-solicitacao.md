# Solicitação de Cadastro e Auto-Onboarding de Morador

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** A inclusão de novos moradores nos sistemas de condomínio costuma ser burocrática, manual e lenta, dependendo de formulários de papel entregues na guarita ou de trocas informais de mensagens por WhatsApp, o que aumenta o risco de invasão, dados incorretos e violação de regras da convenção.
- **Proposta de Valor:** Permitir que novos moradores (proprietários ou inquilinos) iniciem o processo de auto-cadastro diretamente pelo smartphone, enviando comprovante de residência/contrato de locação, dados civis e selfie biométrica, permitindo que o síndico ou a administradora aprovem o ingresso com um clique.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `identidade_cadastro` |
| **Subdomínio** | `onboarding` |
| **Fase de Entrega** | Fase BC-01 (Identidade e Cadastro Completo) |
| **Tabelas do Banco (pt-BR)** | `solicitacao_cadastro_morador`, `pessoa`, `ocupacao_unidade`, `anexo_solicitacao` |
| **Perfis com Acesso** | Morador solicitante (anônimo/autenticado), Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Solicitante | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Enviar solicitação de cadastro | **Sim** | — | — | — | — |
| Fazer upload de documentos e foto | **Sim** | — | — | — | — |
| Visualizar fila de solicitações pendentes | Própria | — | — | **Todas** | **Todas** |
| Solicitar correção / documento adicional | — | — | — | **Sim** | **Sim** |
| Aprovar solicitação e liberar acesso | — | — | — | **Sim** | **Sim** |
| Rejeitar solicitação com justificativa | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados e Ciclo de Vida

```text
[ENVIADA] ──► [EM_ANALISE] ──(solicitar ajuste)──► [PENDENTE_CORRECAO]
    │              │                                      │
    │              ├──(aprovação)──► [APROVADA]           └──(reenvio)──► [EM_ANALISE]
    │              │
    │              └──(rejeição)──► [REJEITADA]
    │
    └──(desistência)──► [CANCELADA]
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `ENVIADA` | Morador preencheu o formulário e submeteu comprovantes. Aguardando triagem. | Cancelamento pelo solicitante. |
| `EM_ANALISE` | Síndico ou administradora abriu o dossiê para checagem documental. | Aprovar, Rejeitar ou Solicitar Correção. |
| `PENDENTE_CORRECAO` | Documento ilegível ou divergente; solicitado novo envio ao morador. | Reenvio de anexos pelo morador. |
| `APROVADA` | Dossiê validado. Criada pessoa, ocupação ativa e emitidas credenciais de acesso. | Consulta histórica (estado terminal). |
| `REJEITADA` | Solicitação recusada formalmente com motivo registrado. | Consulta do motivo pelo solicitante. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Fluxo Principal (Auto-Cadastro pelo Morador)
1. O novo morador baixa o app ou acessa o link do condomínio e clica em **"Primeiro Acesso / Cadastrar-se"**.
2. Seleciona o condomínio, bloco e número da unidade desejada.
3. Informa seus dados civis obrigatórios: Nome Completo, CPF, Data de Nascimento, Telefone e E-mail.
   - **Checagem de CPF Existente:** Caso o CPF já exista na base de dados civil da plataforma, o sistema dispara um **Magic Link de validação de 15 minutos** para o e-mail cadastrado (conforme detalhado em [`onboarding-e-conta.md`](onboarding-e-conta.md)), garantindo a validação de titularidade antes de exibir os dados para conferência do morador.
4. Faz upload dos comprovantes obrigatórios:
   - Foto do documento oficial (RG, CNH ou RNE).
   - Comprovante de posse ou vínculo: Escritura/Matrícula (se proprietário) ou Contrato de Locação assinado (se inquilino).
   - Selfie de identificação em alta resolução (já adequada para validação biométrica).
5. O sistema grava o registro em `solicitacao_cadastro_morador` com status `ENVIADA` e notifica o síndico por push notification.
6. O síndico abre o painel web/PWA, revisa os documentos anexados e clica em **"Aprovar Cadastro"**.
7. O sistema executa atomicamente:
   - Criação ou atualização do registro civil em `pessoa`.
   - Vínculo da pessoa à unidade em `ocupacao_unidade` (com tipo `PROPRIETARIO` ou `INQUILINO`).
   - Disparo de e-mail de boas-vindas com link para criação de senha ou ativação imediata via Google Login.

### 5.2 Fluxo Alternativo (Solicitação de Correção de Documento)
1. Durante a conferência, o síndico nota que o contrato de locação está sem a página de assinaturas.
2. Clica em **"Solicitar Correção"**, digita o motivo: *"Por favor, reenvie a página final com as assinaturas reconhecidas"*.
3. O status muda para `PENDENTE_CORRECAO` e o morador recebe notificação push e e-mail com botão para anexar novo documento.
4. Ao anexar, o status retorna para `EM_ANALISE`.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O CPF informado deve ser estritamente validado pelo algoritmo oficial da Receita Federal antes do envio da solicitação.
- **RN-02:** Não é permitido submeter mais de uma solicitação com status pendente para o mesmo CPF no mesmo condomínio.
- **RN-03:** Em caso de inquilino, a data de início e término do contrato de locação deve ser informada e limitará a vigência automática da ocupação no sistema.
- **RN-04:** A aprovação de cadastro exige obrigatoriamente a presença de pelo menos um documento de identificação com foto e um comprovante de vínculo anexados.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/onboarding/`)
- `POST /api/v1/onboarding/solicitacoes`: Envio público do formulário de solicitação.
- `POST /api/v1/onboarding/solicitacoes/{id}/anexos`: Upload de documentos (multipart/form-data) para o bucket S3.
- `GET /api/v1/onboarding/solicitacoes`: Listagem de solicitações com filtros por status e bloco/unidade.
- `POST /api/v1/onboarding/solicitacoes/{id}/aprovar`: Aprovação formal e materialização dos vínculos.
- `POST /api/v1/onboarding/solicitacoes/{id}/rejeitar`: Rejeição com motivo obrigatório.

### Frontend Angular (PWA)
- Componentes: `features/identidade_cadastro/components/onboarding-wizard`, `features/identidade_cadastro/components/fila-solicitacoes`.
- Componente compartilhado: `upload-foto` para captura de selfie e documento com validação de tamanho (máximo 5MB).

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `solicitacao.recebida` | Síndico e Admin | Push + In-app | "Nova solicitação de morador para a Unidade 102 Bloco B aguardando aprovação." |
| `solicitacao.aprovada` | Morador solicitante | E-mail + Push | "Seu cadastro foi aprovado! Bem-vindo ao CondoUrban. Clique aqui para entrar." |
| `solicitacao.ajuste` | Morador solicitante | E-mail + Push | "Ação necessária: a gestão solicitou um ajuste no seu documento de cadastro." |

---

## 9. Segurança, Auditoria e LGPD

- **Dados Sensíveis:** Documentos civis e selfies possuem acesso restrito por RLS e URLs assinadas de curta duração (pre-signed URLs de 15 minutos).
- **Base Legal:** Execução de procedimentos preliminares a pedido do titular (art. 7º, V da LGPD).
- **Retenção:** Dossiês de solicitações rejeitadas são automaticamente anonimizados após 90 dias.
