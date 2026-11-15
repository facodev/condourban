# Cobrança Condominial e Emissão de Boletos / Pix

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Moradores perdendo prazos de pagamento por falta de entrega de boletos em papel, taxas abusivas de emissão bancária tradicional e morosidade na identificação e conciliação de pagamentos manuais.
- **Proposta de Valor:** Centralizar a visualização das cotas condominiais ordinárias e extraordinárias diretamente no aplicativo móvel/PWA, oferecendo linha digitável, emissão de PDF da 2ª via atualizada com encargos e geração de **Pix Dinâmico (QR Code / Copia e Cola)** com conciliação bancária instantânea.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `financeiro` |
| **Subdomínio** | `cobrancas` e `faturamento` |
| **Fase de Entrega** | Fase 4 (Módulo Financeiro Completo) |
| **Tabelas do Banco (pt-BR)** | `cobranca_condominial`, `item_cobranca`, `pagamento_cobranca`, `webhook_gateway` |
| **Perfis com Acesso** | Morador (próprias faturas), Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador (Titular) | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Visualizar boletos e Pix da própria unidade | **Sim** | Se config | — | — | Sim (próprio) | — |
| Copiar código Pix / Linha digitável | **Sim** | Se config | — | — | Sim (próprio) | — |
| Baixar 2ª via em PDF atualizada | **Sim** | — | — | — | Sim (próprio) | — |
| Gerar faturamento mensal do condomínio | — | — | — | — | Aprova | **Sim** |
| Baixa manual de pagamento em dinheiro/cheque | — | — | — | — | **Sim** | **Sim** |
| Consultar painel geral de arrecadação | — | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Cobrança

```text
[GERADA] ──(vencimento sem pagamento)──► [VENCIDA] ──(acordo firmado)──► [EM_ACORDO]
   │                                           │                                │
   ├──(pagamento via Pix/Boleto)───────────────┴──(compensação)─────────────────┴──► [PAGA]
   │
   └──(cancelamento / erro de rateio)──► [CANCELADA]
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `GERADA` | Cota condominial emitida com código de barras e Pix ativos. | Pagamento e download pelo morador. |
| `VENCIDA` | Prazo limite expirado; incidem juros e multa conforme convenção. | Geração de 2ª via recalculada. |
| `EM_ACORDO` | Débito renegociado em parcelamento formal. | Cumprimento das parcelas acordadas. |
| `PAGA` | Liquidação confirmada via webhook bancário ou baixa manual. | Download do comprovante de quitação. |
| `CANCELADA` | Boleto anulado por retificação de rateio ou duplicidade. | Consulta apenas em auditoria. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Pagamento Instantâneo via Pix Dinâmico pelo Morador
1. O morador abre o app e vê o card no dashboard: *"Cota Condominial de Novembro — R$ 680,00 — Vence em 10/11"*.
2. Clica em **"Pagar com Pix"**.
3. O app exibe o QR Code Pix e o botão **"Copiar Chave Copia e Cola"**.
4. O morador cola no aplicativo do seu banco e confirma o pagamento.
5. Em menos de 5 segundos, a instituição bancária emite um webhook para a API FastAPI.
6. A API valida a assinatura do webhook, identifica a cobrança em `cobranca_condominial`, liquida o título e altera o status para `PAGA`.
7. O morador recebe notificação push imediata: *"Pagamento recebido com sucesso! Sua unidade está em dia."*

### 5.2 Emissão de 2ª Via Recalculada de Boleto Vencido
1. Caso o morador não tenha pago até o vencimento, o status passa a `VENCIDA`.
2. Ao acessar a fatura, o sistema aplica automaticamente a multa de 2% e juros de 1% ao mês (pro-rata die) conforme o Código Civil.
3. O morador clica em **"Gerar 2ª Via Atualizada"**, emitindo novo boleto registrado com validade para o mesmo dia.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o Código Civil brasileiro, a multa por atraso no pagamento da cota condominial é limitada estritamente ao teto legal de 2% sobre o valor principal, acrescida de juros de 1% ao mês.
- **RN-02:** Nenhum boleto é emitido sem o registro prévio na CIP (Câmara Interbancária de Pagamentos) via API do gateway bancário homologado.
- **RN-03:** Todas as baixas manuais exigem anexo do comprovante de depósito e justificativa textual gravada na trilha de auditoria.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/financeiro/`)
- `GET /api/v1/financeiro/cobrancas/unidade`: Lista débitos e faturas da unidade do usuário.
- `GET /api/v1/financeiro/cobrancas/{id}/pix`: Retorna payload Copia e Cola e QR Code em Base64.
- `GET /api/v1/financeiro/cobrancas/{id}/boleto-pdf`: Download do PDF oficial com código de barras.
- `POST /api/v1/financeiro/webhooks/banco`: Webhook de retorno e conciliação bancária (idempotente).

### Frontend Angular (PWA)
- Componente: `features/financeiro/components/minhas-cobrancas` e `segunda-via-modal`.
- Pipe compartilhado: `moeda.pipe.ts` para formatação precisa em BRL (`R$ 1.250,00`).

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `boleto.disponivel` | Morador titular | Push + E-mail | "A fatura do condomínio com vencimento em 10/11 já está disponível." |
| `pagamento.confirmado` | Morador titular | Push | "Confirmamos o pagamento da sua taxa de condomínio via Pix. Obrigado!" |
