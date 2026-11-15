# Bounded Context: Financeiro e Tarifação (`financeiro`)

Este bounded context é o núcleo de gestão orçamentária, geração de receitas condominiais, liquidação de pagamentos, cobrança de inadimplência e rateio por medições de consumo individualizado.

---

## 1. Responsabilidade do Domínio

- **Emissão de Boletos e Pix**: Geração automatizada da taxa condominial mensal (ordinária e extraordinária), emissão de 2ª via de boleto bancário (PDF e linha digitável) e cobrança instantânea via Pix Copia e Cola / QR Code dinâmico.
- **Conciliação e Baixa de Pagamentos**: Processamento de arquivos bancários CNAB 240/400 ou webhooks de gateways de pagamento para baixa automática e reconciliação financeira.
- **Acordos e Inadimplência**: Painel de unidades devedoras, cálculo automático de juros, multas e correção monetária, e celebração de termos de renegociação/parcelamento de dívidas.
- **Medições Individuais de Consumo**: Leitura periódica e tarifação individualizada por unidade para água, gás encanado e energia (onde houver telemetria ou leitura manual).
- **Prestação de Contas e Balancetes**: Publicação de balancetes mensais, gráficos de receitas vs. despesas e demonstrativo para a comissão fiscal e condôminos.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/financeiro/`)
```text
financeiro/
├── __init__.py
├── router.py
├── cobrancas_acordos/     # Boletos, Pix, conciliação e renegociações
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── despesas_medicoes/     # Prestação de contas e medições individuais (água/gás)
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/financeiro/`)
```text
financeiro/
├── components/
│   ├── cobrancas-acordos/ # Emissão de 2ª via, Pix e acordos de pagamento
│   └── despesas-medicoes/ # Balancetes e gráficos de consumo individual
├── services/
│   └── financeiro.service.ts
└── financeiro.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `cobranca_condominial`: Cobrança mensal da unidade (`id`, `condominio_id`, `unidade_id`, `mes_referencia`, `ano_referencia`, `data_vencimento`, `valor_nominal`, `valor_multa`, `valor_juros`, `valor_total`, `status`: `pendente`, `pago`, `atrasado`, `cancelado`, `codigo_barras`, `pix_copia_cola`, `nosso_numero`, `pago_em`).
- `acordo_inadimplencia`: Renegociação de débitos (`id`, `unidade_id`, `valor_total_consolidado`, `quantidade_parcelas`, `status`: `ativo`, `cumprido`, `rompido`, `criado_em`).
- `parcela_acordo`: Parcela do acordo (`id`, `acordo_id`, `numero_parcela`, `vencimento`, `valor`, `status`).
- `medicao_individual_consumo`: Telemetria e consumo (`id`, `unidade_id`, `tipo`: `agua`, `gas`, `energia`, `leitura_anterior`, `leitura_atual`, `consumo_apurado`, `mes_referencia`, `data_leitura`).
- `balancete_financeiro`: Demonstrativo de prestação de contas (`id`, `condominio_id`, `mes_referencia`, `ano_referencia`, `total_receitas`, `total_despesas`, `saldo_atual`, `arquivo_pdf_url`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/financeiro/cobrancas` | Listagem de cobranças da unidade logada ou do condomínio |
| `GET` | `/api/v1/financeiro/cobrancas/{id}/pix` | Geração/obtenção do QR Code e Pix Copia e Cola |
| `GET` | `/api/v1/financeiro/cobrancas/{id}/boleto` | Download do boleto em PDF |
| `POST` | `/api/v1/financeiro/cobrancas/gerar-lote` | Geração em lote das cobranças do mês vigente |
| `GET` | `/api/v1/financeiro/medicoes` | Histórico e gráficos de consumo por unidade |
| `POST` | `/api/v1/financeiro/medicoes` | Lançamento de leituras de água ou gás |
| `GET` | `/api/v1/financeiro/balancetes` | Balancetes e prestação de contas |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-011: Planos e Funcionalidades SaaS](../../decisoes/ADR-011-planos-e-funcionalidades.md)
  - [ADR-010: Nomenclatura em pt-BR](../../decisoes/ADR-010-nomenclatura-pt-br.md)
- **Especificações Funcionais**:
  - [cobranca-e-boletos.md](cobranca-e-boletos.md)
  - [prestacao-contas-e-despesas.md](prestacao-contas-e-despesas.md)
  - [acordos-e-inadimplencia.md](acordos-e-inadimplencia.md)
  - [planos-e-entitlements.md](../10_transversal_plataforma/planos-e-entitlements.md)
- **Scripts SQL**:
  - [009-financeiro.sql](../../sql/009-financeiro.sql) (`cobranca_condominial`, `despesa_condominial`, `termo_acordo`, `medicao_individual`)
  - [013-saas-planos-e-funcionalidades.sql](../../sql/013-saas-planos-e-funcionalidades.sql) (`assinatura`, `plano`, `funcionalidade`)
