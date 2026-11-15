# Bounded Context: Condomínio (`condominio`)

Este bounded context é responsável pela representação estrutural, física e institucional do condomínio, dividindo-se em 4 submódulos canônicos desacoplados:
1. **Branding & Institucional**: Dados cadastrais do empreendimento (razão social, CNPJ, endereço completo, contato da administração), personalização de identidade visual e administração multi-condomínio.
2. **Blocos & Unidades**: Divisões estruturais (blocos, torres, andares), unidades habitacionais/comerciais privativas com metragem e importação CSV em lote.
3. **Vagas de Garagem**: Demarcação de vagas, tipologias veiculares (carro, moto, PCD, visitante), proteção contra intempéries (coberta/descoberta) e alocação vinculada a unidades privativas.
4. **Áreas Comuns**: Inventário de espaços compartilhados (salões de festas, churrasqueiras, piscinas, academias), capacidade máxima de lotação e parâmetros operacionais de reserva.

---

## 1. Responsabilidade dos Submódulos

- **`branding` (Institucional & Multi-tenant Admin)**: Dados jurídicos e cadastrais do condomínio, gestão multi-tenant de instâncias, regras operacionais e customização de tema e branding.
- **`blocos_unidades`**: Hierarquia física vertical e horizontal (torres, andares, metragens, tipologias e numeração).
- **`vagas`**: Demarcação do estacionamento, controle de cobertura e vinculação privativa ou rotativa às unidades.
- **`areas_comuns`**: Espaços de convivência com horários de funcionamento, limites de lotação e taxas de utilização.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [ADR-013: Organização de Diretórios](../../decisoes/ADR-013-organizacao-diretorios.md), cada submódulo adota a **Regra Canônica de 4 Arquivos**:

### Backend (`backend/app/modules/condominio/`)
```text
condominio/
├── __init__.py
├── router.py                  # Agregador central dos sub-roteadores do BC02
├── branding/                  # Submódulo: Dados institucionais, branding e multi-condomínio
│   ├── router.py
│   ├── models.py              # Condominio, Inquilino
│   ├── schemas.py
│   └── service.py             # BrandingService
├── blocos_unidades/           # Submódulo: Torres e Unidades privativas
│   ├── router.py
│   ├── models.py              # Bloco, Unidade
│   ├── schemas.py
│   └── service.py             # BlocosUnidadesService
├── vagas/                     # Submódulo: Vagas de garagem e estacionamento
│   ├── router.py
│   ├── models.py              # VagaGaragem
│   ├── schemas.py
│   └── service.py             # VagasService
├── areas_comuns/              # Submódulo: Espaços de convivência e lazer
│   ├── router.py
│   ├── models.py              # AreaComum
│   ├── schemas.py
│   └── service.py             # AreaComumService
└── estrutura/                 # Fachada retrocompatível transitória
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/condominio/`)
```text
condominio/
├── components/
│   ├── branding/
│   │   └── condominio-admin.component.ts       # Gestão institucional, branding e multi-condomínio
│   ├── blocos-unidades/
│   │   ├── bloco-unidade-list.component.ts     # Visualização predial hierárquica (torres e unidades)
│   │   ├── block-form.component.ts             # Cadastro de bloco/torre
│   │   └── unit-form.component.ts              # Cadastro de unidade habitacional
│   ├── vagas/
│   │   └── vaga-list.component.ts              # Demarcação e gestão de vagas de garagem
│   └── areas-comuns/
│       └── areas-comuns.component.ts           # Gestão de áreas e regras operacionais
├── services/
│   ├── branding.service.ts                     # Chamadas REST de branding/institucional
│   ├── bloco-unidade.service.ts                # Chamadas REST de blocos e unidades
│   ├── vagas.service.ts                        # Chamadas REST de garagens
│   └── condominio.service.ts                   # Facade unificada (retrocompatibilidade)
├── models/
│   └── condominio.model.ts                     # Interfaces TypeScript
└── condominio.routes.ts                        # Roteamento por submódulo
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `inquilino`: Tenant/Administradora raiz.
- `condominio`: Empreendimento físico/jurídico (`id`, `inquilino_id`, `nome`, `razao_social`, `cnpj`, `logradouro`, `cidade`, `uf`, `configuracoes` JSONB).
- `bloco`: Divisão estrutural (`id`, `condominio_id`, `nome`, `descricao`, `ordem`).
- `unidade`: Unidade autônoma (`id`, `condominio_id`, `bloco_id`, `identificacao`, `andar`, `tipo`, `area_privativa`).
- `vaga_garagem`: Vaga de estacionamento (`id`, `condominio_id`, `unidade_id`, `identificacao`, `tipo`, `coberta`).
- `area_comum`: Espaço compartilhado (`id`, `condominio_id`, `nome`, `descricao`, `capacidade`, `taxa_reserva`, `requer_aprovacao`, `ativo`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Submódulo | Método | Endpoint | Descrição |
| :--- | :--- | :--- | :--- |
| **Branding** | `GET` | `/api/v1/condominio/info` | Dados cadastrais do condomínio |
| **Branding** | `PUT` | `/api/v1/condominio/info` | Atualização cadastral |
| **Branding** | `GET` | `/api/v1/condominio/configuracoes` | Parâmetros e identidade visual |
| **Branding** | `GET` | `/api/v1/condominio/todos` | Listagem multi-tenant de condomínios |
| **Branding** | `POST` | `/api/v1/condominio/novo` | Cadastro de nova instância condominial |
| **Blocos & Unidades** | `GET` | `/api/v1/condominio/blocos` | Listagem de blocos e torres |
| **Blocos & Unidades** | `POST` | `/api/v1/condominio/blocos` | Criação de bloco |
| **Blocos & Unidades** | `GET` | `/api/v1/condominio/unidades` | Listagem de unidades |
| **Blocos & Unidades** | `POST` | `/api/v1/condominio/unidades` | Criação de unidade privativa |
| **Blocos & Unidades** | `POST` | `/api/v1/condominio/unidades/importar` | Carga de unidades via arquivo CSV |
| **Vagas** | `GET` | `/api/v1/condominio/vagas` | Catálogo de vagas de garagem |
| **Vagas** | `POST` | `/api/v1/condominio/vagas` | Cadastro de demarcação de vaga |
| **Áreas Comuns** | `GET` | `/api/v1/condominio/areas-comuns` | Listagem de espaços comuns |
| **Áreas Comuns** | `POST` | `/api/v1/condominio/areas-comuns` | Cadastro de espaço compartilhado |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-006: Isolamento por Condomínio com RLS no PostgreSQL](../../decisoes/ADR-006-isolamento-rls-postgresql.md)
  - [ADR-010: Nomenclatura em pt-BR](../../decisoes/ADR-010-nomenclatura-pt-br.md)
  - [ADR-013: Organização de Diretórios](../../decisoes/ADR-013-organizacao-diretorios.md)
