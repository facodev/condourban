# Gestão de Achados e Perdidos

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Objetos pessoais esquecidos nas áreas comuns (chaves, brinquedos na piscina, carteiras, óculos na academia, casacos no salão de festas) acumulam-se desordenadamente na guarita sem registro, gerando desconfiança e descarte indevido.
- **Proposta de Valor:** Criar um mural digital transparente de achados e perdidos, onde itens encontrados por colaboradores ou moradores são cadastrados com foto e descrição, permitindo ao dono identificar seu pertence pelo app e retirá-lo na guarita mediante recibo digital.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `portaria` |
| **Subdomínio** | `atendimento` e `achados_perdidos` |
| **Fase de Entrega** | Fase 3 (Governança e Serviços) |
| **Tabelas do Banco (pt-BR)** | `item_achado_perdido`, `termo_restituicao_item` |
| **Perfis com Acesso** | Todos os moradores (leitura do mural), Porteiro e Zelador (cadastro e entrega) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Cadastrar item encontrado com foto | **Sim** | **Sim** | **Sim** | **Sim** | — |
| Consultar mural de itens guardados | **Todos** | **Todos** | **Todos** | **Todos** | **Todos** |
| Reivindicar posse do item pelo app | **Sim** | — | — | — | — |
| Dar baixa na devolução com termo assinado | — | **Sim** | **Sim** | **Sim** | — |
| Registrar doação ou descarte pós-prazo | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados do Item Achado e Perdido

```text
[GUARDADO_PORTARIA] ──(proprietário retira)──► [RESTITUIDO]
         │
         └──(prazo legal de 90 dias expirado)──► [DOADO_DESCARTADO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Registro do Item Encontrado
1. Um morador ou faxineiro encontra uma chave de carro na área da piscina e entrega na portaria.
2. O porteiro clica em `Achados e Perdidos > Novo Item`.
3. Informa:
   - **Título / Categoria:** Chaveiro com chave de veículo Hyundai.
   - **Local onde foi encontrado:** Borda da piscina infantil.
   - **Foto:** Captura foto do objeto na bancada da guarita.
4. O item é salvo com status `GUARDADO_PORTARIA` e surge imediatamente no mural do aplicativo para todos os moradores do condomínio.

### 5.2 Restituição do Objeto ao Dono
1. O morador dono da chave vê a foto no app e comparece à portaria.
2. O porteiro localiza o registro, confere a descrição fornecida pelo morador (ex: *"Tem um chaveiro do Homem-Aranha"*).
3. O morador assina digitalmente o recibo na tela do PWA.
4. O status é atualizado para `RESTITUIDO` com o nome e unidade do recebedor arquivados.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Documentos pessoais oficiais encontrados (RG, CNH, cartões bancários) não devem ter seus números e dados sensíveis expostos publicamente na foto do mural (o porteiro oculta os dígitos no momento da captura).
- **RN-02:** Objetos sem reivindicação após 90 dias de guarda são encaminhados para doação a instituições de caridade ou descarte, conforme deliberação da assembleia geral.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/portaria/`)
- `GET /api/v1/portaria/achados-perdidos`: Listagem pública dos itens sob custódia.
- `POST /api/v1/portaria/achados-perdidos`: Cadastro de novo item com upload de foto no S3.
- `POST /api/v1/portaria/achados-perdidos/{id}/restituir`: Registro de entrega com assinatura.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `item.cadastrado` | Todos os Moradores | In-app | "Novo objeto cadastrado no mural de Achados e Perdidos: Chave na piscina." |
