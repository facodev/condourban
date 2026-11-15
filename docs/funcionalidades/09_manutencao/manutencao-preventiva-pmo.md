# Plano de Manutenção Preventiva Obrigatória (PMO) e Vistorias Prediais

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Síndicos respondendo civil e criminalmente por acidentes prediais (quedas de elevadores, incêndios por extintores vencidos, contaminação de água por falta de limpeza de caixas ou queima de motores de bombas por falta de graxa) devido à ausência de controle cronológico de manutenções periódicas obrigatórias (NBR 5674).
- **Proposta de Valor:** Calendário automatizado do Plano de Manutenção Obrigatória (PMO), programando inspeções preventivas diárias, semanais, mensais e anuais, alertando a gestão com antecedência e arquivando laudos técnicos e certificados com validade jurídica.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `manutencao` |
| **Subdomínio** | `preventiva` e `equipamentos` |
| **Fase de Entrega** | Fase 3 (Governança e Serviços) |
| **Tabelas do Banco (pt-BR)** | `plano_manutencao_preventiva`, `equipamento_predial`, `execucao_preventiva`, `certificado_laudo` |
| **Perfis com Acesso** | Zelador (executa checklists), Síndico, Administradora, Prestador Técnico credenciado |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Cadastrar equipamentos (gerador, bombas, elevador) | — | — | — | **Sim** | **Sim** |
| Configurar rotinas preventivas com periodicidade | — | — | — | **Sim** | **Sim** |
| Executar checklist de inspeção de rotina no app | — | — | **Sim** | **Sim** | — |
| Fazer upload de laudos técnicos (ART/RRT) | — | — | — | **Sim** | **Sim** |
| Acompanhar painel de conformidade e vencimentos | — | — | **Sim** | **Sim** | **Sim** |

---

## 4. Equipamentos e Itens Críticos do PMO

| Item / Equipamento | Periodicidade | Exigência Legal / Norma | Responsável Típico |
| :--- | :--- | :--- | :--- |
| **Limpeza de Caixas d'Água** | Semestral | Portaria de Saúde Pública | Empresa Especializada |
| **Recarga de Extintores e Mangueiras** | Anual | Corpo de Bombeiros / AVCB | Empresa Homologada |
| **Inspeção de Elevadores** | Mensal | RIA / Norma Técnica ABNT | Empresa Fabricante/Conservadora |
| **Teste de Grupo Gerador** | Semanal | NBR 5674 | Zelador do condomínio |
| **Limpeza da Caixa de Gordura** | Trimestral | Ambiental / Sanitária | Zelador ou Limpa-Fossa |
| **Laudo do SPDA (Para-raios)** | Anual | NBR 5419 | Engenheiro Eletricista com ART |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Alerta Automático e Agendamento
1. O cronômetro do sistema detecta que a recarga anual dos extintores vencerá em 30 dias.
2. A API emite notificação automática para o síndico e insere a pendência em destaque no dashboard.
3. O síndico contrata a empresa homologada e agenda o serviço para o dia 12.

### 5.2 Execução e Encerramento com Laudo Técnico
1. Os técnicos realizam o teste hidrostático e a recarga dos extintores.
2. O zelador inspeciona a entrega, anexa a foto do novo selo do INMETRO e faz o upload da nota fiscal e do certificado de recarga (.PDF).
3. O sistema calcula automaticamente a nova data de vencimento (+365 dias) e atualiza o indicador de conformidade do prédio para `100% REGULAR`.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Laudos técnicos de manutenções de alta complexidade (elevadores, geradores, bombas de recalque, para-raios) exigem obrigatoriamente anotação da Anotação de Responsabilidade Técnica (ART) ou Registro de Responsabilidade Técnica (RRT) com o número do CREA/CAU do engenheiro responsável.
- **RN-02:** O atraso de qualquer rotina crítica obrigatória altera o indicador de conformidade geral do condomínio para `ALERTA VERMELHO`.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/manutencao/preventiva`)
- `GET /api/v1/manutencao/preventiva/cronograma`: Calendário anual de intervenções.
- `POST /api/v1/manutencao/preventiva/execucoes`: Registro de checklist executado com anexos.
- `GET /api/v1/manutencao/preventiva/indicadores`: Índice de conformidade predial.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `pmo.item_vencendo` | Síndico e Zelador | Push + E-mail | "Atenção: A limpeza semestral das caixas d'água vence em 15 dias." |
| `pmo.rotina_semanal` | Zelador | Push Semanal | "Rotina da Segunda-feira: Testar partida do grupo gerador e anotar nível de diesel." |
