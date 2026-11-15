# Gestão de Correspondências e Encomendas (Pacotes)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Portarias abarrotadas de caixas de e-commerce (Amazon, Mercado Livre), extravio de encomendas, moradores reclamando de atraso no aviso e falta de comprovação de quem realmente retirou o pacote na guarita.
- **Proposta de Valor:** Automatizar a recepção de encomendas com leitura ótica de etiqueta, foto comprobatória do pacote, notificação push instantânea para o morador com código PIN de retirada e protocolo digital de entrega.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `portaria` |
| **Subdomínio** | `encomendas` |
| **Fase de Entrega** | Fase 2 (Operação) |
| **Tabelas do Banco (pt-BR)** | `encomenda`, `historico_encomenda`, `retirada_encomenda` |
| **Perfis com Acesso** | `ENCOMENDAS` (recebe e dá baixa), Morador (aviso e PIN); Porteiro **não** opera pacotes |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Encomendas | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Registrar chegada de encomenda com foto | — | — | — | **Sim** | **Sim** | **Sim** | — |
| Visualizar encomendas da própria unidade | **Sim** | **Sim** | — | — | — | — | — |
| Consultar estoque de encomendas na portaria | — | — | — | **Todas** | **Todas** | **Todas** | **Todas** |
| Dar baixa na entrega com PIN / Assinatura | — | — | — | **Sim** | **Sim** | **Sim** | — |
| Autorizar terceiro/vizinho a retirar pacote | **Sim** | — | — | — | — | — | — |

---

## 4. Máquina de Estados das Encomendas

```text
[RECEBIDO_PORTARIA] ──(morador retira com PIN)──► [ENTREGUE]
        │
        ├──(prazo excedido de 15 dias)──► [AGUARDANDO_DEVOLUCAO]
        │
        └──(recusa/devolução ao entregador)──► [DEVOLVIDO]
```

| Estado | Significado Operacional | Ações Permitidas |
| :--- | :--- | :--- |
| `RECEBIDO_PORTARIA` | Pacote sob custódia física da portaria; notificação emitida. | Baixa de entrega ou reenvio de lembrete. |
| `ENTREGUE` | Morador retirou o pacote mediante validação de PIN ou assinatura. | Consulta em histórico (estado final). |
| `AGUARDANDO_DEVOLUCAO` | Pacote esquecido há mais de 15 dias na guarita. | Síndico pode notificar formalmente a unidade. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Recebimento de Pacote (Operador de Encomendas)
1. O entregador dos Correios ou transportadora chega com os pacotes.
2. O operador com papel `ENCOMENDAS` acessa: `Portaria > Nova Encomenda`.
3. Seleciona Bloco e Unidade do destinatário.
4. Informa a transportadora / remetente e o código de rastreio (pode ler código de barras com leitor USB ou câmera).
5. Tira uma foto rápida do pacote na guarita (mostrando a etiqueta com o nome legível).
6. O sistema gera automaticamente um **PIN de Retirada de 4 dígitos** exclusivo e grava em `encomenda`.
7. O morador recebe imediatamente uma notificação push no celular com a foto do pacote e o PIN de retirada.

### 5.2 Retirada do Pacote pelo Morador
1. O morador desce até o ponto de correspondências e informa: *"Boa noite, vim retirar a encomenda do 402"*.
2. O operador de encomendas localiza o registro da unidade no painel.
3. O morador digita seu PIN no teclado ou apresenta o QR Code da encomenda na tela do smartphone.
4. O sistema valida o PIN, registra a baixa com data/hora exata e o nome do operador, e move o status para `ENTREGUE`.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Nenhuma encomenda pode ser marcada como entregue sem a conferência do PIN de segurança do morador ou captura de assinatura digital na tela.
- **RN-02:** Pacotes contendo itens perecíveis (ex: delivery de farmácia, flores) recebem flag prioritária com envio de lembrete push reforçado a cada 30 minutos.
- **RN-03:** O morador pode autorizar um vizinho a retirar sua encomenda gerando um PIN compartilhado de uso único no aplicativo.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/portaria/`)
- `POST /api/v1/portaria/encomendas`: Registro de nova encomenda com upload da foto no S3.
- `GET /api/v1/portaria/encomendas/pendentes`: Lista de encomendas na guarita aguardando retirada.
- `POST /api/v1/portaria/encomendas/{id}/baixar`: Validação de PIN e baixa de entrega.

### Frontend Angular (PWA)
- Componente: `features/portaria/components/encomendas`.
- Componente morador: Cartão de encomenda com foto em destaque e botão de exibição do PIN.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `encomenda.recebida` | Morador titular e dependentes | Push + In-app | "Você recebeu uma encomenda (Amazon) na portaria! Seu PIN de retirada é 8492." |
| `encomenda.entregue` | Morador titular | Push | "A encomenda final 8492 foi retirada na portaria com sucesso." |
