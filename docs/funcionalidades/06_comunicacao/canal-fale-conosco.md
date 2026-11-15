# Canal Fale Conosco e Atendimento Direto à Administração

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Síndicos abordados a qualquer hora na garagem ou no elevador para tirar dúvidas triviais, perda de histórico de solicitações enviadas em chats privados e demora para encaminhar pedidos administrativos à administradora do condomínio.
- **Proposta de Valor:** Canal direto, profissional e centralizado de mensageria assíncrona entre o morador e a equipe de gestão (síndico, conselho e administradora), garantindo prazos de resposta (SLA), registro histórico de conversas e encaminhamento organizado de solicitações.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `comunicacao` |
| **Subdomínio** | `atendimento` e `fale_conosco` |
| **Fase de Entrega** | Fase 1 (Fundação) |
| **Tabelas do Banco (pt-BR)** | `conversa_atendimento`, `mensagem_atendimento` |
| **Perfis com Acesso** | Morador solicitante, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Enviar mensagem / dúvida à administração | **Sim** | — | — | — | — |
| Responder mensagem do morador | — | — | — | **Sim** | **Sim** |
| Encaminhar ticket para a administradora | — | — | — | **Sim** | **Sim** |
| Encerrar conversa com avaliação de satisfação | **Sim** | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados do Atendimento

```text
[NOVA_MENSAGEM] ──(visualização da gestão)──► [EM_ATENDIMENTO] ──(resposta enviada)──► [RESPONDIDO]
                                                                                           │
                                                                                           └──(resolvido)──► [CONCLUIDO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Envio de Dúvida pelo Morador
1. O morador entra em `Ajuda > Fale com a Administração`.
2. Seleciona o assunto: Dúvida sobre Cota Condominial, Solicitação de Tag, Sugestão de Melhoria, Dúvida Geral.
3. Digita sua mensagem e anexa arquivo se necessário (ex: foto ou comprovante).
4. O sistema cria o chamado com SLA padrão de 48 horas úteis e notifica o síndico.

### 5.2 Resposta e Acompanhamento
1. O síndico ou analista da administradora abre a caixa de entrada, responde ao morador e anexa a resposta.
2. O morador recebe notificação push imediata e pode replicar dentro da mesma conversa.
3. Ao finalizar, o morador avalia o atendimento com nota de 1 a 5 estrelas.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O canal Fale Conosco é estritamente privado: apenas os membros da unidade autora e os administradores autorizados do condomínio visualizam a conversa.
- **RN-02:** Reclamações que envolvam infrações de convenção contra outros vizinhos devem ser automaticamente redirecionadas para o [ocorrencias-livro.md](ocorrencias-livro.md).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/comunicacao/fale-conosco`)
- `POST /api/v1/comunicacao/fale-conosco`: Nova conversa.
- `GET /api/v1/comunicacao/fale-conosco`: Histórico de conversas do usuário.
- `POST /api/v1/comunicacao/fale-conosco/{id}/mensagens`: Envio de nova resposta.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `fale_conosco.resposta` | Morador autor | Push + E-mail | "A administração respondeu à sua solicitação sobre tags." |
