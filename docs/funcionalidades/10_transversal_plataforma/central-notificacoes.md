# Central de Notificações Multicanal (Push PWA, E-mail, In-App)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Mensagens críticas perdidas no lixo eletrônico, moradores alegando que não foram notificados sobre encomendas ou assembleias e custos elevados com envios desnecessários de SMS para comunicações de rotina.
- **Proposta de Valor:** Motor unificado de notificações que orquestra a entrega inteligente através de três canais (Push Notifications no PWA via Web Push Protocol / VAPID, E-mails transacionais e Feed de Notificações In-App), respeitando as preferências de notificação do usuário e registrando status de entrega e leitura.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `transversal` |
| **Subdomínio** | `notificacoes` |
| **Fase de Entrega** | Fase 1 (Base In-App/Email) / Fase 2 (Push VAPID) |
| **Tabelas do Banco (pt-BR)** | `notificacao`, `inscricao_push_web`, `preferencia_notificacao` |
| **Tecnologias** | Celery + Redis (filas de envio), Web Push API, SMTP/SES |

---

## 3. Matriz de Canais por Categoria de Evento

| Categoria do Evento | Push PWA | E-mail Transacional | Alerta In-App | Exemplo |
| :--- | :---: | :---: | :---: | :--- |
| **Segurança e Urgência** | **Sim (Alto volume)** | **Sim** | **Sim (Modal)** | Alarme de porta arrombada, vazamento de gás. |
| **Acesso e Portaria** | **Sim** | — | **Sim** | Chegada de visitante, encomenda recebida na guarita. |
| **Lazer e Reservas** | **Sim** | **Sim** | **Sim** | Confirmação de reserva, lembrete de lista de convidados. |
| **Governança e Assembleia** | **Sim** | **Sim (com Edital PDF)** | **Sim** | Convocação de assembleia, liberação de pauta de votação. |
| **Financeiro e Cobrança** | **Sim** | **Sim (com Boleto/Pix)** | **Sim** | Nova fatura disponível, lembrete de vencimento em 3 dias. |
| **Comunitário e Social** | — | — | **Sim (Feed)** | Novo item em classificados, enquete informal. |

---

## 4. Ciclo de Vida da Notificação

```text
[ENFILEIRADA] ──(processamento Celery)──► [ENVIADA] ──(confirmação push/gateway)──► [ENTREGUE] ──(clique do morador)──► [LIDA]
      │                                       │
      └──(falha de conexão/token expirado)────┴──(retry 3x)──► [FALHA]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Registro de Inscrição Push no Frontend (PWA)
1. Ao fazer login no app no smartphone ou computador, o morador visualiza o prompt amigável: *"Deseja receber alertas sobre suas encomendas e visitantes?"*
2. Ao clicar em **"Permitir"**, o Service Worker do Angular solicita permissão via `Notification.requestPermission()`.
3. A chave pública VAPID é utilizada para gerar o endpoint e chaves de criptografia da inscrição (`PushSubscription`).
4. O frontend envia a assinatura para a API: `POST /api/v1/notificacoes/push/inscrever`.
5. O backend grava os dados em `inscricao_push_web` vinculados ao `usuario_id` e condomínio ativo.

### 5.2 Disparo Assíncrono de Notificação
1. Um evento ocorre no sistema (ex: porteiro cadastra recebimento de encomenda).
2. A API despacha a mensagem para a fila Celery `tasks.notificacoes.enviar`.
3. O worker busca todas as inscrições ativas do morador destinatário.
4. Envia o payload criptografado via protocolo Web Push e atualiza o feed in-app.
5. O morador ouve o toque de notificação no celular e visualiza o card na barra de notificações.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O morador pode customizar suas preferências de notificação (ex: desabilitar avisos de classificados ou murais), mas notificações de segurança e convocações de assembleia são **obrigatórias e inegociáveis**.
- **RN-02:** Inscrições Push que retornem status HTTP `410 Gone` (aplicativo desinstalado ou permissão revogada pelo usuário no navegador) são automaticamente expurgadas do banco para evitar sobrecarga.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/notificacoes/`)
- `POST /api/v1/notificacoes/push/inscrever`: Registro de endpoint Push.
- `GET /api/v1/notificacoes/minhas`: Consulta paginada do feed in-app com indicador de lida/não-lida.
- `PATCH /api/v1/notificacoes/{id}/marcar-lida`: Confirmação de visualização.

---

## 8. Segurança e Privacidade

- **LGPD:** O consentimento para notificações em smartphone pode ser revogado a qualquer momento pelo usuário no menu de configurações do aplicativo.
- **Criptografia:** Todo payload Web Push é obrigatoriamente cifrado usando a curva elíptica ECDH (P-256) com HKDF, conforme a RFC 8291.
