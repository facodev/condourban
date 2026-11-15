# Enquetes e Consultas de Opinião da Comunidade

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Síndicos precisam consultar a opinião dos moradores sobre decisões cotidianas (ex: cor da pintura da fachada, horário de funcionamento da academia, aquisição de novo brinquedo para o parquinho) sem a burocracia, custos e quórum estrito de uma assembleia geral formal.
- **Proposta de Valor:** Permitir a criação de enquetes rápidas com múltipla escolha ou voto único por unidade autônoma, apuração em tempo real com gráficos intuitivos e encerramento automatizado no prazo estipulado.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `comunicacao` |
| **Subdomínio** | `enquetes` |
| **Fase de Entrega** | Fase 2 (Operação) |
| **Tabelas do Banco (pt-BR)** | `enquete`, `opcao_enquete`, `voto_enquete` |
| **Perfis com Acesso** | Síndico e Administradora (criam); Moradores (votam e acompanham resultado) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Criar enquete com opções e data limite | — | — | — | — | **Sim** | **Sim** |
| Votar na enquete ativa (1 voto por unidade) | **Sim (titular)** | Se permitido | — | — | Sim (se morador) | — |
| Visualizar resultado parcial em tempo real | Se config | Se config | — | — | **Sim** | **Sim** |
| Encerrar enquete manualmente | — | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Enquete

```text
[RASCUNHO] ──(publicar)──► [ABERTA_VOTACAO] ──(prazo atingido / encerramento)──► [ENCERRADA]
                                 │
                                 └──(cancelamento)──► [CANCELADA]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Criação de Enquete pelo Síndico
1. O síndico acessa `Comunicação > Enquetes > Nova Enquete`.
2. Informa:
   - **Título / Pergunta:** Ex: *"Qual melhoria devemos priorizar na área de lazer este ano?"*
   - **Descrição:** Contexto explicativo com fotos das opções.
   - **Opções de Voto:** Opção 1: Troca dos aparelhos da academia; Opção 2: Aquecimento da piscina; Opção 3: Brinquedos novos no playground.
   - **Data e Hora de Encerramento:** Ex: 30 de novembro às 23h59.
   - **Regra de Votação:** `1_VOTO_POR_UNIDADE` (apenas o titular vota) ou `VOTO_POR_PESSOA`.
   - **Visibilidade:** Parcial aberta ou resultado visível apenas após o encerramento.
3. O sistema publica a enquete e emite push notification a todos os moradores.

### 5.2 Votação pelo Morador
1. O morador clica na notificação e visualiza a enquete no app.
2. Seleciona a opção desejada e clica em **"Confirmar Meu Voto"**.
3. O sistema valida se a unidade já votou; se não, grava o voto de forma anônima/auditável em `voto_enquete`.
4. O app exibe a confirmação visual e o percentual de votos até o momento.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Enquetes têm caráter consultivo e de escuta ativa; não substituem formalmente o valor legal de uma assembleia geral de condomínio ([assembleias-virtuais.md](../07_governanca/assembleias-virtuais.md)).
- **RN-02:** Em enquetes configuradas com regra de unidade, o registro de voto de um morador bloqueia imediatamente a votação para os demais dependentes daquela mesma unidade.
- **RN-03:** Não é permitida a alteração das opções de voto após o primeiro voto computado.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/comunicacao/enquetes`)
- `GET /api/v1/comunicacao/enquetes`: Enquetes ativas e histórico de encerradas.
- `POST /api/v1/comunicacao/enquetes`: Criação de nova enquete.
- `POST /api/v1/comunicacao/enquetes/{id}/votar`: Envio de voto.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `enquete.aberta` | Moradores | Push | "Participe: Nova enquete sobre a área de lazer aberta para votação!" |
| `enquete.resultado` | Moradores | Push + In-app | "Enquete encerrada! Veja o resultado final da escolha da melhoria." |
