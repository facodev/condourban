# Agendamento de Mudanças e Uso de Elevadores de Serviço

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Conflito de duas mudanças simultâneas na mesma torre, bloqueio desordenado de elevadores em horários de pico, danos aos espelhos/cabines dos elevadores e descumprimento de horários estabelecidos pela convenção do condomínio.
- **Proposta de Valor:** Organizar o calendário de agendamento de mudanças (entrada e saída), garantindo que apenas uma mudança ocorra por turno em cada torre, coordenando o revestimento protetor (acolchoado) do elevador de serviço pela equipe de manutenção e a conferência de regras na guarita.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `portaria` |
| **Subdomínio** | `atendimento` e `mudancas` |
| **Fase de Entrega** | Fase 3 (Governança e Serviços) |
| **Tabelas do Banco (pt-BR)** | `agendamento_mudanca`, `vistoria_mudanca`, `unidade` |
| **Perfis com Acesso** | Morador solicitante, Porteiro, Zelador, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Solicitar agendamento de mudança | **Sim** | — | — | **Sim** | **Sim** |
| Aprovar / Rejeitar data e turno | — | — | — | **Sim** | **Sim** |
| Registrar vistoria prévia e posterior do elevador | — | **Sim** | **Sim** | **Sim** | — |
| Consultar calendário de mudanças da torre | Próprio | **Todas** | **Todas** | **Todas** | **Todas** |

---

## 4. Máquina de Estados do Agendamento de Mudança

```text
[SOLICITADO] ──(aprovação do síndico)──► [AGENDADO] ──(dia da mudança)──► [EM_ANDAMENTO] ──(vistoria final)──► [CONCLUIDO]
     │                                        │
     └──(rejeição/conflito de data)──► [RECUSADO] └──(cancelamento)──► [CANCELADO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Solicitação pelo Morador
1. O morador acessa `Serviços > Agendar Mudança`.
2. Seleciona o tipo: `ENTRADA` (novo morador) ou `SAIDA` (desocupação da unidade).
3. Escolhe a data desejada e o turno (ex: Manhã: 08h00 às 13h00 | Tarde: 13h00 às 18h00).
4. Informa a transportadora responsável e placa do caminhão (se souber).
5. Assina digitalmente o **Termo de Responsabilidade por Danos Patrimoniais**.
6. O sistema valida se o turno está livre na torre e envia a solicitação para aprovação do síndico.

### 5.2 Execução no Dia da Mudança
1. No dia agendado, o zelador instala a capa acolchoada no elevador de serviço e realiza a vistoria prévia com fotos no app.
2. O caminhão chega à guarita; o porteiro confirma o agendamento no terminal e orienta o estacionamento na vaga de carga e descarga.
3. Ao término da mudança, o zelador inspeciona o elevador, hall e portas; se não houver avarias, encerra a mudança como `CONCLUIDA`.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** É estritamente proibida mais de uma mudança no mesmo turno (manhã/tarde) na mesma torre/bloco.
- **RN-02:** Mudanças aos domingos e feriados nacionais são bloqueadas automaticamente pelo sistema, conforme padrão da convenção.
- **RN-03:** A solicitação de mudança deve ser feita com antecedência mínima de 48 horas úteis da data pretendida.
- **RN-04:** Em mudanças de `SAIDA`, o sistema verifica se a unidade possui pendências materiais (ex: crachás/tags de controle de acesso a serem devolvidas à administração).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/portaria/`)
- `POST /api/v1/portaria/mudancas`: Criação da solicitação de mudança.
- `GET /api/v1/portaria/mudancas/calendario`: Retorna datas e turnos ocupados por torre.
- `POST /api/v1/portaria/mudancas/{id}/aprovar`: Aprovação pela gestão.
- `POST /api/v1/portaria/mudancas/{id}/vistoria`: Registro fotográfico da vistoria do elevador.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `mudanca.agendada` | Morador | Push + E-mail | "Sua mudança para o dia 25/11 no período da manhã foi confirmada pelo síndico." |
| `mudanca.alerta_dia` | Zelador e Portaria | Alerta In-app | "Mudança agendada hoje às 08h00 na Torre B (Apto 74)." |
