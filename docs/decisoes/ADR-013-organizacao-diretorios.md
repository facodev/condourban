# ADR-013: Organização de Diretórios por Bounded Contexts e Consolidação de Subdomínios

- **Status:** Aceito
- **Data:** 2026-10-09 (Otimizado e consolidado em 2026-10-17)
- **Autores:** Time de Engenharia de Software e Arquitetura
- **Relacionado:** [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md), [ADR-010](ADR-010-nomenclatura-pt-br.md), [Estrutura.md](Estrutura.md)

## Contexto

A plataforma de gestão condominial atende múltiplos perfis (moradores, porteiros, síndicos, conselheiros e administradoras) e conecta integrações heterogêneas (dispositivos IoT, biometria facial, gateways bancários e telemetria de consumo).

Inicialmente, foram identificados dois desafios arquiteturais na organização do código:
1. **Risco de acoplamento e ambiguidade semântica:** Risco de misturar linguagem técnica em inglês com termos de negócio em português, além de acoplar regras de hardware e integrações físicas com o cadastro civil de pessoas.
2. **Fragmentação excessiva de subdomínios:** A divisão inicial previa mais de 30 subdiretórios individuais finamente granulados, gerando dispersão de arquivos, redundância de contratos (schemas/services) e sobrecarga cognitiva para rotinas intimamente correlatas (como separar visitantes de prestadores na portaria, ou dispersar ocorrências entre guarita e morador).

## Decisão

### 1. Adoção de 9 Bounded Contexts em Português do Brasil (pt-BR)

Adota-se a arquitetura modular baseada em **Domain-Driven Design (DDD)** dividida rigorosamente em **9 Bounded Contexts**, utilizando a Linguagem Ubíqua em português brasileiro (snake_case no código e sem caracteres especiais) para nomear os módulos no Backend (`backend/app/modulos/`) e no Frontend (`frontend/src/app/features/`):

1. **`identidade_cadastro/`**: Restrito exclusivamente a dados civis de indivíduos, contas de acesso, perfis de membresia, ocupações de unidades, veículos e animais domésticos. Não armazena lógica de liberação de hardware ou cancelas.
2. **`condominio/`**: Representação geoespacial e estrutural do empreendimento (condomínio, blocos, unidades, garagens e áreas comuns).
3. **`controle_acesso/`**: Motor operacional de integração IoT, controladoras de portas, antenas RFID/LPR, biometria facial, regras de autorização física e trilha de eventos de passagem.
4. **`portaria/`**: Operação da guarita humana ou remota, cobrindo o fluxo de atendimento a visitantes/prestadores e a custódia/retirada de encomendas.
5. **`reservas/`**: Ciclo de agendamento de áreas comuns, validação de regras de concorrência, lista de convidados (integrada à portaria) e vistorias/termos de caução.
6. **`comunicacao/`**: Canais de relacionamento institucional e social, murais de avisos, notificações push e gestão unificada de ocorrências de convivência.
7. **`governanca/`**: Gestão deliberativa formal, incluindo pautas de assembleias virtuais, votações com quórum digital, atas registradas, controle de papéis (RBAC) e auditoria de sistema.
8. **`financeiro/`**: Toda a operação monetária e de faturamento (boletos bancários, Pix, prestação de contas, despesas, acordos jurídicos e individualização de hidrômetros/gás).
9. **`manutencao/`**: Gestão patrimonial e conservação predial, incluindo chamados de reparo, cronograma preventivo (PMO), ordens de serviço e estoque de suprimentos.

---

### 2. Otimização e Consolidação Pragmática de Subdomínios

Para eliminar a fragmentação dos 30+ subdiretórios anteriores, consolida-se a estrutura interna de cada Bounded Context para **2 a 4 subdiretórios por módulo**:

- **Fusão de Visitantes e Prestadores em `portaria/atendimento/`**: Visitantes, prestadores de serviço e hóspedes temporários compartilham a mesma mecânica operacional de identificação civil, conferência de autorização/convite gerado pelo morador e registro de entrada/saída na guarita.
- **Centralização de Ocorrências em `comunicacao/ocorrencias/`**: Elimina-se a dispersão entre "livro de portaria" e "ocorrências do morador". Todas as ocorrências residem na mesma entidade/tabela unificada, diferenciadas pelo atributo de origem (`TIPO_ORIGEM = 'PORTARIA' | 'MORADOR' | 'GESTAO'`).
- **Unificação de Membros e Ocupações em `identidade_cadastro/usuarios/`**: Como o usuário autenticado precisa estar associado ao seu papel de membresia (síndico, morador, porteiro) e à sua ocupação da unidade (proprietário, inquilino) para geração do token JWT e execução de políticas de Row Level Security (RLS) no PostgreSQL, esses conceitos residem no mesmo subdomínio.
- **Lista de Convidados embutida em `reservas/agendamentos/`**: A lista de convidados não tem ciclo de vida autônomo sem uma reserva vinculada; ela é tratada como sub-recurso do agendamento, facilitando a consulta em lote pela guarita da portaria.

