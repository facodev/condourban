# Matriz de Rastreabilidade — 9 Bounded Contexts

Este documento mapeia todos os artefatos técnicos, especificações funcionais, ADRs e scripts de banco de dados para os seus respectivos **Bounded Contexts** consolidados em [Estrutura.md](../decisoes/Estrutura.md).

---

## 1. Especificações Funcionais e Domínios → Bounded Contexts

| Bounded Context | Documento do Domínio | Especificação Funcional | Submódulo / Destaque |
| :--- | :--- | :--- | :--- |
| `01_identidade_cadastro` | [identidade-cadastro.md](01_identidade_cadastro/identidade-cadastro.md) | [onboarding-e-conta.md](01_identidade_cadastro/onboarding-e-conta.md) | Criação de conta, auto-onboarding seguro com Magic Link (15 min) e revogação preventiva anti-scraping LGPD |
| `01_identidade_cadastro` | [identidade-cadastro.md](01_identidade_cadastro/identidade-cadastro.md) | [cadastro-morador-solicitacao.md](01_identidade_cadastro/cadastro-morador-solicitacao.md) | Fila de auto-onboarding e validação documental com selfie |
| `01_identidade_cadastro` | [identidade-cadastro.md](01_identidade_cadastro/identidade-cadastro.md) | [veiculos-e-pets.md](01_identidade_cadastro/veiculos-e-pets.md) | Cadastro de veículos (placas) e animais da unidade |
| `02_condominio` | [condominio.md](02_condominio/condominio.md) | [estrutura-fisica.md](02_condominio/estrutura-fisica.md) | Blocos, unidades, garagens e catálogo de áreas comuns |
| `02_condominio` | [condominio.md](02_condominio/condominio.md) | [configuracao-condominio.md](02_condominio/configuracao-condominio.md) | Branding institucional e regras/horários de convivência |
| `03_controle_acesso` | [controle-acesso.md](03_controle_acesso/controle-acesso.md) | [biometria-facial-intelbras.md](03_controle_acesso/biometria-facial-intelbras.md) | Leitoras faciais e sincronização de biometria via adapter |
| `03_controle_acesso` | [controle-acesso.md](03_controle_acesso/controle-acesso.md) | [credenciais-e-dispositivos.md](03_controle_acesso/credenciais-e-dispositivos.md) | Tags RFID, QR codes dinâmicos e antenas LPR |
| `03_controle_acesso` | [controle-acesso.md](03_controle_acesso/controle-acesso.md) | [acionamentos-e-eventos.md](03_controle_acesso/acionamentos-e-eventos.md) | Abertura remota in-app com geofence e trilha de passagens |
| `04_portaria` | [portaria.md](04_portaria/portaria.md) | [atendimento-visitantes-prestadores.md](04_portaria/atendimento-visitantes-prestadores.md) | Terminal da guarita — papel `PORTEIRO`/`PORTARIA` libera entrada (sem encomendas) |
| `04_portaria` | [portaria.md](04_portaria/portaria.md) | [correspondencias-encomendas.md](04_portaria/correspondencias-encomendas.md) | Papel `ENCOMENDAS`: recebimento com foto, notificação e baixa com PIN |

