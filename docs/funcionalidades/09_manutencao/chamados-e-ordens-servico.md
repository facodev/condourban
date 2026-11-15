# Chamados de Manutenção Corretiva e Ordens de Serviço (OS)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Lâmpadas queimadas nos corredores, vazamentos em garagens ou portões com defeito são relatados verbalmente ao zelador e caem no esquecimento; síndicos não conseguem medir o tempo de atendimento da equipe de manutenção nem comprovar custos de peças e reparos.
- **Proposta de Valor:** Transformar solicitações de reparo em Ordens de Serviço (OS) digitais e estruturadas, permitindo triagem pelo síndico, atribuição ao zelador ou prestador terceirizado, registro de fotos antes/depois e controle de custos de materiais e mão de obra.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `manutencao` |
| **Subdomínio** | `chamados` e `ordens_servico` |
| **Fase de Entrega** | Fase 3 (Governança e Serviços) |
| **Tabelas do Banco (pt-BR)** | `chamado_manutencao`, `ordem_servico`, `anexo_manutencao`, `custo_manutencao` |
| **Perfis com Acesso** | Morador (abre chamado), Zelador (executa), Síndico (aprova e atribui) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Reportar problema predial na área comum | **Sim** | **Sim** | **Sim** | **Sim** | — |
| Converter chamado em Ordem de Serviço (OS) | — | — | — | **Sim** | **Sim** |
| Atribuir OS ao zelador ou fornecedor terceirizado | — | — | — | **Sim** | **Sim** |
| Registrar fotos do reparo concluído | — | — | **Sim** | **Sim** | — |
| Aprovar conclusão e dar baixa na OS | — | — | — | **Sim** | **Sim** |
| Lançar custos de peças e materiais | — | — | **Sim** | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Ordem de Serviço

```text
[CHAMADO_ABERTO] ──(triagem do síndico)──► [OS_GERADA] ──(atribuição)──► [EM_EXECUCAO]
       │                                                                       │
       └──(duplicado/inviável)──► [RECUSADO]                                  ├──(aguardando peça)──► [AGUARDANDO_MATERIAL]
                                                                               │
                                                                               └──(zelador conclui)──► [CONCLUIDA] ──(validação)──► [ENCERRADA]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Abertura de Chamado pelo Morador ou Porteiro
1. O morador nota uma lâmpada piscando no hall do 4º andar do Bloco A.
2. Abre o app em `Manutenção > Reportar Problema`.
3. Tira uma foto do local, seleciona a categoria *"Elétrica / Iluminação"* e digita breve descrição.
4. O chamado é registrado em `chamado_manutencao` com status `CHAMADO_ABERTO`.

### 5.2 Emissão e Execução da OS pelo Zelador
1. O síndico abre o painel web, revisa o chamado e clica em **"Gerar Ordem de Serviço"**.
2. Atribui a tarefa ao zelador com prioridade `NORMAL`.
3. O zelador recebe notificação no celular, troca o reator e a lâmpada.
4. Pelo app, o zelador tira uma foto do serviço concluído, anexa o custo da lâmpada (R$ 22,00 do almoxarifado) e clica em **"Concluir OS"**.
5. O morador que abriu o chamado recebe notificação com a foto do reparo feito.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Chamados classificados como emergência (ex: vazamento de gás, curto-circuito, elevador travado com passageiro) disparam notificações em modo urgente e com alerta sonoro para o zelador e síndico.
- **RN-02:** A conclusão de qualquer OS corretiva exige obrigatoriamente a anexação de pelo menos uma foto comprobatória do reparo executado.
- **RN-03:** Despesas de materiais que excedam a alçada autorizada do zelador exigem aprovação prévia do síndico antes da compra.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/manutencao/`)
- `POST /api/v1/manutencao/chamados`: Abertura de chamado de manutenção.
- `POST /api/v1/manutencao/chamados/{id}/gerar-os`: Conversão em Ordem de Serviço.
- `PATCH /api/v1/manutencao/ordens-servico/{id}/concluir`: Conclusão com foto e custos.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `manutencao.os_atribuida` | Zelador | Push | "Nova OS atribuída a você: Troca de iluminação Bloco A (Hall 4º andar)." |
| `chamado.concluido` | Morador solicitante | Push + In-app | "Seu chamado sobre a iluminação do 4º andar foi concluído pelo zelador!" |
