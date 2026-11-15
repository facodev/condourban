# Mural de Comunicados e Avisos Oficiais

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Papéis impressos colados nos elevadores que rasgam ou passam despercebidos, falta de comprovação jurídica de que os moradores foram devidamente avisados sobre obras, cortes de água programados ou manutenções e excesso de ruído em grupos informais de mensagens.
- **Proposta de Valor:** Canal oficial e institucional de comunicação da gestão do condomínio com os moradores, permitindo publicação de avisos segmentados por torre/bloco, categorização por urgência, anexação de documentos PDF e auditoria com confirmação obrigatória de leitura na tela do app.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `comunicacao` |
| **Subdomínio** | `comunicados` |
| **Fase de Entrega** | Fase 1 (Fundação) |
| **Tabelas do Banco (pt-BR)** | `comunicado`, `leitura_comunicado`, `anexo_comunicado` |
| **Perfis com Acesso** | Síndico, Administradora (publicam); Morador, Porteiro, Zelador (leitura) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Publicar comunicado oficial | — | — | — | **Sim** | **Sim** |
| Marcar comunicado como Urgente | — | — | — | **Sim** | **Sim** |
| Fixar comunicado no topo do mural | — | — | — | **Sim** | **Sim** |
| Segmentar por Bloco ou Torre | — | — | — | **Sim** | **Sim** |
| Visualizar relatórios de leitura (% lido) | — | — | — | **Sim** | **Sim** |
| Confirmar leitura no app | **Sim** | **Sim** | **Sim** | — | — |

---

## 4. Classificação e Níveis de Urgência

| Nível de Urgência | Comportamento no App | Exemplo de Uso |
| :--- | :--- | :--- |
| `INFORMATIVO` | Notificação silenciosa padrão no feed; card cinza/azul. | Manutenção de rotina nos jardins, troca de lâmpadas. |
| `IMPORTANTE` | Push notification com som padrão; destaque amarelo. | Dedetização das áreas comuns, limpeza de caixas d'água. |
| `URGENTE` | Modal bloqueante em tela cheia com pop-up imediato; alerta sonoro. | Rompimento de cano mestre, falta de energia geral, incêndio. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Publicação de Comunicado pelo Síndico
1. O síndico acessa `Comunicação > Novo Comunicado`.
2. Digita:
   - **Título:** Ex: *"Interrupção Programada do Fornecimento de Água"*.
   - **Conteúdo formatado:** Detalhes de data, horários e orientações aos moradores.
   - **Público-alvo:** `TODOS_OS_BLOCOS` ou apenas `TORRE_B`.
   - **Urgência:** `IMPORTANTE`.
   - **Exigir Confirmação de Leitura:** Sim.
   - **Anexos:** Documento oficial da concessionária de água (.PDF).
3. Clica em **"Publicar e Notificar"**.
4. O backend FastAPI grava em `comunicado` e enfileira tarefa no Celery para disparo de push notifications para todos os dispositivos dos moradores do público selecionado.

### 5.2 Leitura e Confirmação pelo Morador
1. O morador recebe o push e clica na notificação.
2. O app abre o comunicado com destaque visual.
3. Se marcado com confirmação obrigatória, exibe o botão **"Confirmo que Li este Comunicado"**.
4. Ao clicar, grava em `leitura_comunicado` com timestamp e ID do usuário.
5. O painel do síndico atualiza em tempo real: *"184 de 220 unidades (83%) confirmaram a leitura"*.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Comunicados publicados por moradores não são permitidos; o canal é estritamente unidirecional da gestão para o condomínio (interações de moradores ocorrem em [ocorrencias-livro.md](ocorrencias-livro.md) ou [canal-fale-conosco.md](canal-fale-conosco.md)).
- **RN-02:** Comunicados com flag `URGENTE` exigem confirmação explícita de leitura para desbloquear a navegação das demais telas do aplicativo.
- **RN-03:** A exclusão de um comunicado com confirmações de leitura já registradas mantém o histórico em auditoria para resguardo legal da gestão.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/comunicacao/`)
- `GET /api/v1/comunicacao/comunicados`: Mural paginado filtrado pela unidade/bloco do usuário logado.
- `POST /api/v1/comunicacao/comunicados`: Criação de novo comunicado com upload de anexos no S3.
- `POST /api/v1/comunicacao/comunicados/{id}/confirmar-leitura`: Registro da confirmação de ciência.
- `GET /api/v1/comunicacao/comunicados/{id}/relatorio-leitura`: Métricas de engajamento para o síndico.

### Frontend Angular (PWA)
- Componente: `features/comunicacao/components/mural-comunicados` e modal de leitura obrigatória.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `comunicado.novo` | Moradores elegíveis | Push PWA + E-mail | "Aviso da Administração: Interrupção Programada do Fornecimento de Água." |
| `comunicado.urgente` | Todos do condomínio | Push Urgente (High Priority) | "URGENTE: Manutenção emergencial no sistema elétrico agora." |
