# Estrutura Física do Condomínio (Blocos, Unidades, Vagas e Áreas Comuns)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Condomínios residenciais e comerciais possuem configurações físicas variadas (torres verticais, vilas horizontais, blocos com subsolos, vagas privativas ou rotativas, e múltiplos espaços de lazer). Sem um modelo digital preciso, o isolamento de dados por unidade falha e o agendamento de espaços ou controle de acessos torna-se caótico.
- **Proposta de Valor:** Mapear a arquitetura física e geoespacial do condomínio, estabelecendo a hierarquia formal entre Condomínio → Blocos/Torres → Unidades Autônomas → Vagas de Garagem e Áreas Comuns, servindo de fundação para o multi-tenancy e as políticas de segurança.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `condominio` |
| **Subdomínio** | `estrutura` e `areas_comuns` |
| **Fase de Entrega** | Fase 1 (Fundação) |
| **Tabelas do Banco (pt-BR)** | `condominio`, `bloco`, `unidade`, `vaga_garagem`, `area_comum` |
| **Perfis com Acesso** | Síndico, Administradora, Admin da Plataforma (leitura para Morador e Porteiro) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora | Admin Plataforma |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Cadastrar / Editar Bloco ou Torre | — | — | — | **Sim** | **Sim** | **Sim** |
| Cadastrar / Importar Unidades em lote | — | — | — | **Sim** | **Sim** | **Sim** |
| Configurar vagas de garagem | — | — | — | **Sim** | **Sim** | **Sim** |
| Cadastrar Áreas Comuns (salão, quiosque) | — | — | — | **Sim** | **Sim** | **Sim** |
| Consultar mapa e unidades do condomínio | Própria | Todas | Todas | Todas | Todas | Todas |

---

## 4. Máquina de Estados e Ciclo de Vida

```text
[CADASTRADO] ──(manutenção/obra)──► [INTERDITADO] ──(liberação)──► [CADASTRADO]
     │
     └──(desativação definitiva)──► [INATIVO]
```

| Estado | Significado para Áreas Comuns e Unidades | Ações Permitidas |
| :--- | :--- | :--- |
| `ATIVO` | Espaço ou unidade plenamente operacional e habitável. | Agendamentos, acessos e cadastros normais. |
| `INTERDITADO` | Em reforma, vistoria ou reparo emergencial (ex: piscina ou salão). | Bloqueio imediato de novos agendamentos no app. |
| `INATIVO` | Espaço desativado ou unidade fundida/desmembrada. | Consulta apenas em relatórios históricos. |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Importação Inicial da Estrutura do Condomínio (Setup)
1. Durante a implantação, a administradora acessa `Configurações > Estrutura Física`.
2. Faz o upload de planilha padronizada (.CSV ou .XLSX) contendo:
   - Identificação dos Blocos/Torres (ex: Bloco A, Bloco B).
   - Lista de Unidades com número, andar e metragem/fração ideal (ex: Apt 101, Apt 102).
   - Vagas de garagem vinculadas (ex: Vaga G-12 coberta vinculada ao Apt 101).
3. A API FastAPI processa a planilha, valida duplicidades e cria os registros em transação atômica.
4. O sistema gera a árvore completa do condomínio no banco PostgreSQL.

### 5.2 Cadastro de Áreas Comuns (Espaços Reserváveis)
1. O síndico acessa `Áreas Comuns > Nova Área`.
2. Informa:
   - **Nome:** Ex: "Salão de Festas Nobre".
   - **Capacidade Máxima:** Ex: 80 pessoas.
   - **Regras de Funcionamento:** Horário permitido (ex: 09h00 às 22h00).
   - **Taxa de Limpeza / Caução:** Se houver (ex: R$ 150,00).
   - **Fotos do Espaço:** Upload de fotos para exibição no catálogo do morador.
3. O espaço fica disponível imediatamente para visualização e agendamento no módulo de reservas.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O identificador da unidade (combinação de `bloco_id` + `numero_unidade`) é estritamente único dentro do mesmo condomínio.
- **RN-02:** Toda unidade residencial deve pertencer obrigatoriamente a um condomínio válido e ativo.
- **RN-03:** A capacidade máxima de uma área comum é vinculada aos limites do Auto de Vistoria do Corpo de Bombeiros (AVCB) cadastrado.
- **RN-04:** A desativação de uma área comum com reservas futuras ativas exige o cancelamento justificado ou realocação prévia de todos os eventos afetados.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/condominio/`)
- `GET /api/v1/condominio/blocos`: Lista os blocos e torres.
- `GET /api/v1/condominio/unidades`: Lista unidades com filtros por bloco e status de ocupação.
- `POST /api/v1/condominio/unidades/importar`: Importação em lote de estrutura via arquivo.
- `GET /api/v1/condominio/areas-comuns`: Catálogo de espaços físicos e de lazer.
- `POST /api/v1/condominio/areas-comuns`: Criação de novo espaço físico.

### Frontend Angular (PWA)
- Componente: `features/condominio/components/estrutura` e `features/condominio/components/areas-comuns`.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `area_comum.interditada` | Todos os Moradores | Push + Mural | "Atenção: A piscina principal estará interditada para manutenção nos dias X e Y." |

---

## 9. Segurança, Auditoria e LGPD

- **Multi-tenancy:** Toda a árvore física referencia `condominio_id`, garantindo isolamento total por Row-Level Security (RLS) no PostgreSQL.
- **Auditoria:** Alterações cadastrais de frações ideais ou vínculos de vagas de garagem são auditadas permanentemente com o usuário autor.
