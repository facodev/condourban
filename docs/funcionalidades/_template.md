# [Nome da Funcionalidade]

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Qual atrito operacional ou dor cotidiana no condomínio esta funcionalidade resolve?
- **Proposta de Valor:** O que muda na rotina de moradores, porteiros, zeladores ou da administração?

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | (ex: `identidade_cadastro`, `condominio`, `portaria`, etc.) |
| **Subdomínio** | (ex: `atendimento`, `agendamentos`, `ocorrencias`) |
| **Fase de Entrega** | (Fase 1: Fundação, Fase 2: Operação, Fase 3: Governança, Fase 4: Financeiro/Escala) |
| **Tabelas do Banco (pt-BR)** | (ex: `pessoa`, `visita_portaria`, `reserva_area_comum`) |
| **Perfis com Acesso** | (Morador, Dependente, Porteiro, Zelador, Síndico, Administradora, Admin Plataforma) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Criar / Registrar | Sim / Não | Sim / Não | Sim / Não | Sim / Não | Sim / Não | Sim / Não |
| Consultar / Visualizar | Próprio / Todos | Próprio | Todos | Todos | Todos | Todos |
| Atualizar / Tramitar | — | — | Sim / Não | Sim / Não | Sim | Sim |
| Cancelar / Excluir | Se aberto | — | — | — | Sim | Sim |

---

## 4. Máquina de Estados e Ciclo de Vida

```text
[ESTADO_INICIAL] ──(evento/ação)──► [ESTADO_INTERMEDIARIO] ──(conclusão)──► [ESTADO_TERMINAL]
                                           │
                                           └──(rejeição/cancelamento)──► [CANCELADO]
```

| Estado | Descrição e Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `RASCUNHO` / `PENDENTE` | Registro iniciado, aguardando validação ou envio. | Edição pelo autor. |
| `EM_PROCESSAMENTO` | Em análise pela administração ou em atendimento na portaria. | Atualização por operador/gestor. |
| `CONCLUIDO` / `APROVADO` | Fluxo finalizado com sucesso. | Leitura e consulta em histórico. |
| `REJEITADO` / `CANCELADO` | Operação recusada ou cancelada pelo autor/gestor. | Consulta do motivo no histórico. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Fluxo Principal (Caminho Feliz)
1. O usuário acessa a funcionalidade através do portal Angular correspondente ao seu perfil.
2. O frontend valida o formulário reativo e envia requisição autenticada para a API FastAPI.
3. A API valida o schema Pydantic, contexto de tenant (`condominio_id`) e executa a transação no SQLAlchemy.
4. O evento correspondente é registrado na trilha de auditoria e emitido para a fila Celery (quando assíncrono).
5. O sistema retorna o recurso criado com status `201 Created` e notifica os perfis interessados via push notification/e-mail.

### 5.2 Fluxos Alternativos
- **Fluxo A:** Consulta com filtros avançados e paginação.
- **Fluxo B:** Edição de dados antes da aprovação final.

### 5.3 Tratamento de Exceções e Erros
- **Falha de Conectividade:** Operação offline suportada pelo PWA com fila local de sincronização.
- **Conflito de Regra de Negócio:** Retorno `422 Unprocessable Entity` com mensagem clara e orientativa em português.
- **Acesso Não Autorizado:** Retorno `403 Forbidden` com código de erro específico (`FEATURE_DISABLED` ou `ROLE_UNAUTHORIZED`).

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Regra de validação primária.
- **RN-02:** Limites operacionais, cotas por unidade ou antecedência mínima/máxima.
- **RN-03:** Anti-abuso e regras de concorrência.
- **RN-04:** Critérios de impedimento (ex: bloqueio de reserva por convenção).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/...`)
- `GET /api/v1/{modulo}/{recurso}`: Listagem paginada com filtros.
- `POST /api/v1/{modulo}/{recurso}`: Criação do registro com validação Pydantic.
- `GET /api/v1/{modulo}/{recurso}/{id}`: Detalhes do registro.
- `PATCH /api/v1/{modulo}/{recurso}/{id}`: Atualização parcial de estado ou dados.

### Frontend Angular (PWA)
- **Localização do Módulo:** `frontend/src/app/features/{modulo}/`
- **Componentes:** Componente de listagem (`data-table`), formulário de cadastro e modal de detalhes.
- **Guards Aplicáveis:** `papel.guard.ts` e `condominio.guard.ts`.

### Tarefas Assíncronas (Celery + Redis)
- Fila responsável por disparos de notificações, sincronizações de hardware ou processamento de arquivos.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal Principal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `recurso.criado` | Gestão / Portaria | Push + In-app | Alerta operacional imediato para triagem. |
| `recurso.atualizado` | Morador autor | Push + E-mail | Atualização do status do pedido ou chamado. |

---

## 9. Segurança, Auditoria e LGPD

- **Categorização de Dados:** Classificação dos dados (pessoais comuns vs sensíveis).
- **Base Legal (LGPD):** Execução de contrato (art. 7º, V) ou Legítimo interesse (art. 7º, IX).
- **Trilha de Auditoria:** Registro obrigatório na tabela `registro_auditoria` para todas as mutações (`CREATE`, `UPDATE`, `DELETE`).
- **Política de Retenção:** Prazo de armazenamento e regras para anonimização/descarte após o encerramento do vínculo.
