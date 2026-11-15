# Assembleias Gerais Virtuais e Híbridas (Votação Digital e Atas)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Baixa adesão e falta de quórum em assembleias presenciais noturnas, conflitos acalorados entre vizinhos, dificuldade na coleta e validação manual de procurações em papel, e demora de semanas para redigir, assinar e registrar a ata final da reunião.
- **Proposta de Valor:** Plataforma completa para realização de assembleias virtuais, híbridas ou assíncronas com validade jurídica (Lei 14.309/2022), contemplando publicação de edital de convocação, validação digital de procurações, apuração automatizada com cálculo por fração ideal ou por unidade, votação secreta/aberta auditável e geração da minuta da ata em tempo real.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `governanca` |
| **Subdomínio** | `assembleias` |
| **Fase de Entrega** | Fase 3 (Governança e Serviços) |
| **Tabelas do Banco (pt-BR)** | `assembleia`, `pauta_assembleia`, `voto_assembleia`, `procuracao_assembleia`, `ata_assembleia` |
| **Perfis com Acesso** | Moradores adimplentes (votam), Síndico (preside/convoca), Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador (Titular) | Morador Inadimplente | Procurador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Cadastrar edital de convocação e pautas | — | — | — | **Sim** | **Sim** |
| Anexar procuração com assinatura digital | **Sim** | — | **Sim** | **Sim** | **Sim** |
| Assinar lista de presença virtual | **Sim** | Apenas ouvinte | **Sim** | **Sim** | **Sim** |
| Votar nas pautas deliberativas | **Sim** | Bloqueado por lei | **Sim** | **Sim** | — |
| Acompanhar transmissão ao vivo e chat | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** |
| Encerrar votação e gerar minuta da ata | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Assembleia

```text
[CONVOCADA] ──(data de início)──► [EM_ANDAMENTO] ──(abertura de pautas)──► [EM_VOTACAO]
     │                                                                           │
     ├──(cancelamento formal)──► [CANCELADA]                                     ├──(encerramento de pautas)
     │                                                                           ▼
     └──(suspensão por falta de quórum)──► [SUSPENSA_SESSAO_PERMANENTE] ──► [CONCLUIDA_AGUARDANDO_ATA] ──► [REGISTRADA]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Convocação e Envio de Procuração
1. A gestão cadastra a assembleia no sistema:
   - Tipo: Ordinária (prestação de contas / eleição) ou Extraordinária (obras).
   - Modalidade: Virtual (100% online) ou Híbrida.
   - Pautas numeradas com opções de votação (ex: *Pauta 1: Aprovação da Previsão Orçamentária 2027*).
   - Link da videoconferência (Zoom/Google Meet/YouTube).
2. O sistema emite o edital por push notification, e-mail e disponibiliza no mural com antecedência legal mínima (conforme convenção).
3. Caso o titular não possa comparecer, ele anexa a procuração assinada digitalmente (Gov.br ou ICP-Brasil) indicando o procurador.

### 5.2 Votação Durante a Assembleia
1. O presidente da mesa abre a votação da **Pauta 1**.
2. A tela do app dos moradores adimplentes presentes exibe as opções: `A FAVOR`, `CONTRA` ou `ABSTENÇÃO`.
3. O morador vota. O sistema valida se a unidade está quite com a taxa condominial (art. 1.335, III do Código Civil).
4. O voto é computado ponderando o peso da fração ideal da unidade (ou voto paritário por unidade, conforme convenção).
5. Ao fechar a pauta, o resultado matemático é auditado e exibido na tela da transmissão.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o art. 1.335, III do Código Civil, moradores em inadimplência com a taxa condominial possuem direito de assistir e manifestar-se (se não houver proibição na convenção), mas são **bloqueados de votar e de ser votados**.
- **RN-02:** O cálculo do resultado da deliberação respeita rigorosamente o tipo de quórum exigido por lei para o tema:
  - Maioria simples dos presentes (contas, orçamento anual).
  - Maioria absoluta de todos os condôminos (alteração de regimento).
  - Dois terços de todos os condôminos (obras voluptuárias, alteração de convenção).
  - Unanimidade (mudança de destinação do edifício).
- **RN-03:** Cada procuração deve ser validada e aprovada pela mesa diretora antes da liberação do poder de voto do representante.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/governanca/assembleias`)
- `POST /api/v1/governanca/assembleias`: Criação de assembleia e pautas.
- `GET /api/v1/governanca/assembleias/{id}/presenca`: Registro de presença digital.
- `POST /api/v1/governanca/assembleias/{id}/pautas/{pauta_id}/voto`: Envio de voto auditável.
- `GET /api/v1/governanca/assembleias/{id}/ata`: Geração da minuta de ata em PDF com assinaturas digitais.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `assembleia.convocacao` | Todos os Moradores | Push + E-mail Oficial | "Edital de Convocação: Assembleia Geral Ordinária em 10/12 às 19h30." |
| `assembleia.pauta_aberta` | Presentes na reunião | Push em Tempo Real | "VOTAÇÃO ABERTA: Pauta 2 liberada para votação agora no app." |
