# Acionamentos Remotos e Trilha de Eventos de Passagem

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Moradores retidos na chuva aguardando o porteiro abrir a clausura, prestadores aguardando na entrada de serviço sem ninguém na guarita e falta de histórico confiável sobre quem entrou ou saiu do condomínio para fins de segurança e perícia.
- **Proposta de Valor:** Permitir que moradores autorizados acionem portões, cancelas e portas sociais diretamente pelo aplicativo com validação por geolocalização (geofencing) e garantir uma trilha de auditoria completa e imutável de todos os eventos de passagem.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `controle_acesso` |
| **Subdomínio** | `eventos_acesso` e `dispositivos` |
| **Fase de Entrega** | Fase 2 (Logs) / Fase 4 (Acionamento Remoto In-App) |
| **Tabelas do Banco (pt-BR)** | `acionamento_remoto`, `evento_passagem_acesso`, `dispositivo_acesso` |
| **Perfis com Acesso** | Morador (portões permitidos), Porteiro, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Acionar portão veicular pelo app | **Sim (com geofence)** | **Sim** | **Sim** | **Sim** | — |
| Acionar porta de pedestre / clausura | **Sim (com geofence)** | **Sim** | **Sim** | **Sim** | — |
| Visualizar histórico das próprias passagens | **Sim** | — | — | — | — |
| Visualizar trilha geral de passagens do prédio | — | **Sim** | **Sim** | **Sim** | **Sim** |
| Exportar relatório pericial de eventos | — | — | — | **Sim** | **Sim** |

---

## 4. Tipos de Eventos de Passagem Registrados

| Tipo de Evento | Origem | Ação Resultante |
| :--- | :--- | :--- |
| `ACESSO_PERMITIDO` | Leitora Facial, Tag ou QR Code válido | Porta destravada, evento registrado no feed. |
| `ACESSO_NEGADO` | Credencial expirada, bloqueada ou sem horário | Porta permanece travada; alerta visual na tela da portaria. |
| `ACIONAMENTO_REMOTO` | Botão no aplicativo móvel | Comando de relé enviado à controladora com coordenadas GPS. |
| `PASSAGEM_FORCADA` | Sensor magnético aberto sem autenticação prévia | Alarme sonoro na guarita e notificação de pânico aos operadores. |
| `PORTA_ABERTA_TEMPO` | Porta travada aberta por mais de 60 segundos | Alerta sonoro de advertência na clausura. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Acionamento Remoto de Portão pelo App com Geofencing
1. O morador se aproxima do portão da garagem e abre o app no smartphone.
2. Clica no botão **"Abrir Portão da Garagem"**.
3. O app captura a posição GPS atual do dispositivo e envia para a API junto com o comando.
4. A API valida:
   - Se o morador possui veículo cadastrado e vaga ativa.
   - Se a geolocalização está dentro do raio de segurança de 100 metros do portão.
5. Se validado, a API emite comando MQTT/TCP para o relé da controladora do portão.
6. O portão abre e o evento `ACIONAMENTO_REMOTO` é gravado com o ID do morador, coordenadas e horário exato.

### 5.2 Consulta e Auditoria de Passagens
1. Em caso de ocorrência no condomínio (ex: furto de bicicleta na garagem), o síndico acessa `Controle de Acesso > Trilha de Passagens`.
2. Filtra pelo portão de pedestres e pelo intervalo de data e hora suspeito.
3. O sistema exibe a lista cronológica com foto capturada pela câmera do dispositivo, nome da pessoa, tipo de credencial e unidade.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O acionamento remoto in-app exige obrigatoriamente validação de raio de geolocalização (geofencing) para evitar aberturas acidentais a quilômetros de distância.
- **RN-02:** Todo evento de passagem é imutável: registros em `evento_passagem_acesso` nunca podem ser alterados ou excluídos, garantindo validade pericial e jurídica.
- **RN-03:** Acionamentos remotos realizados por portaria remota gravam o operador logado e o motivo da liberação.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/controle-acesso/`)
- `POST /api/v1/controle-acesso/acionamentos`: Execução de abertura de porta com payload contendo `{dispositivo_id, latitude, longitude}`.
- `GET /api/v1/controle-acesso/eventos`: Consulta paginada da trilha de eventos com filtros por período, dispositivo e pessoa.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `passagem.dependente` | Morador titular | Push | "Seu dependente João acessou a Portaria Principal às 17h45." |
| `alarme.porta_forcada` | Porteiros e Síndico | Push Urgente + Som | "ALERTA: Portão Lateral de Pedestres foi arrombado/forçado!" |
