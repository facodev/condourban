# Gestão de Acordos de Cobrança e Inadimplência

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Índices elevados de inadimplência que asfixiam o fluxo de caixa do condomínio, desgaste emocional e atritos diretos entre o síndico e moradores devedores, e dificuldade de formalizar e acompanhar parcelamentos de dívidas antigas.
- **Proposta de Valor:** Automatizar a régua de cobrança preventiva e amigável, permitindo ao condômino inadimplente simular e firmar acordos de parcelamento de débitos diretamente no aplicativo, com geração automática dos termos jurídicos e boletos das parcelas mensais.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `financeiro` |
| **Subdomínio** | `acordos` e `inadimplencia` |
| **Fase de Entrega** | Fase 4 (Financeiro) |
| **Tabelas do Banco (pt-BR)** | `acordo_cobranca`, `parcela_acordo`, `historico_inadimplencia` |
| **Perfis com Acesso** | Morador titular (própria dívida), Síndico, Administradora, Jurídico |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador (Inadimplente) | Síndico | Administradora | Jurídico / Cobrança |
| :--- | :---: | :---: | :---: | :---: |
| Simular parcelamento de débitos | **Sim** | **Sim** | **Sim** | **Sim** |
| Propor e assinar Termo de Acordo | **Sim** | **Sim** | **Sim** | **Sim** |
| Homologar acordo financeiro | — | **Sim** | **Sim** | **Sim** |
| Cancelar acordo por quebra de parcela | — | **Sim** | **Sim** | **Sim** |
| Consultar taxa global de inadimplência | — | **Sim** | **Sim** | **Sim** |

---

## 4. Máquina de Estados do Acordo de Cobrança

```text
[PROPOSTA_CRIADA] ──(aceite e assinatura)──► [VIGENTE] ──(todas parcelas quitadas)──► [QUITADO]
        │                                        │
        └──(rejeição/expiração)──► [CANCELADO]   └──(atraso de parcela > 30 dias)──► [QUEBRADO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Simulação e Assinatura de Acordo pelo Morador
1. O morador com 3 cotas em atraso acessa `Financeiro > Regularizar Pendências`.
2. O app consolida o débito total com encargos: R$ 2.400,00.
3. O morador escolhe a forma de parcelamento dentro das regras permitidas pelo condomínio:
   - Entrada de R$ 600,00 + 6 parcelas mensais de R$ 300,00.
4. O app gera a minuta do **Termo de Confissão e Parcelamento de Dívida**.
5. O morador assina digitalmente no app e efetua o pagamento imediato do Pix da entrada.
6. O status do acordo passa para `VIGENTE` e a unidade recupera a adimplência condicional.

### 5.2 Quebra de Acordo por Inadimplência
1. Caso o morador atrase uma parcela do acordo por mais de 30 dias, o sistema emite notificação de quebra de acordo.
2. O status muda para `QUEBRADO`, a dívida remanescente é antecipada integralmente e o caso é direcionado para a cobrança jurídica/judicial.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O acordo firmado só ganha vigência jurídica e suspende medidas de cobrança após a efetiva compensação bancária do pagamento da entrada.
- **RN-02:** O atraso no pagamento de qualquer parcela por período superior ao previsto na convenção acarreta o vencimento antecipado das parcelas vincendas e a incidência das penalidades originais.
- **RN-03:** Em respeito à dignidade e à LGPD, a lista nominal de condôminos inadimplentes é de acesso estritamente restrito ao síndico, conselho e administradora (nunca divulgada no mural público do condomínio).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/financeiro/acordos`)
- `GET /api/v1/financeiro/acordos/simular`: Cálculo de cenários de parcelamento.
- `POST /api/v1/financeiro/acordos`: Criação formal do termo com assinatura digital.
- `GET /api/v1/financeiro/acordos/{id}/parcelas`: Listagem de boletos do parcelamento.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `acordo.firmado` | Morador titular | E-mail + Push | "Acordo de regularização de débitos firmado com sucesso. Veja o cronograma de parcelas." |
| `parcela.vencendo` | Morador titular | Push (3 dias antes) | "Lembrete: A parcela 2 do seu acordo financeiro vence em 3 dias." |