| `04_portaria` | [portaria.md](04_portaria/portaria.md) | [agendamento-mudancas.md](04_portaria/agendamento-mudancas.md) | Agendamento de mudança, elevador de serviço e vistorias |
| `04_portaria` | [portaria.md](04_portaria/portaria.md) | [achados-e-perdidos.md](04_portaria/achados-e-perdidos.md) | Mural de itens esquecidos, custódia e termo de restituição |
| `05_reservas` | [reservas.md](05_reservas/reservas.md) | [agendamento-espacos.md](05_reservas/agendamento-espacos.md) | Calendário interativo de áreas comuns, regras e taxas |
| `05_reservas` | [reservas.md](05_reservas/reservas.md) | [lista-convidados.md](05_reservas/lista-convidados.md) | Lista de convidados vinculada à reserva e portaria |
| `05_reservas` | [reservas.md](05_reservas/reservas.md) | [vistorias-checkin-checkout.md](05_reservas/vistorias-checkin-checkout.md) | Vistoria fotográfica pré e pós-uso e liberação de caução |
| `06_comunicacao` | [comunicacao.md](06_comunicacao/comunicacao.md) | [mural-comunicados.md](06_comunicacao/mural-comunicados.md) | Avisos oficiais e comunicados urgentes com leitura confirmada |
| `06_comunicacao` | [comunicacao.md](06_comunicacao/comunicacao.md) | [ocorrencias-livro.md](06_comunicacao/ocorrencias-livro.md) | Livro de ocorrências unificado (morador/portaria/gestão) e sigilo |
| `06_comunicacao` | [comunicacao.md](06_comunicacao/comunicacao.md) | [enquetes-consultas.md](06_comunicacao/enquetes-consultas.md) | Enquetes rápidas da comunidade e apuração em tempo real |
| `06_comunicacao` | [comunicacao.md](06_comunicacao/comunicacao.md) | [mural-comunidade.md](06_comunicacao/mural-comunidade.md) | Classificados internos e avisos comunitários |
| `06_comunicacao` | [comunicacao.md](06_comunicacao/comunicacao.md) | [canal-fale-conosco.md](06_comunicacao/canal-fale-conosco.md) | Mensageria privada direta morador ↔ administração |
| `07_governanca` | [governanca.md](07_governanca/governanca.md) | [assembleias-virtuais.md](07_governanca/assembleias-virtuais.md) | Editais, procurações, votações ao vivo e atas digitais |
| `07_governanca` | [governanca.md](07_governanca/governanca.md) | [repositorio-documentos.md](07_governanca/repositorio-documentos.md) | Convenção, regimento interno, apólices e contratos |
| `08_financeiro` | [financeiro.md](08_financeiro/financeiro.md) | [cobranca-e-boletos.md](08_financeiro/cobranca-e-boletos.md) | Boletos, Pix dinâmico instantâneo, 2ª via e conciliação |
| `08_financeiro` | [financeiro.md](08_financeiro/financeiro.md) | [prestacao-contas-e-despesas.md](08_financeiro/prestacao-contas-e-despesas.md) | Balancetes mensais, notas fiscais e parecer do conselho |
| `08_financeiro` | [financeiro.md](08_financeiro/financeiro.md) | [acordos-e-inadimplencia.md](08_financeiro/acordos-e-inadimplencia.md) | Simulação e termos de confissão/parcelamento de dívidas |
| `09_manutencao` | [manutencao.md](09_manutencao/manutencao.md) | [chamados-e-ordens-servico.md](09_manutencao/chamados-e-ordens-servico.md) | Chamados corretivos, triagem e OS do zelador com fotos |
| `09_manutencao` | [manutencao.md](09_manutencao/manutencao.md) | [manutencao-preventiva-pmo.md](09_manutencao/manutencao-preventiva-pmo.md) | Plano de Manutenção Preventiva Obrigatória (PMO / NBR 5674) |
| `10_transversal_plataforma` | [transversal.md](10_transversal_plataforma/transversal.md) | [perfis-e-permissoes.md](10_transversal_plataforma/perfis-e-permissoes.md) | Matriz RBAC — inclui `ENCOMENDAS` separado de `PORTEIRO`/`PORTARIA` |

| `10_transversal_plataforma` | [transversal.md](10_transversal_plataforma/transversal.md) | [central-notificacoes.md](10_transversal_plataforma/central-notificacoes.md) | Motor multicanal de notificações (Push VAPID, E-mail, In-App) |
| `10_transversal_plataforma` | [transversal.md](10_transversal_plataforma/transversal.md) | [planos-e-entitlements.md](10_transversal_plataforma/planos-e-entitlements.md) | Catálogo de planos SaaS e entitlements (ADR-011) |

---

## 2. Decisões Arquiteturais (ADRs) → Bounded Contexts

