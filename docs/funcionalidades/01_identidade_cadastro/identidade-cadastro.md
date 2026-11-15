# Bounded Context: Identidade e Cadastro (`identidade_cadastro`)

Este bounded context é o pilar fundamental de identificação civil, controle de contas, vínculos contratuais e cadastros complementares dentro do sistema.

---

## 1. Responsabilidade do Domínio

- **Pessoas**: Manutenção dos dados civis, documentos oficiais (CPF, RG, CNH), dados de contato e consentimentos da LGPD de todas as pessoas que interagem com o ecossistema condominial.
- **Usuários e Acessos**: Credenciais de login no sistema (e-mail, senha criptografada via bcrypt, vínculo federado Google OAuth2), controle de sessões e associação a perfis de permissão (RBAC).
- **Ocupações e Vínculos**: Associação formal de pessoas e usuários a unidades específicas (morador residente, proprietário residente, proprietário não residente, inquilino, dependente, funcionário particular).
- **Onboarding e Auto-Cadastro**: Solicitação de ingresso pelo morador, upload e conferência de documentos probatórios, histórico de aprovação ou rejeição pela administração com coleta biométrica inicial.
- **Veículos e Animais de Estimação (Pets)**: Cadastro dos veículos associados a vagas de garagem e animais cadastrados para segurança e bem-estar coletivo.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/identidade_cadastro/`)
```text
identidade_cadastro/
├── __init__.py
├── router.py
├── pessoas/               # Dados civis, documentos e contatos
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── usuarios/              # Contas de acesso, papéis (RBAC) e ocupações
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── onboarding/            # Solicitações pendentes, validação documental e aprovação
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── veiculos_pets/         # Veículos da unidade e animais de estimação
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/identidade_cadastro/`)
```text
identidade_cadastro/
├── components/
│   ├── pessoas/           # Edição de perfil pessoal e dados civis
│   ├── usuarios/          # Gestão de acessos e membros da equipe/condomínio
│   ├── onboarding/        # Fila de análise e aprovação de cadastros
│   └── veiculos-pets/     # Gestão visual de veículos e pets
├── services/
│   └── identidade-cadastro.service.ts
└── identidade-cadastro.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `pessoa`: Identificador único civil (`id`, `nome_completo`, `cpf`, `rg`, `email`, `telefone`, `foto_url`, `criado_em`).
- `usuario`: Conta do sistema (`id`, `pessoa_id`, `email`, `senha_hash`, `ativo`, `ultimo_login`).
- `membro_condominio`: Papéis de um usuário em um condomínio (`condominio_id`, `usuario_id`, `papel`: `sindico`, `subsindico`, `conselheiro`, `porteiro`, `zelador`, `morador`).
- `ocupacao_unidade`: Vínculo de uma pessoa a uma unidade física (`unidade_id`, `pessoa_id`, `responsavel_ocupacao_id`, `tipo_vinculo`: `proprietario`, `inquilino`, `morador`, `dependente`, `temporario`, `hospede`, `mora_no_local`, `inicio_em`, `fim_em`, `status`).

### 3.1. Regras Invariantes de Ocupação da Unidade
1. **Conflito de Posse Direta:** Se houver `INQUILINO` com status `ATIVO` na unidade, nenhum `PROPRIETARIO` pode ter `mora_no_local = TRUE`. Ao ativar um inquilino, o proprietário residente é desmarcado automaticamente para `mora_no_local = FALSE`. Tentativas manuais de marcar proprietário como morador com inquilino ativo são rejeitadas (`CONFLITO_POSSE_DIRETA`).
2. **Datas Obrigatórias para Curtos Prazos:** Vínculos do tipo `TEMPORARIO` ou `HOSPEDE` exigem obrigatoriamente preenchimento de `data_inicio` (`inicio_em`) e `data_fim` (`fim_em`).
3. **Validação de Retroatividade:** A `data_fim` (`fim_em`) deve ser estritamente maior que a `data_inicio` (`inicio_em`).
4. **Bloqueio Automático de Acesso:** Rotina diária (Cron Job / Worker CLI `rotina_expiracao_ocupacoes.py` ou procedure PG `fn_expirar_ocupacoes_vencidas`) inativa ocupações cujo prazo expirou (`fim_em < now()`), associada ao filtro preventivo em tempo real nos módulos de acesso.
5. **Dependentes Exigem Responsável Ativo Residente:** Registros do tipo `DEPENDENTE` só podem ser criados ou mantidos ativos se houver um `PROPRIETARIO` morador ou `INQUILINO` ativo residente (`mora_no_local = TRUE`) na mesma unidade. A inativação do titular responsável propaga cascade para `INATIVO` em seus dependentes órfãos.
- `solicitacao_cadastro_morador`: Workflow de entrada (`unidade_id`, `nome`, `email`, `telefone`, `documentos_anexos`, `status`: `pendente`, `aprovado`, `rejeitado`).
- `veiculo`: (`unidade_id`, `placa`, `marca_modelo`, `cor`, `vaga_id`).
- `pet`: (`unidade_id`, `nome`, `especie`, `raca`, `porte`, `vacinacao_em_dia`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/identidade/pessoas` | Listagem de pessoas com filtros de busca |
| `POST` | `/api/v1/identidade/pessoas` | Cadastro de nova pessoa física |
| `GET` | `/api/v1/identidade/usuarios` | Consulta de usuários e papéis ativos |
| `POST` | `/api/v1/identidade/usuarios` | Criação de credenciais de acesso |
| `GET` | `/api/v1/identidade/onboarding` | Fila de solicitações de entrada pendentes |
| `POST` | `/api/v1/identidade/onboarding/{id}/aprovar` | Aprovação de cadastro e liberação de acesso |
| `POST` | `/api/v1/identidade/onboarding/{id}/rejeitar` | Rejeição fundamentada de solicitação |
| `GET` | `/api/v1/identidade/ocupacoes` | Consulta e listagem de ocupações por unidade/condomínio |
| `POST` | `/api/v1/identidade/ocupacoes` | Criação de vínculo de ocupação com validação das 5 regras |
| `PATCH` | `/api/v1/identidade/ocupacoes/{id}` | Atualização de dados de ocupação |
| `POST` | `/api/v1/identidade/ocupacoes/{id}/inativar` | Inativação de vínculo com opção de cascade em dependentes |
| `POST` | `/api/v1/identidade/ocupacoes/rotina-expiracao` | Acionamento manual/job da rotina diária de expiração de prazos |
| `GET` | `/api/v1/identidade/veiculos-pets` | Consulta de veículos e animais por unidade |
| `POST` | `/api/v1/identidade/veiculos-pets/veiculos` | Cadastro de automóvel |
| `POST` | `/api/v1/identidade/veiculos-pets/pets` | Cadastro de animal de estimação |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-007: Autenticação JWT e Google](../../decisoes/ADR-007-autenticacao-jwt-aplicacao.md)
  - [ADR-008: Separação de Pessoa e Usuário](../../decisoes/ADR-008-pessoa-e-usuario.md)
  - [ADR-010: Nomenclatura em pt-BR](../../decisoes/ADR-010-nomenclatura-pt-br.md)
- **Especificações Funcionais**:
  - [onboarding-e-conta.md](onboarding-e-conta.md)
  - [cadastro-morador-solicitacao.md](cadastro-morador-solicitacao.md)
  - [veiculos-e-pets.md](veiculos-e-pets.md)
  - [perfis-e-permissoes.md](../10_transversal_plataforma/perfis-e-permissoes.md)
- **Scripts SQL**:
  - [003-identidade-cadastro.sql](../../sql/003-identidade-cadastro.sql)
