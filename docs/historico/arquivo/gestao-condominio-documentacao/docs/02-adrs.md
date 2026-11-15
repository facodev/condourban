# ADRs — Gestão Condomínio

## ADR-001 — Monólito modular na primeira fase

**Status:** Aceito

### Contexto
O produto precisa validar rapidamente o fluxo de condomínio, moradores, portaria e controle facial.

### Decisão
Usar um monólito modular FastAPI, com fronteiras de domínio claras.

### Consequências
- menor complexidade operacional;
- transações locais simples;
- evolução posterior para serviços independentes;
- exige disciplina arquitetural para evitar acoplamento entre módulos.

---

## ADR-002 — PostgreSQL como banco principal

**Status:** Aceito

### Decisão
PostgreSQL será o banco transacional principal.

### Motivos
- transações;
- integridade referencial;
- JSONB;
- índices;
- RLS;
- maturidade;
- suporte a workloads relacionais e eventos operacionais.

---

## ADR-003 — UUID como identificador

**Status:** Aceito

Todos os identificadores públicos serão UUID.

### Motivos
- não expor sequência;
- geração distribuída;
- facilidade para integrações;
- menor risco de enumeração.

---

## ADR-004 — Isolamento por condomínio com RLS

**Status:** Aceito

Todas as tabelas operacionais pertencentes a um condomínio possuirão `condominio_id`.

O PostgreSQL aplicará Row Level Security.

A aplicação deverá estabelecer `app.condominio_id` por transação após validar a associação do usuário.

---

## ADR-005 — Keycloak para autenticação

**Status:** Aceito

Keycloak será responsável por:

- login;
- MFA quando habilitado;
- recuperação de acesso;
- emissão de tokens;
- identidade técnica.

O domínio da aplicação continua responsável por:

- vínculo da pessoa;
- condomínio;
- papéis;
- permissões;
- autorização de negócio.

---

## ADR-006 — Separar Pessoa de Usuário

**Status:** Aceito

`pessoa` representa a identidade de negócio.

`usuario` representa a conta autenticada no Keycloak.

Uma pessoa pode existir sem possuir uma conta de usuário.

---

## ADR-007 — Aprovação cadastral separada da sincronização Intelbras

**Status:** Aceito

A aprovação do cadastro não depende da disponibilidade da Intelbras.

Após aprovação:

```text
Cadastro aprovado
    |
    +--> Pessoa ativa
    +--> Vínculo ativo
    +--> Credencial criada
    +--> Sincronização pendente
```

Um trabalhador assíncrono processa a sincronização.

---

## ADR-008 — Abstração de provedor de controle de acesso

**Status:** Aceito

O domínio não chamará a API da Intelbras diretamente.

Será utilizada uma interface conceitual:

```python
class ProvedorControleAcesso(Protocol):
    async def cadastrar_credencial(...): ...
    async def atualizar_credencial(...): ...
    async def remover_credencial(...): ...
    async def criar_autorizacao(...): ...
    async def revogar_autorizacao(...): ...
    async def consultar_eventos(...): ...
```

A primeira implementação será Intelbras.

---

## ADR-009 — Arquivos fora do PostgreSQL

**Status:** Aceito

Arquivos serão armazenados em objeto compatível com S3.

PostgreSQL guarda:

- chave;
- MIME;
- tamanho;
- hash;
- versão;
- autor;
- datas;
- status.

---

## ADR-010 — Biometria facial como credencial operacional

**Status:** Aceito

A coleta facial durante o cadastro poderá gerar uma credencial utilizada no controle de acesso.

A verificação facial e a credencial operacional são entidades diferentes.

---

## ADR-011 — Não armazenar senha

**Status:** Aceito

Nenhuma senha será armazenada no banco da aplicação.

---

## ADR-012 — Auditoria obrigatória

**Status:** Aceito

Mudanças de cadastro, aprovação, rejeição, credenciais, autorizações, acessos e operações administrativas relevantes serão auditadas.

---

## ADR-013 — Idempotência em integrações

**Status:** Aceito

Operações que possam ser repetidas terão chave de idempotência e/ou referência externa.

Particularmente:

- cadastro facial;
- criação de autorização;
- revogação;
- recebimento de eventos;
- pagamentos futuros.

---

## ADR-014 — Controle de acesso baseado em credencial + autorização

**Status:** Aceito

Possuir uma credencial facial não significa ter autorização irrestrita.

O acesso será determinado por:

```text
Pessoa
+
Credencial
+
Autorização
+
Período
+
Regras
+
Dispositivo
```

---

## ADR-015 — Termos de negócio em pt-BR

**Status:** Aceito

Nomes de tabelas, campos e conceitos de negócio serão em português brasileiro.

Termos técnicos consolidados, como `JWT`, `RLS`, `UUID`, `JSONB`, `API` e `OIDC`, permanecem em sua forma técnica.
