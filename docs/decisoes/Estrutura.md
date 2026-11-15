# Estrutura de Diretórios do Projeto

Este documento descreve a organização padronizada das árvores de diretórios do **Backend** (FastAPI) e do **Frontend** (Angular PWA), formalizada no **[ADR-013: Organização de Diretórios por Bounded Contexts e Consolidação de Subdomínios](ADR-013-organizacao-diretorios.md)**.

---

## 1. Estrutura de Diretórios do Backend

```text
backend/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── core/                          # Infraestrutura base, segurança e configurações transversais
│   │   ├── __init__.py
│   │   ├── config.py                  # Variáveis de ambiente
│   │   ├── database.py                # Conexão assíncrona SQLAlchemy (PostgreSQL / RLS)
│   │   ├── security.py                # Hashing (bcrypt) e JWT
│   │   ├── dependencies.py            # get_db, tenant, current_user
│   │   └── exceptions.py              # Tratamento unificado de erros
│   │
│   ├── modulos/                       # 9 Bounded Contexts Simplificados
│   │   │
│   │   ├── identidade_cadastro/       # 1. Identidade e Cadastro
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── pessoas/               # Dados civis e documentos
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── usuarios/              # Contas de acesso, membros (perfis) e ocupações (vínculos)
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── onboarding/            # Solicitações de cadastro, aprovação e biometria
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── veiculos_pets/         # Veículos e animais domésticos da unidade
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── condominio/                # 2. Estrutura Física do Condomínio
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── estrutura/             # Condomínio, blocos, unidades e vagas de garagem
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── areas_comuns/          # Cadastro de salões, quiosques, churrasqueiras
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── controle_acesso/           # 3. Controle de Acesso e Hardware/IoT
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── dispositivos/          # Provedores, catracas, leitoras faciais, cancelas e sincronização
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── credenciais/           # Tags RFID, biometria e regras de autorização
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── eventos_acesso/        # Histórico e logs de passagens
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── portaria/                  # 4. Portaria e Atendimento
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── atendimento/           # Visitantes, prestadores, hóspedes e convites prévios
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── encomendas/            # Recebimento, foto e retirada de pacotes
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── reservas/                  # 5. Reservas de Espaços Comuns
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── agendamentos/          # Reservas e gestão da lista de convidados
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── vistorias/             # Vistoria pré/pós uso e controle de caução
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── comunicacao/               # 6. Comunicação e Convivência
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── mensageria/            # Comunicados oficiais e canal direto morador-gestão
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── ocorrencias/           # Ocorrências unificadas (morador e livro da portaria)
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── mural_social/          # Enquetes, achados/perdidos e classificados
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── governanca/                # 7. Governança e Administração Legal
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── assembleias/           # Editais, pautas, votação digital e atas
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── seguranca_auditoria/   # Papéis/permissões administrativas e logs de auditoria
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   ├── financeiro/                # 8. Financeiro e Tarifação
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── cobrancas_acordos/     # Boletos, Pix, conciliação e renegociações
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── despesas_medicoes/     # Prestação de contas e medições individuais (água/gás)
│   │   │       ├── router.py
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       └── service.py
│   │   │
│   │   └── manutencao/                # 9. Manutenção e Operação Predial
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── chamados_servicos/     # Chamados de reparo, agendamentos e ordens de serviço
│   │       │   ├── router.py
│   │       │   ├── models.py
│   │       │   ├── schemas.py
│   │       │   └── service.py
│   │       └── plano_inventario/      # PMO preventivo e inventário/patrimônio
│   │           ├── router.py
│   │           ├── models.py
│   │           ├── schemas.py
│   │           └── service.py
│   │
│   └── main.py                        # Ponto de entrada FastAPI
├── tests/
├── requirements.txt
├── Dockerfile
└── alembic.ini
```

---

## 2. Estrutura de Diretórios do Frontend

