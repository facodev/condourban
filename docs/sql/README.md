# Schema PostgreSQL (DDL de Referência Canônico)

Modelo de dados relacional canônico para **staging/produção** (PostgreSQL). Em **desenvolvimento/testes** a escada de persistência segue SQLite → Postgres ([ADR-005](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md)).  
Políticas de Row Level Security (RLS) e tipos específicos aplicam-se estritamente ao PostgreSQL.

O schema foi modularizado rigorosamente de acordo com os **9 Bounded Contexts** do projeto, formalizados no **[ADR-013: Organização de Diretórios por Bounded Contexts](../decisoes/ADR-013-organizacao-diretorios.md)**, no **[Estrutura.md](../decisoes/Estrutura.md)** e no **[15-modelo-dados-postgresql.md](../plano/15-modelo-dados-postgresql.md)**.

---

## 1. Ordem de Execução dos Scripts

Executar rigorosamente na ordem abaixo em um banco de dados novo:

```text
001-extensoes-e-tipos.sql
002-condominio.sql
003-identidade-cadastro.sql
004-controle-acesso.sql
005-portaria.sql
006-reservas.sql
007-comunicacao.sql
008-governanca.sql
009-financeiro.sql
010-manutencao.sql
011-transversal-e-auditoria.sql
012-rls.sql
013-saas-planos-e-funcionalidades.sql
014-seeds.sql
```

---

## 2. Conteúdo e Mapeamento por Bounded Context

| Arquivo | Bounded Context (`pt-BR`) | Tabelas / Entidades Principais |
| :--- | :--- | :--- |
| `001-extensoes-e-tipos.sql` | `transversal` | Extensões `pgcrypto`, `citext`; enums de status, vínculo, documentos, facial, veículos, pets, manutenção e mudanças. |
| `002-condominio.sql` | `condominio` | `inquilino`, `condominio`, `bloco`, `unidade`, `vaga_garagem`, `area_comum`. |
| `003-identidade-cadastro.sql` | `identidade_cadastro` | `pessoa`, `usuario`, `membro_condominio`, `ocupacao_unidade`, `documento_identificacao`, `convite_cadastro_morador`, `solicitacao_cadastro_morador`, `documento_cadastro`, `verificacao_facial`, `historico_analise_cadastro`, `motivo_correcao_cadastro`, `veiculo`, `pet`. |
| `004-controle-acesso.sql` | `controle_acesso` | `integracao_provedor`, `dispositivo_acesso`, `credencial_acesso`, `autorizacao_acesso`, `evento_acesso`, `sincronizacao_acesso`. |
| `005-portaria.sql` | `portaria` | `visitante`, `convite_visitante`, `prestador`, `autorizacao_prestador`, `registro_visita`, `encomenda`, `evento_encomenda`, `agendamento_mudanca`, `item_perdido`. |
| `006-reservas.sql` | `reservas` | `reserva`, `convidado_reserva`, `vistoria_reserva`. |
| `007-comunicacao.sql` | `comunicacao` | `comunicado`, `leitura_comunicado`, `ocorrencia` (unificada: morador/portaria/gestão), `historico_ocorrencia`, `enquete`, `opcao_enquete`, `voto_enquete`, `item_comunidade`, `mensagem_fale_conosco`. |
| `008-governanca.sql` | `governanca` | `assembleia`, `pauta_assembleia`, `participante_assembleia`, `procuracao_assembleia`, `votacao_assembleia`, `opcao_votacao`, `voto_assembleia`, `ata_assembleia`, `pasta_documento`, `documento`. |
| `009-financeiro.sql` | `financeiro` | `cobranca_condominial`, `despesa_condominial`, `termo_acordo`, `medicao_individual`. |
| `010-manutencao.sql` | `manutencao` | `chamado_manutencao`, `ordem_servico`, `item_preventiva_pmo`, `registro_inspecao_pmo`. |
| `011-transversal-e-auditoria.sql` | `transversal` | `evento_auditoria`, `evento_uso`. |
| `012-rls.sql` | `transversal` | Função `obter_condominio_sessao()` e ativação de Row Level Security (RLS) com política `isolamento_condominio` em todas as 44 tabelas escopadas por condomínio. |
| `013-saas-planos-e-funcionalidades.sql` | `transversal` / `financeiro` | `funcionalidade`, `plano`, `plano_funcionalidade`, `assinatura`, `condominio_funcionalidade`, função `funcionalidade_habilitada()`. |
| `014-seeds.sql` | `transversal` | Seeds de catálogo: motivos de correção cadastral, matriz de planos (Starter, Essencial, Acesso, Administradora) e mapeamento de entitlements. |

---

## 3. Contrato RLS (Row Level Security)

Após autenticar o usuário via JWT e validar sua membresia no condomínio ativo, o backend FastAPI executa na transação:

```sql
SET LOCAL app.condominio_id = '<uuid-do-condominio>';
```

- A função `obter_condominio_sessao()` extrai o valor de `app.condominio_id`.
- O `condominio_id` enviado pelo cliente **nunca autoriza o acesso isoladamente**; a validação sempre ocorre na camada de segurança do servidor ([ADR-006](../decisoes/ADR-006-isolamento-rls-postgresql.md)).

---

## 4. Decisões Arquiteturais Vinculadas (ADRs)

- [ADR-001: Governança e Stack Tecnológica](../decisoes/ADR-001-documentacao-e-stack-tecnologica.md)
- [ADR-004: Integração Intelbras Facial e Pré-Cadastro](../decisoes/ADR-004-integracao-intelbras-facial.md)
- [ADR-005: Persistência PostgreSQL](../decisoes/ADR-005-persistencia-sqlite-para-postgres.md)
- [ADR-006: Isolamento RLS no PostgreSQL](../decisoes/ADR-006-isolamento-rls-postgresql.md)
- [ADR-007: Autenticação JWT e Google](../decisoes/ADR-007-autenticacao-jwt-aplicacao.md)
- [ADR-008: Separação de Pessoa e Usuário](../decisoes/ADR-008-pessoa-e-usuario.md)
- [ADR-009: Idempotência em Integrações e Webhooks](../decisoes/ADR-009-idempotencia-integracoes.md)
- [ADR-010: Nomenclatura em pt-BR](../decisoes/ADR-010-nomenclatura-pt-br.md)
- [ADR-011: Planos e Funcionalidades SaaS](../decisoes/ADR-011-planos-e-funcionalidades.md)
- [ADR-012: Backend FastAPI](../decisoes/ADR-012-backend-fastapi.md)
- [ADR-013: Organização por Bounded Contexts](../decisoes/ADR-013-organizacao-diretorios.md)

---

## 5. Status

| Campo | Valor |
| :--- | :--- |
| **Status** | `canônico vivo` — referência oficial de DDL do projeto |
| **Última Revisão** | 2026-10-17 — Modularização completa pelos 9 Bounded Contexts (ADR-013) e inclusão de veículos, pets, manutenção predial PMO e vistorias |
| **Escopo** | Tabelas relacionais PostgreSQL + Políticas RLS + Catálogo SaaS |
