# Gestão de Veículos e Animais Domésticos (Pets)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Conflitos recorrentes de estacionamento (veículos não autorizados, uso indevido de vagas de visitantes e bloqueio de passagens) e ocorrências com animais soltos, barulho ou raças de grande porte sem coleira nas áreas comuns.
- **Proposta de Valor:** Vincular formalmente cada automóvel, moto e animal doméstico à respectiva unidade residencial e vaga demarcada, permitindo identificação instantânea pela guarita da portaria e pelas câmeras LPR (leitura de placas).

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `identidade_cadastro` |
| **Subdomínio** | `veiculos_pets` |
| **Fase de Entrega** | Fase BC-01 (Identidade e Cadastro Completo) |
| **Tabelas do Banco (pt-BR)** | `veiculo`, `pet`, `vaga_garagem`, `ocupacao_unidade` |
| **Perfis com Acesso** | Morador da unidade, Porteiro, Síndico, Administradora |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Cadastrar veículo / moto | **Sim (própria unidade)** | — | — | — | **Sim** | **Sim** |
| Cadastrar pet (cão, gato, etc.) | **Sim (própria unidade)** | — | — | — | **Sim** | **Sim** |
| Consultar veículo por placa | Próprio | Próprio | **Todos** | **Todos** | **Todos** | **Todos** |
| Consultar pet por foto/unidade | Próprio | Próprio | **Todos** | **Todos** | **Todos** | **Todos** |
| Vincular veículo à vaga de garagem | Sim (se tiver vaga) | — | — | — | **Sim** | **Sim** |
| Desativar / Excluir veículo ou pet | **Sim** | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados e Ciclo de Vida

```text
[ATIVO] ──(venda do auto / óbito / doação)──► [INATIVO]
   │
   └──(advertência / irregularidade na vaga)──► [EM_ALERTA] ──(regularização)──► [ATIVO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Cadastro de Veículo pelo Morador
1. O morador entra em `Minha Unidade > Veículos e Vagas > Adicionar Veículo`.
2. Informa:
   - **Placa:** Formato Mercosul (`ABC1D23`) ou tradicional (`ABC-1234`).
   - **Tipo:** Automóvel, Moto, Utilitário, Bicicleta Elétrica.
   - **Marca / Modelo / Cor:** Ex: Toyota Corolla Preto.
   - **Vaga Vinculada:** Seleciona entre as vagas de garagem atribuídas à sua unidade.
3. O sistema valida o formato da placa, grava o registro em `veiculo` e sincroniza automaticamente a placa com as antenas/câmeras LPR do controle de acesso.

### 5.2 Cadastro de Animal Doméstico (Pet)
1. O morador acessa `Minha Unidade > Pets > Cadastrar Pet`.
2. Informa:
   - **Nome:** Ex: "Thor".
   - **Espécie / Raça / Porte:** Canino / Golden Retriever / Grande.
   - **Foto do Animal:** Foto nítida para identificação visual em caso de fuga.
   - **Comprovante de Vacinação:** Upload opcional ou obrigatório conforme a convenção do condomínio.
3. O sistema grava o registro em `pet` e disponibiliza para consulta da portaria e no mural de achados/perdidos caso o animal seja encontrado solto no condomínio.

### 5.3 Consulta de Placa pela Portaria
1. Um carro estaciona em vaga irregular ou na entrada da guarita.
2. O porteiro digita os 3 primeiros caracteres da placa na busca rápida do terminal.
3. O sistema retorna instantaneamente: Morador responsável, Bloco, Unidade, Telefone e foto do veículo cadastrado.
4. O porteiro clica em **"Notificar Morador"**, disparando alerta imediato pelo app.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Cada placa é única por condomínio ativo; não é permitido o cadastro da mesma placa em unidades distintas sem prévia desvinculação.
- **RN-02:** A quantidade máxima de veículos cadastrados com vaga prioritária não pode exceder o número de vagas escrituradas da respectiva unidade.
- **RN-03:** A máscara de placa deve suportar e normalizar tanto o padrão Mercosul quanto o padrão antigo de 3 letras e 4 números.
- **RN-04:** Animais de raças classificadas como de guarda pelo regimento interno (ex: Pitbull, Rottweiler) geram alerta obrigatório no cadastro para conferência do uso de focinheira e guia nas áreas comuns.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/veiculos-pets/`)
- `GET /api/v1/veiculos`: Listagem dos veículos da unidade (morador) ou busca por placa (portaria/gestão).
- `POST /api/v1/veiculos`: Cadastro de novo automóvel/moto.
- `DELETE /api/v1/veiculos/{id}`: Desativação de veículo vendido.
- `GET /api/v1/pets`: Listagem dos pets da unidade.
- `POST /api/v1/pets`: Cadastro de novo animal com upload de foto no S3.

### Frontend Angular (PWA)
- Componente: `features/identidade_cadastro/components/veiculos-pets`.
- Pipes compartilhados: `placa.pipe.ts` para formatação automática em tempo real.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `veiculo.irregular` | Morador titular | Push Urgente | "Atenção: O veículo placa ABC1D23 está estacionado em vaga não permitida." |
| `pet.cadastrado` | Gestão | In-app | "Novo animal doméstico registrado na Unidade 304 Bloco A." |

---

## 9. Segurança, Auditoria e LGPD

- **Dados Sensíveis:** Placas de veículos são vinculadas exclusivamente às unidades para controle de segurança física patrimonial.
- **Base Legal:** Legítimo interesse do condomínio para segurança coletiva (art. 7º, IX da LGPD).
