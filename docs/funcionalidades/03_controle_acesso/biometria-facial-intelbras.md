# Biometria Facial e Integração com Controladoras Intelbras/IoT

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Falhas de segurança nas portarias com liberação visual equivocada, filas nos horários de pico e complexidade de gerenciar sincronizações biométricas entre o software de gestão e múltiplos equipamentos de hardware de diferentes fabricantes instalados nas entradas do condomínio.
- **Proposta de Valor:** Permitir o pré-cadastro e captura de biometria facial diretamente pelo smartphone do morador ou no tablet da portaria, sincronizando templates faciais de forma assíncrona, tolerante a falhas e segura com equipamentos de controle de acesso (Intelbras/Control iD), mantendo auditoria rigorosa de passagens e contingência por QR Code.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `controle_acesso` |
| **Subdomínio** | `dispositivos` e `credenciais` |
| **Fase de Entrega** | Fase 2 (Operação e Acesso) |
| **Tabelas do Banco (pt-BR)** | `dispositivo_acesso`, `credencial_acesso`, `sincronizacao_acesso`, `evento_passagem_acesso` |
| **Padrão Arquitetural** | **Adapter Pattern** via `AccessControlProvider` (ADR-004) e Idempotência (ADR-009) |
| **Perfis com Acesso** | Morador (captura selfie), Porteiro, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Capturar / Atualizar própria selfie biométrica | **Sim** | — | — | **Sim** | **Sim** |
| Capturar foto facial de visitante na portaria | — | **Sim** | — | **Sim** | **Sim** |
| Vincular credencial facial a leitoras físicas | — | **Sim** | — | **Sim** | **Sim** |
| Forçar re-sincronização com leitoras | — | **Sim** | — | **Sim** | **Sim** |
| Visualizar status online das leitoras | — | **Sim** | **Sim** | **Sim** | **Sim** |
| Revogar credencial facial imediatamente | Própria | **Sim** | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Sincronização de Hardware

```text
[PENDENTE] ──(envio à controladora)──► [SINCRONIZANDO] ──(sucesso)──► [SINCRONIZADO]
    │                                         │
    │                                         └──(timeout/erro)──► [FALHA]
    │                                                                  │
    └──(tentativa esgotada)────────────────────────────────────────────┴──(retry Celery)──► [SINCRONIZANDO]
```

| Estado | Significado Técnico | Ação do Sistema |
| :--- | :--- | :--- |
| `PENDENTE` | Credencial facial aprovada no app; aguardando envio para as leitoras. | Inserção na fila de tarefas do Celery. |
| `SINCRONIZANDO` | Comunicação TCP/HTTP ativa com o gateway local ou IP da leitora. | Envio do payload com cabeçalho de idempotência. |
| `SINCRONIZADO` | Confirmação de gravação do template recebida do hardware. | Credencial ativa para abertura de portas. |
| `FALHA` | Erro de rede na guarita ou equipamento offline. | Retentativa automática com backoff exponencial (até 5 vezes). |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Captura Facial pelo Morador no App PWA
1. O morador acessa `Acesso > Minha Biometria Facial > Cadastrar Rosto`.
2. O app aciona a câmera frontal e exibe instruções visuais de enquadramento (iluminação adequada, sem óculos escuros ou chapéu).
3. O morador captura a selfie e assina digitalmente o **Termo de Consentimento Biométrico (LGPD)**.
4. O frontend envia a foto para a API FastAPI.
5. O backend executa o corte e normalização de imagem, grava em `credencial_acesso` (`tipo_credencial = 'FACIAL'`) e agenda tarefa Celery: `sincronizar_credencial_equipamentos(credencial_id)`.
6. O adapter `IntelbrasProvider` conecta-se às leitoras da guarita/portões autorizados e envia o template.
7. Ao receber o `OK`, atualiza o status para `SINCRONIZADO` e notifica o morador que seu acesso facial está liberado.

### 5.2 Contingência Offline da Portaria
1. Caso a conexão de internet da guarita caia, os equipamentos Intelbras continuam operando em modo offline com o banco local de templates já sincronizados.
2. Visitantes sem biometria prévia utilizam o **QR Code Dinâmico** gerado pelo convite do morador como fallback imediato.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-004](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-004-integracao-intelbras-facial.md), a aprovação cadastral de uma pessoa é **desacoplada** do hardware; a indisponibilidade física de uma leitora nunca corrompe ou desfaz o cadastro civil no sistema.
- **RN-02:** Conforme o [ADR-009](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-009-idempotencia-integracoes.md), toda requisição de sincronização com equipamentos utiliza chave de idempotência (`idempotency_key`), evitando duplicidade de registros na memória da leitora.
- **RN-03:** A exclusão ou desativação de um morador ou prestador no sistema aciona imediatamente a fila de **revogação biométrica prioritária** em todas as controladoras cadastradas.
- **RN-04:** É obrigatório o consentimento explícito e auditável para armazenamento de dados biométricos sensíveis antes do processamento da imagem.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/controle-acesso/`)
- `POST /api/v1/controle-acesso/facial/capturar`: Upload da foto facial com consentimento LGPD.
- `GET /api/v1/controle-acesso/dispositivos`: Listagem de controladoras e leitoras faciais ativas.
- `POST /api/v1/controle-acesso/dispositivos/{id}/sincronizar`: Disparo manual de re-sincronização.
- `POST /api/v1/controle-acesso/webhooks/{provedor}`: Webhook receptor de eventos de passagem emitidos pelo hardware.

### Worker Assíncrono (Celery)
- Task `tasks.hardware.sincronizar_facial`: Orquestra o envio para múltiplas controladoras em paralelo, tolerando falhas individuais.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `facial.liberado` | Morador | Push PWA | "Seu reconhecimento facial foi habilitado nas portarias e garagens." |
| `leitora.offline` | Porteiro e Síndico | Alerta In-app | "Atenção: A leitora facial Portão Social A perdeu conexão com a rede." |

---

## 9. Segurança, Auditoria e LGPD

- **Dado Pessoal Sensível:** O dado biométrico é classificado como sensível (art. 5º, II da LGPD) e exige consentimento formal e inequívoco (art. 11, I da LGPD).
- **Criptografia:** Fotos biométricas são armazenadas em bucket privado com criptografia AES-256 e transmitidas via HTTPS/TLS 1.3.
