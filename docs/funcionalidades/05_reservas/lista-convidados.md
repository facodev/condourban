# Lista de Convidados de Eventos e Festas

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Em dias de festa no condomínio, a portaria é bombardeada por listas de convidados em papel amassado ou bilhetes de última hora, causando filas gigantescas na entrada, desvios de convidados para outras torres e risco à segurança.
- **Proposta de Valor:** Vincular a lista de convidados diretamente à reserva confirmada, permitindo ao morador cadastrar nomes completos e CPFs ou compartilhar um link de pré-confirmação (RSVP), espelhando a lista em tempo real no terminal da portaria com controle de presença instantâneo.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `reservas` |
| **Subdomínio** | `agendamentos` (sub-recurso da reserva conforme ADR-013) |
| **Fase de Entrega** | Fase 2 (Operação e Lazer) |
| **Tabelas do Banco (pt-BR)** | `reserva_area_comum`, `convidado_reserva`, `visita_portaria` |
| **Perfis com Acesso** | Morador anfitrião, Porteiro (terminal da guarita), Síndico |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador Anfitrião | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Adicionar / Remover nomes na lista | **Sim** | — | — | **Sim** | — |
| Importar lista via arquivo (.CSV ou contatos) | **Sim** | — | — | — | — |
| Gerar link público de confirmação (RSVP) | **Sim** | — | — | — | — |
| Marcar presença de convidado na guarita | — | **Sim** | — | **Sim** | — |
| Consultar total de presentes vs limite do salão | **Sim (em tempo real)** | **Sim** | **Sim** | **Sim** | **Sim** |

---

## 4. Ciclo de Vida do Convidado na Lista

```text
[CONVIDADO] ──(chegada na portaria)──► [PRESENTE_NO_EVENTO] ──(término do evento)──► [SAIU]
     │
     └──(não compareceu)──► [AUSENTE]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Preenchimento da Lista pelo Morador Anfitrião
1. O morador acessa `Minhas Reservas > [Seleciona a Reserva de Aniversário] > Lista de Convidados`.
2. Pode adicionar manualmente (Nome + CPF/RG) ou clicar em **"Compartilhar Link RSVP"**.
3. Pelo link RSVP (enviado no convite de WhatsApp), os próprios amigos digitam seus nomes e documentos.
4. O app exibe o contador em tempo real: *"42 de 60 convidados cadastrados"*.

### 5.2 Liberação na Portaria no Dia do Evento
1. O convidado chega à portaria e informa: *"Boa noite, vim para a festa do Lucas no Salão de Festas"*.
2. O porteiro abre a aba **"Eventos de Hoje"** no terminal.
3. Digita as primeiras letras do nome do convidado; o sistema filtra instantaneamente.
4. O porteiro clica no botão de check-in **"Liberar Entrada"**.
5. A catraca/porta é destravada, o status do convidado muda para `PRESENTE_NO_EVENTO` e o anfitrião recebe notificação push discreta: *"Seu convidado Pedro Alves acaba de chegar"*.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-013](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-013-organizacao-diretorios.md), a lista de convidados não existe de forma autônoma; ela é estritamente vinculada a um `reserva_id` ativo.
- **RN-02:** O sistema bloqueia a adição de novos convidados se a lotação cadastrada exceder a capacidade máxima do AVCB do espaço.
- **RN-03:** A lista de convidados fica acessível para o terminal da portaria apenas no dia do evento (iniciando 2 horas antes e encerrando 2 horas após o término contratado).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/reservas/{reserva_id}/convidados`)
- `GET /api/v1/reservas/{id}/convidados`: Lista todos os convidados vinculados.
- `POST /api/v1/reservas/{id}/convidados`: Adição unitária ou em lote.
- `POST /api/v1/reservas/{id}/convidados/{convidado_id}/check-in`: Registro de entrada pelo porteiro.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `convidado.chegou` | Morador anfitrião | Push | "Convidado Marina Costa deu entrada na portaria para o seu evento." |
| `evento.lotacao_80` | Morador anfitrião | Push Alerta | "Atenção: Seu evento atingiu 80% da capacidade máxima autorizada do salão." |
