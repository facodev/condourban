# Prestação de Contas Digital, Balancetes e Gestão de Despesas

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Falta de transparência na aplicação dos recursos do condomínio, desconfiança de desvios, balancetes impressos incompreensíveis e dificuldade do conselho fiscal em analisar notas fiscais e comprovantes de despesas bancárias.
- **Proposta de Valor:** Transformar a prestação de contas em um painel digital intuitivo e interativo, onde moradores visualizam gráficos claros de receitas e despesas por categoria (água, luz, funcionários, contratos), acessam cópias digitalizadas de notas fiscais e comprovantes de pagamento, e o conselho fiscal emite pareceres formais diretamente no sistema.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `financeiro` |
| **Subdomínio** | `prestacao_contas` e `despesas` |
| **Fase de Entrega** | Fase 4 (Financeiro) |
| **Tabelas do Banco (pt-BR)** | `balancete_mensal`, `lancamento_financeiro`, `categoria_financeira`, `parecer_conselho_fiscal` |
| **Perfis com Acesso** | Todos os moradores (leitura dos balancetes aprovados), Síndico, Conselho, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Conselho Fiscal | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Consultar balancetes e gráficos de despesas | **Sim** | **Sim** | — | **Sim** | **Sim** |
| Visualizar notas fiscais e comprovantes | **Sim** | **Sim** | — | **Sim** | **Sim** |
| Lançar despesa com nota fiscal anexada | — | — | — | **Sim** | **Sim** |
| Emitir parecer formal sobre o mês contábil | — | **Sim** | — | — | — |
| Fechar e publicar competência mensal | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados do Balancete Mensal

```text
[EM_LANCAMENTO] ──(fechamento contábil)──► [AGUARDANDO_CONSELHO] ──(parecer favorável)──► [PUBLICADO]
                                                    │
                                                    └──(ressalvas/dúvidas)──► [COM_RESSALVAS]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Consulta pelo Morador no App
1. O morador entra em `Financeiro > Prestação de Contas`.
2. Visualiza o resumo do mês anterior:
   - Total Arrecadado: R$ 85.400,00
   - Total de Despesas: R$ 78.200,00
   - Saldo em Fundo de Reserva: R$ 142.000,00
3. Um gráfico de rosca ilustra a distribuição: Folha (45%), Concessionárias (25%), Manutenções (18%), Outros (12%).
4. O morador clica na despesa *"Manutenção dos Elevadores — R$ 2.450,00"* e pode abrir o PDF da nota fiscal emitida pela fabricante com o comprovante de transferência bancária.

### 5.2 Análise e Parecer do Conselho Fiscal
1. Ao final do mês, os membros eleitos do conselho fiscal recebem notificação para conferência da pasta digital.
2. Analisam os lançamentos e anexam o **Parecer do Conselho Fiscal**: `FAVORÁVEL`, `FAVORÁVEL COM RESSALVAS` ou `DESFAVORÁVEL`.
3. O balancete com o parecer é publicado automaticamente no repositório de documentos do condomínio.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Notas fiscais e comprovantes bancários são acessíveis exclusivamente aos membros e proprietários vinculados ao respectivo condomínio.
- **RN-02:** Um balancete com status `PUBLICADO` é congelado como imutável: qualquer retificação contábil posterior exige estorno documentado e registro em ata.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/financeiro/`)
- `GET /api/v1/financeiro/prestacao-contas/balancetes`: Lista de balancetes mensais.
- `GET /api/v1/financeiro/prestacao-contas/balancetes/{competencia}/detalhes`: Itens de receitas e despesas.
- `POST /api/v1/financeiro/prestacao-contas/conselho/parecer`: Envio do parecer assinado digitalmente.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `balancete.publicado` | Todos os Moradores | Push + In-app | "Prestação de contas de Outubro/2026 já está disponível para consulta no app." |
| `conselho.solicitacao_parecer` | Membros do Conselho | E-mail + Push | "A pasta de prestação de contas de Outubro aguarda sua análise e parecer." |