---

### 3. Padrão Interno das Camadas do Backend (FastAPI)

Dentro de cada subdomínio no backend, preserva-se a divisão canônica em 4 arquivos essenciais:

| Arquivo | Responsabilidade |
| :--- | :--- |
| `router.py` | Declaração de endpoints, roteamento HTTP e injeção de dependências. |
| `models.py` | Entidades mapeadas no SQLAlchemy 2.0 assíncrono conectadas ao PostgreSQL/SQLite. |
| `schemas.py` | Modelos Pydantic v2 para validação, serialização e contratos de entrada/saída. |
| `service.py` | Regras de negócio, validações de domínio e orquestração de transações. |

---

### 4. Padrão das Camadas de Infraestrutura e Compartilhada

- **Infraestrutura Transversal (`backend/app/core/` e `frontend/src/app/core/`)**:
  - `config.py`: Carregamento e tipagem de variáveis de ambiente.
  - `database.py`: Pool assíncrono do SQLAlchemy e injeção do tenant para RLS (`SET LOCAL app.condominio_id`).
  - `security.py`: Criptografia (hashing bcrypt/argon2 e assinatura JWT).
  - `dependencies.py`: Injeção de dependências do FastAPI (`get_db`, `current_user`, `current_tenant`).
  - `core/guards/` e `core/interceptors/` (Angular): Interceptores HTTP de JWT e guards de rotas por papel (`papel.guard.ts`) e condomínio (`condominio.guard.ts`).
- **Camada Compartilhada (`frontend/src/app/shared/`)**:
  - `components/`: Componentes reutilizáveis sem regra de negócio própria (`data-table`, `confirm-dialog`, `status-badge`, `upload-foto`).
  - `pipes/` e formatadores brasileiros: Máscaras e pipes para CPF/CNPJ, Placas Mercosul, Telefone e Moeda (BRL).

---

### 5. Padrão no Frontend (Angular 22+ PWA)

No frontend, a árvore em `frontend/src/app/features/` espelha diretamente os 9 Bounded Contexts através de **Standalone Components** com carregamento sob demanda (**Lazy Loading** via `loadChildren` / `loadComponent`), garantindo que perfis específicos (ex: moradores ou operadores de guarita) baixem apenas os bundles pertinentes ao seu escopo.

Cada componente Angular (`shared/` e `features/`) segue obrigatoriamente a **Regra de Separação de 3 Arquivos ([ADR-003](ADR-003-ui-estilizacao-e-portabilidade-web.md))**:
- `{nome}.component.ts`: Lógica reativa com Signals, injeção de dependências e metadados (`templateUrl`, `styleUrls`, `encapsulation: ViewEncapsulation.Emulated`). É proibido o uso de `template` ou `styles` inline.
- `{nome}.component.html`: Marcação semântica combinando diretivas Angular Material 3 e utilitários Tailwind CSS v4.
- `{nome}.component.scss`: Estilos encapsulados com seletor `:host` explícito.

## Consequências

### Positivas
- **Alinhamento com a Linguagem Ubíqua:** Nomenclatura idêntica entre os termos utilizados por síndicos, porteiros, administradoras e o código-fonte.
- **Navegabilidade e Produtividade:** Localização imediata de endpoints, tabelas e regras de qualquer fluxo em segundos.
- **Redução de Código Duplicado:** Menos redundância de `service.py`, `schemas.py` e rotas genéricas.
- **Isolamento de Mudanças de Hardware:** Fabricantes de catracas ou leitoras faciais podem ser alterados ou adicionados em `controle_acesso/` sem impactar `identidade_cadastro/` ou `portaria/`.
- **Performance no Frontend:** O Lazy Loading por Bounded Context assegura bundles leves e carregamento veloz no PWA.

### Pontos de Atenção / Trade-offs
- **Comunicação Interdomínios:** Serviços de domínios distintos não devem criar importações circulares acopladas; a comunicação deve ocorrer via contratos públicos de API ou eventos de domínio assíncronos.
- **Padronização Sem Acentuação:** Arquivos e diretórios em português devem utilizar estritamente caracteres ASCII minúsculos (ex: `manutencao`, `comunicacao`, `areas_comuns`).

## Referências

- [docs/decisoes/Estrutura.md](Estrutura.md) — Árvore canônica e detalhada de diretórios do Backend e Frontend
- [ADR-001: Governança e Stack Tecnológica](ADR-001-documentacao-e-stack-tecnologica.md)
- [ADR-010: Nomenclatura em pt-BR](ADR-010-nomenclatura-pt-br.md)
- [docs/funcionalidades/MAPA.md](../funcionalidades/MAPA.md) — Mapa arquitetural e matriz de rastreabilidade dos Bounded Contexts