| ADR | Tema | Bounded Context(s) |
| :--- | :--- | :--- |
| [ADR-002: Stack Python + Angular](../decisoes/ADR-002-stack-python-angular.md) | Stack padrão FastAPI e Angular | `transversal` |
| [ADR-003: UI, Tailwind CSS v4 + Material 3 e PWA](../decisoes/ADR-003-ui-estilizacao-e-portabilidade-web.md) | Arquitetura de estilos CSS-first, separação de componentes e diretrizes de design | Todos os 9 contextos + `transversal` |
| [ADR-004: Intelbras Facial e Pré-Cadastro](../decisoes/ADR-004-integracao-intelbras-facial.md) | Reconhecimento facial no controle de acesso | `controle_acesso` + `portaria` |
| [ADR-005: Persistência PostgreSQL](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md) | Banco relacional oficial | `transversal` |
| [ADR-006: Isolamento RLS PostgreSQL](../decisoes/ADR-006-isolamento-rls-postgresql.md) | Multi-tenancy por condomínio via RLS | `transversal` + `condominio` |
| [ADR-007: Autenticação JWT e Google](../decisoes/ADR-007-autenticacao-jwt-aplicacao.md) | Login JWT e SSO com Google | `identidade_cadastro` + `transversal` |
| [ADR-008: Separação Pessoa e Usuário](../decisoes/ADR-008-pessoa-e-usuario.md) | Pessoa física distinta de conta de acesso | `identidade_cadastro` |
| [ADR-009: Idempotência em Integrações](../decisoes/ADR-009-idempotencia-integracoes.md) | Sync confiável de hardware e webhooks | `controle_acesso` |
| [ADR-010: Nomenclatura em pt-BR](../decisoes/ADR-010-nomenclatura-pt-br.md) | Nomenclatura brasileira de negócio no schema | Todos os 9 contextos |
| [ADR-011: Planos e Funcionalidades](../decisoes/ADR-011-planos-e-funcionalidades.md) | Tarifação e planos | `financeiro` |
| [ADR-012: Backend FastAPI](../decisoes/ADR-012-backend-fastapi.md) | Estrutura modular da API | Todos os 9 contextos |
| [ADR-013: Organização de Diretórios](../decisoes/ADR-013-organizacao-diretorios.md) | Organização por Bounded Contexts | Todos os 9 contextos |

---

## 3. Schemas de Banco de Dados (`docs/sql/`) → Bounded Contexts

| Script SQL | Bounded Context(s) Correspondente(s) | Tabelas Principais |
| :--- | :--- | :--- |
| [001-extensoes-e-tipos.sql](../sql/001-extensoes-e-tipos.sql) | `transversal` | Enums de negócio, UUID e funções base |
| [002-condominio.sql](../sql/002-condominio.sql) | `condominio` | `inquilino`, `condominio`, `bloco`, `unidade`, `vaga_garagem`, `area_comum` |
| [003-identidade-cadastro.sql](../sql/003-identidade-cadastro.sql) | `identidade_cadastro` | `pessoa`, `usuario`, `membro_condominio`, `ocupacao_unidade`, `convite_cadastro_morador`, `solicitacao_cadastro_morador`, `veiculo`, `pet` |
| [004-controle-acesso.sql](../sql/004-controle-acesso.sql) | `controle_acesso` | `integracao_provedor`, `dispositivo_acesso`, `credencial_acesso`, `autorizacao_acesso`, `evento_acesso`, `sincronizacao_acesso` |
| [005-portaria.sql](../sql/005-portaria.sql) | `portaria` | `visitante`, `convite_visitante`, `prestador`, `autorizacao_prestador`, `registro_visita`, `encomenda`, `agendamento_mudanca`, `item_perdido` |
| [006-reservas.sql](../sql/006-reservas.sql) | `reservas` | `reserva`, `convidado_reserva`, `vistoria_reserva` |
| [007-comunicacao.sql](../sql/007-comunicacao.sql) | `comunicacao` | `comunicado`, `leitura_comunicado`, `ocorrencia`, `historico_ocorrencia`, `enquete`, `item_comunidade`, `mensagem_fale_conosco` |
| [008-governanca.sql](../sql/008-governanca.sql) | `governanca` | `assembleia`, `pauta_assembleia`, `voto_assembleia`, `procuracao_assembleia`, `ata_assembleia`, `pasta_documento`, `documento` |
| [009-financeiro.sql](../sql/009-financeiro.sql) | `financeiro` | `cobranca_condominial`, `despesa_condominial`, `termo_acordo`, `medicao_individual` |
| [010-manutencao.sql](../sql/010-manutencao.sql) | `manutencao` | `chamado_manutencao`, `ordem_servico`, `item_preventiva_pmo`, `registro_inspecao_pmo` |
| [011-transversal-e-auditoria.sql](../sql/011-transversal-e-auditoria.sql) | `transversal` | `evento_auditoria`, `evento_uso` |
| [012-rls.sql](../sql/012-rls.sql) | `transversal` | Políticas de Row Level Security (RLS) por `condominio_id` |
| [013-saas-planos-e-funcionalidades.sql](../sql/013-saas-planos-e-funcionalidades.sql) | `transversal` / `financeiro` | `funcionalidade`, `plano`, `plano_funcionalidade`, `assinatura`, `condominio_funcionalidade` |
| [014-seeds.sql](../sql/014-seeds.sql) | `transversal` | Seeds de catálogo, motivos e planos |