```text
frontend/
├── src/
│   ├── app/
│   │   ├── core/                      # Serviços singleton, segurança, autenticação e PWA
│   │   │   ├── guards/                # Proteção e regras de navegação
│   │   │   │   ├── auth.guard.ts      # Garante usuário logado
│   │   │   │   ├── papel.guard.ts     # Valida RBAC (síndico, morador, porteiro)
│   │   │   │   └── unidade.guard.ts   # Garante contexto de condomínio/unidade selecionado
│   │   │   ├── interceptors/          # Interceptação de tráfego HTTP
│   │   │   │   ├── token.interceptor.ts   # Injeta Bearer JWT e cabeçalhos de tenant
│   │   │   │   └── error.interceptor.ts   # Captura global de 401, 403, 500 e offline
│   │   │   ├── services/              # Infraestrutura global
│   │   │   │   ├── pwa-sync.service.ts    # Monitora status offline, sync e prompt de instalação
│   │   │   │   ├── session.service.ts     # Armazenamento e estado do usuário/perfil atual
│   │   │   │   └── notification.service.ts # Push notifications do PWA / Service Worker
│   │   │   └── models/                # Tipagens e enums transversais do sistema
│   │   │       ├── usuario-sessao.model.ts
│   │   │       └── resposta-api.model.ts
│   │   │
│   │   ├── shared/                    # Componentes de interface, diretivas e pipes reutilizáveis
│   │   │   ├── components/            # Componentes sem regra de negócio
│   │   │   │   ├── confirm-dialog/    # Modal genérico de confirmação
│   │   │   │   ├── data-table/        # Tabela paginada com ordenação
│   │   │   │   ├── status-badge/      # Tag visual para status (pendente, aprovado, etc.)
│   │   │   │   └── upload-foto/       # Componente de captura/upload (câmera PWA)
│   │   │   ├── pipes/                 # Formatadores específicos brasileiros
│   │   │   │   ├── cpf.pipe.ts
│   │   │   │   ├── placa.pipe.ts
│   │   │   │   ├── moeda.pipe.ts
│   │   │   │   ├── phone.pipe.ts
│   │   │   │   └── data-format.pipe.ts
│   │   │   └── ui/                    # Layouts padrão (cards, botões, modais)
│   │   │
│   │   ├── features/                  # 9 Bounded Contexts Consolidados (Rotas com Lazy Loading)
│   │   │   │
│   │   │   ├── auth/                  # Autenticação e Entrada no Sistema
│   │   │   │   ├── components/        # login, recuperar-senha, callback-social
│   │   │   │   ├── services/          # auth.service.ts
│   │   │   │   └── auth.routes.ts
│   │   │   │
│   │   │   ├── identidade_cadastro/   # 1. Identidade e Cadastro
│   │   │   │   ├── components/
│   │   │   │   │   ├── pessoas/       # Edição de dados civis e perfil pessoal
│   │   │   │   │   ├── usuarios/      # Gestão de acessos, membros (papéis) e ocupações (vínculos)
│   │   │   │   │   ├── onboarding/    # Solicitações de cadastro pendentes e aprovação
│   │   │   │   │   └── veiculos-pets/ # Gestão de veículos e animais da unidade
│   │   │   │   ├── services/
│   │   │   │   └── identidade-cadastro.routes.ts
│   │   │   │
│   │   │   ├── condominio/            # 2. Estrutura Física
│   │   │   │   ├── components/
│   │   │   │   │   ├── estrutura/     # Mapa do condomínio: blocos, unidades e vagas
│   │   │   │   │   └── areas-comuns/  # Cadastro de salões, quiosques e churrasqueiras
│   │   │   │   ├── services/
│   │   │   │   └── condominio.routes.ts
│   │   │   │
│   │   │   ├── controle_acesso/       # 3. Hardware e IoT
│   │   │   │   ├── components/
│   │   │   │   │   ├── dispositivos/  # Painel de catracas, antenas RFID, LPR e status de sync
│   │   │   │   │   ├── credenciais/   # Cadastro de tags, biometria e regras de horário
│   │   │   │   │   └── eventos/       # Log em tempo real das passagens
│   │   │   │   ├── services/
│   │   │   │   └── controle-acesso.routes.ts
│   │   │   │
│   │   │   ├── portaria/              # 4. Portaria e Atendimento
│   │   │   │   ├── components/
│   │   │   │   │   ├── atendimento/   # Fila da portaria: visitantes, prestadores, hóspedes e convites
│   │   │   │   │   └── encomendas/    # Recebimento de pacotes com foto e baixa por código
│   │   │   │   ├── services/
│   │   │   │   └── portaria.routes.ts
│   │   │   │
│   │   │   ├── reservas/              # 5. Reservas e Espaços Comuns
│   │   │   │   ├── components/
│   │   │   │   │   ├── agendamentos/  # Calendário de reservas e lista de convidados embutida
│   │   │   │   │   └── vistorias/     # Vistorias pré/pós evento e conferência de caução
│   │   │   │   ├── services/
│   │   │   │   └── reservas.routes.ts
│   │   │   │
│   │   │   ├── comunicacao/           # 6. Comunicação e Convivência
│   │   │   │   ├── components/
│   │   │   │   │   ├── mensageria/    # Feed de comunicados oficiais e chat morador-gestão
│   │   │   │   │   ├── ocorrencias/   # Ocorrências unificadas (morador e registros da portaria)
│   │   │   │   │   └── mural-social/  # Enquetes, achados/perdidos e classificados
│   │   │   │   ├── services/
│   │   │   │   └── comunicacao.routes.ts
│   │   │   │
│   │   │   ├── governanca/            # 7. Governança e Administração Legal
│   │   │   │   ├── components/
│   │   │   │   │   ├── assembleias/   # Convocação, pauta, votação digital ao vivo e atas
│   │   │   │   │   └── seguranca-auditoria/ # Matriz de permissões (RBAC) e logs de auditoria
│   │   │   │   ├── services/
│   │   │   │   └── governanca.routes.ts
│   │   │   │
│   │   │   ├── financeiro/            # 8. Financeiro e Tarifação
│   │   │   │   ├── components/
│   │   │   │   │   ├── cobrancas-acordos/ # Emissão de 2ª via de boleto, Pix e acordos
│   │   │   │   │   └── despesas-medicoes/ # Balancetes e gráficos de consumo individual (água/gás)
│   │   │   │   ├── services/
│   │   │   │   └── financeiro.routes.ts
│   │   │   │
│   │   │   └── manutencao/            # 9. Manutenção Predial e Ativos
│   │   │       ├── components/
│   │   │       │   ├── chamados-servicos/ # Abertura de chamados com foto e ordens de serviço
│   │   │       │   └── plano-inventario/  # Cronograma preventivo (PMO) e patrimônio
│   │   │       ├── services/
│   │   │       └── manutencao.routes.ts
│   │   │
│   │   ├── app.component.html         # Shell com barra de navegação responsiva (mobile/desktop)
│   │   ├── app.component.ts           # Lógica do container principal
│   │   ├── app.config.ts              # Provedores Angular (HttpClient, ServiceWorker, Router)
│   │   └── app.routes.ts              # Mapeamento raiz com Lazy Loading para os 9 módulos
│   │
│   ├── assets/                        # Ícones do PWA (192x192, 512x512), splash screens e sons
│   ├── environments/                  # Variáveis de ambiente (API URL, WebSocket, etc.)
│   ├── manifest.webmanifest           # Configuração de instalação do PWA
│   ├── ngsw-config.json               # Configuração de cache e rotas offline do Angular Service Worker
│   └── styles.scss                    # Variáveis de cor, tipografia e reset CSS
│
├── angular.json
├── package.json
└── tsconfig.json
```