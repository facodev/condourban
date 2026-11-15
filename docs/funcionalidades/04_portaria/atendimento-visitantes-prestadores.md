# Atendimento de Portaria (Visitantes, Convidados e Prestadores de Serviços)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Portarias sobrecarregadas, filas de carros e entregadores nas entradas, interfones ocupados e o risco crítico de segurança ao permitir o ingresso de pessoas não identificadas ou sem autorização expressa do morador.
- **Proposta de Valor:** Centralizar em uma única tela de guarita de alta produtividade (FastAPI + Angular) todo o fluxo de atendimento da portaria, unificando a identificação civil, conferência de convites gerados pelos moradores, autorização de prestadores de serviço e registro de entrada e saída.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `portaria` |
| **Subdomínio** | `atendimento` (consolidação conforme ADR-013) |
| **Fase de Entrega** | Fase 2 (Operação e Portaria) |
| **Tabelas do Banco (pt-BR)** | `pessoa`, `visita_portaria`, `autorizacao_acesso`, `convite_visitante` |
| **Perfis com Acesso** | Porteiro/`PORTARIA` (liberação de entrada), Morador (convites), Síndico; papel `ENCOMENDAS` **não** libera visitantes |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Encomendas | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Enviar convite / pré-autorizar visitante | **Sim** | — | — | — | **Sim** | — |
| Pré-autorizar prestador de serviço na unidade | **Sim** | — | — | — | **Sim** | — |
| Registrar entrada de visitante não prévio | — | **Sim** | — | — | **Sim** | — |
| Capturar foto de documento / rosto na guarita | — | **Sim** | — | — | **Sim** | — |
| Registrar saída (check-out) | — | **Sim** | — | — | **Sim** | — |
| Consultar painel de pessoas presentes no prédio | — | **Sim** | — | **Sim** | **Sim** | **Sim** |

---

## 4. Máquina de Estados do Atendimento de Portaria

```text
[PRE_AUTORIZADO] ──(chegada na guarita)──► [NA_PORTARIA] ──(identificado)──► [NO_CONDOMINIO]
        │                                         │                                │
        └──(não compareceu)──► [EXPIRADO]          └──(morador recusa)──► [RECUSADO] └──(saída)──► [CONCLUIDO]
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `PRE_AUTORIZADO` | Convite gerado pelo morador com antecedência via app. | Liberação rápida por QR Code ou CPF. |
| `NA_PORTARIA` | Visitante ou prestador aguardando liberação na guarita. | Consulta ao morador via interfone ou push. |
| `NO_CONDOMINIO` | Acesso concedido. Pessoa encontra-se fisicamente no condomínio. | Registro de saída (check-out). |
| `RECUSADO` | Morador não atendeu, não autorizou ou identificação inválida. | Entrada barrada e motivo arquivado. |
| `CONCLUIDO` | Pessoa registrou saída e deixou as dependências do prédio. | Consulta em histórico pericial. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Entrada Rápida com Convite Prévio (QR Code ou CPF)
1. Morador gera convite no app para um amigo com nome e data do evento.
2. O convidado chega à portaria e apresenta o QR Code no leitor ou dita seu CPF.
3. A tela do terminal da guarita exibe instantaneamente: Nome do Convidado, Foto (se houver), Unidade de Destino e Autorizador.
4. O porteiro confere o documento oficial e clica no botão de atalho **"Liberar Entrada"**.
5. O sistema registra a entrada em `visita_portaria`, aciona a abertura da catraca e notifica o morador por push notification.

### 5.2 Entrada de Prestador de Serviço para Obras na Unidade
1. O morador cadastra em `Minha Unidade > Prestadores`: Nome, CPF, Empresa e dias permitidos (ex: segunda a sexta, 08h às 17h).
2. O prestador chega à guarita com ferramentas e documento.
3. O porteiro pesquisa pelo CPF do prestador, confirma a autorização da unidade, tira uma foto rápida na webcam da guarita e entrega um crachá de visitante.
4. Ao final do expediente, o porteiro escaneia o crachá devolvido e clica em **"Registrar Saída"**.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-013](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-013-organizacao-diretorios.md), visitantes, hóspedes e prestadores utilizam a mesma mecânica operacional e tabelas (`pessoa` e `visita_portaria`), variando apenas o atributo de classificação (`tipo_visitante = 'VISITANTE' | 'PRESTADOR' | 'HOSPEDE'`).
- **RN-02:** Nenhuma pessoa não residente ingressa no condomínio sem que haja o registro da unidade de destino e a identificação do morador que autorizou a entrada.
- **RN-03:** Prestadores de serviços não podem ingressar fora dos horários permitidos pelo regimento interno (salvo chamados de emergência hidráulica/elétrica autorizados expressamente pelo síndico).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/portaria/`)
- `POST /api/v1/portaria/atendimento/convites`: Morador emite novo convite prévio.
- `GET /api/v1/portaria/atendimento/presentes`: Painel em tempo real de quem está no prédio.
- `POST /api/v1/portaria/atendimento/check-in`: Registro de entrada de visitante/prestador.
- `POST /api/v1/portaria/atendimento/check-out`: Registro de saída.

### Frontend Angular (PWA)
- Componente: `features/portaria/components/terminal-atendimento` (otimizado para teclado numérico e leitor de código de barras USB).

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `visita.chegada` | Morador da unidade | Push Urgente | "Seu visitante Carlos Silva acabou de dar entrada na portaria." |
| `visita.aguardando` | Morador da unidade | Push + Chamada | "Visitante na guarita aguardando sua autorização para subir." |
