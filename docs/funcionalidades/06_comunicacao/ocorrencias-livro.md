# Livro de Ocorrências Unificado (Morador, Portaria e Gestão)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Livros pretos de papel na guarita onde moradores escrevem reclamações caluniosas visíveis a qualquer vizinho, desencontro de informações sobre barulho noturno e chamados perdidos sem prazo formal de atendimento ou resposta da gestão.
- **Proposta de Valor:** Centralizar em um livro digital único todas as ocorrências do condomínio, unificando registros feitos por moradores (reclamações de convivência, barulho, vazamentos), porteiros (irregularidades noturnas na portaria) e pelo síndico (notificações administrativas), com controle de sigilo, linha do tempo interativa e registro fotográfico/áudio.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `comunicacao` |
| **Subdomínio** | `ocorrencias` (consolidação unificada conforme ADR-013) |
| **Fase de Entrega** | Fase 1 (Fundação) |
| **Tabelas do Banco (pt-BR)** | `ocorrencia`, `evento_ocorrencia`, `anexo_ocorrencia`, `categoria_ocorrencia` |
| **Perfis com Acesso** | Morador (próprias/públicas), Porteiro (portaria), Zelador, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Abrir ocorrência de convivência / barulho | **Sim** | Se config | **Sim (portaria)** | **Sim** | **Sim** | **Sim** |
| Anexar fotos / vídeos / gravações de áudio | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** |
| Definir visibilidade (`SIGILOSA` vs `PUBLICA`) | **Sim** | — | **Sim** | — | **Sim** | **Sim** |
| Comentar na linha do tempo da ocorrência | Própria | — | Se atribuído | Se atribuído | **Todas** | **Todas** |
| Mudar status (tramitar atendimento) | — | — | — | Se atribuído | **Sim** | **Sim** |
| Aplicar advertência / multa formal decorrente | — | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Ocorrência

```text
[ABERTA] ──(triagem da gestão)──► [EM_ANALISE] ──(ação em curso)──► [EM_ANDAMENTO]
   │                                     │                                 │
   │                                     ├──(aguarda autor)                ├──(solução proposta)
   │                                     │   └──► [AGUARDANDO_MORADOR]     │   └──► [RESOLVIDA]
   │                                     │                                 │            │
   └──(cancelamento autor)──► [CANCELADA] └──(sem procedência)─────────────┴────────────┴──(aceite/prazo)──► [FECHADA]
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `ABERTA` | Recém-criada pelo morador ou porteiro; na fila de triagem. | Edição/cancelamento pelo autor. |
| `EM_ANALISE` | Síndico ou zelador tomou conhecimento e está avaliando. | Atribuir responsável ou classificar. |
| `EM_ANDAMENTO` | Providência prática sendo tomada (notificação ou vistoria). | Inserção de eventos na timeline. |
| `AGUARDANDO_MORADOR` | A gestão solicitou esclarecimento ou foto complementar. | Réplica e envio de anexo pelo morador. |
| `RESOLVIDA` | Providência concluída; aguardando validação do morador. | Morador aceita ou contesta. |
| `FECHADA` | Chamado encerrado definitivamente. | Consulta em arquivo histórico. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Registro de Ocorrência pelo Morador
1. O morador entra em `Atendimento > Nova Ocorrência`.
2. Informa:
   - **Origem:** Gerada automaticamente como `TIPO_ORIGEM = 'MORADOR'`.
   - **Categoria:** Barulho excessivo, Infiltração/Vazamento, Uso indevido de vaga, Desrespeito à convenção.
   - **Local:** Unidade causadora (se houver, ex: "Apt 52 Torre A") ou Área Comum.
   - **Nível de Sigilo:** `SIGILOSA` (apenas síndico e administradora visualizam os dados do autor) ou `PUBLICA_CONDOMINIO` (visível para a comunidade).
   - **Evidências:** Anexa áudio de gravação do ruído ou foto.
3. O sistema cria o registro, emite push para a gestão e abre a linha do tempo interativa.

### 5.2 Registro de Ocorrência pela Portaria (Livro da Guarita)
1. Durante a ronda noturna às 01h30, o porteiro constata som alto na piscina.
2. Acessa no terminal: `Ocorrências > Registrar Irregularidade`.
3. O sistema grava com `TIPO_ORIGEM = 'PORTARIA'` e o ID do porteiro de plantão.
4. O síndico recebe o alerta na manhã seguinte para emissão de notificação ou aplicação de multa conforme o regimento.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-013](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-013-organizacao-diretorios.md), o livro de ocorrências da portaria e os chamados do morador residem na mesma tabela unificada `ocorrencia`, diferenciados pela coluna `tipo_origem = 'PORTARIA' | 'MORADOR' | 'GESTAO'`.
- **RN-02:** Proteção anti-retaliação: Ocorrências marcadas como `SIGILOSA` ocultam o nome, unidade e dados do morador autor para qualquer vizinho ou terceiro denunciado.
- **RN-03:** Toda alteração de status ou mensagem gera um evento imutável em `evento_ocorrencia` com autor, carimbo de tempo e texto.
- **RN-04:** Uma ocorrência marcada como `RESOLVIDA` fecha automaticamente após 5 dias corridos caso o morador não apresente réplica.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/comunicacao/ocorrencias`)
- `GET /api/v1/comunicacao/ocorrencias`: Lista paginada com filtros por status, origem e sigilo.
- `POST /api/v1/comunicacao/ocorrencias`: Abertura de chamado com upload de anexos no S3.
- `POST /api/v1/comunicacao/ocorrencias/{id}/eventos`: Envio de comentário na linha do tempo.
- `PATCH /api/v1/comunicacao/ocorrencias/{id}/status`: Tramitação de status pela gestão.

### Frontend Angular (PWA)
- Componente: `features/comunicacao/components/livro-ocorrencias` e `timeline-atendimento`.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `ocorrencia.aberta` | Síndico | Push Urgente | "Nova ocorrência registrada pelo Morador da Unidade 31 Torre B (Barulho)." |
| `ocorrencia.respondida` | Morador autor | Push + E-mail | "A gestão respondeu sua ocorrência #104: 'Notificação enviada ao morador'." |
