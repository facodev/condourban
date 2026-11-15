# Agendamento de Áreas Comuns (Salão de Festas, Churrasqueira, Quadras)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Conflitos de agendamento em livros físicos de papel, moradores monopolizando espaços nobres em datas concorridas (feriados, Natal, Réveillon), falta de transparência na cobrança de taxas de limpeza e disputas por quebras ou avarias após os eventos.
- **Proposta de Valor:** Disponibilizar um sistema digital e transparente de reservas de áreas comuns no app PWA, com regras automatizadas de concorrência, cálculo de taxas de uso, bloqueio inteligente de datas conflitantes e integração direta com a lista de convidados e a vistoria de entrada/saída.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `reservas` |
| **Subdomínio** | `agendamentos` |
| **Fase de Entrega** | Fase 2 (Operação e Lazer) |
| **Tabelas do Banco (pt-BR)** | `reserva_area_comum`, `area_comum`, `termo_responsabilidade_reserva`, `cobranca_condominial` |
| **Perfis com Acesso** | Morador (reserva), Síndico, Administradora, Porteiro (consulta) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Consultar disponibilidade de datas no calendário | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** |
| Solicitar agendamento de espaço comum | **Sim (titular)** | Se config | — | — | **Sim** | **Sim** |
| Cancelar própria reserva dentro do prazo | **Sim** | — | — | — | **Sim** | **Sim** |
| Aprovar reservas manuais com taxa/caução | — | — | — | — | **Sim** | **Sim** |
| Bloquear datas administrativas (manutenção) | — | — | — | — | **Sim** | **Sim** |
| Isentar taxa ou aplicar penalidade | — | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Reserva

```text
[SOLICITADA] ──(aprovação / pagamento de taxa)──► [CONFIRMADA] ──(dia do evento)──► [EM_ANDAMENTO]
      │                                                │                                  │
      ├──(rejeição pela gestão)──► [RECUSADA]          ├──(cancelamento pelo morador)      └──(checkout)──► [CONCLUIDA]
      │                                                │   └──► [CANCELADA]
      └──(expiração de pagamento de taxa)──────────────┘
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `SOLICITADA` | Morador escolheu a data; aguardando validação de taxa ou aprovação. | Cancelamento imediato sem ônus. |
| `CONFIRMADA` | Data garantida e reservada na agenda do condomínio. | Cadastro da lista de convidados. |
| `EM_ANDAMENTO` | Espaço sob uso no dia do evento; vistoria prévia liberada. | Realização de check-in/check-out. |
| `CONCLUIDA` | Evento finalizado e vistoria de saída aprovada sem avarias. | Consulta histórica (estado terminal). |
| `CANCELADA` | Reserva cancelada pelo morador antes do evento. | Liberação automática da data na agenda. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Solicitação e Confirmação de Reserva pelo Morador
1. O morador entra em `Lazer > Reservas de Espaços`.
2. Escolhe o espaço desejado (ex: "Churrasqueira 01"). O app exibe fotos, capacidade máxima (30 pessoas), horário permitido (10h às 22h) e valor da taxa de limpeza (R$ 80,00).
3. Seleciona a data no calendário interativo (dias já ocupados aparecem desabilitados em vermelho).
4. O app exibe o **Termo de Responsabilidade e Conservação** do condomínio; o morador lê e clica em **"Li e Aceito os Termos"**.
5. O sistema valida as regras de concorrência (ex: a unidade já possui reserva ativa no mesmo mês?).
6. Se aprovada a regra, o status passa a `CONFIRMADA` e o valor da taxa de limpeza é automaticamente agendado para o próximo boleto condominial da unidade.

### 5.2 Cancelamento de Reserva
1. O morador acessa `Minhas Reservas > Cancelar`.
2. O sistema verifica a política de cancelamento: se o cancelamento ocorrer com mais de 72 horas de antecedência, a taxa é estornada integralmente; caso contrário, é retida conforme convenção.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Concorrência: A mesma unidade residencial não pode ter mais de uma reserva de fim de semana ativa simultaneamente no mesmo espaço nobre dentro do período de 30 dias.
- **RN-02:** Unidades com pendências financeiras graves ou suspensão deliberada por assembleia são bloqueadas de efetuar novas reservas (conforme regra configurável por condomínio).
- **RN-03:** O limite de convidados estabelecido no cadastro da área comum nunca pode ser excedido na lista de convidados gerada pelo morador.
- **RN-04:** Datas especiais (Natal, Réveillon, Carnaval) utilizam sorteio automatizado configurável em vez de ordem de chegada, se previsto na convenção.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/reservas/`)
- `GET /api/v1/reservas/espacos`: Lista as áreas comuns reserváveis.
- `GET /api/v1/reservas/calendario`: Retorna datas livres e ocupadas de um espaço.
- `POST /api/v1/reservas`: Criação de nova reserva.
- `PATCH /api/v1/reservas/{id}/cancelar`: Cancelamento pelo usuário ou gestão.

### Frontend Angular (PWA)
- Componente: `features/reservas/components/calendario-reservas` e `features/reservas/components/meus-agendamentos`.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `reserva.confirmada` | Morador | Push + E-mail | "Sua reserva para o Salão Gourmet no dia 15/12 foi confirmada com sucesso!" |
| `reserva.lembrete_lista` | Morador | Push (48h antes) | "Faltam 2 dias para o seu evento. Lembre-se de preencher a lista de convidados para a portaria." |
