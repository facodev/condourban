# Bounded Context: Governança e Administração Legal (`governanca`)

Este bounded context é o pilar de governança formal, conformidade jurídica e segurança administrativa do condomínio, abrangendo assembleias, votações digitais auditáveis e auditoria forense do sistema.

---

## 1. Responsabilidade do Domínio

- **Assembleias Digitais e Híbridas**: Convocação formal por editais com prazos legais (Ordinárias e Extraordinárias), definição de primeira e segunda chamada e suporte à transmissão remota ou presencial.
- **Pautas e Deliberações**: Estruturação de pautas independentes de discussão, quorum específico por tipo de tema (maioria simples, 2/3, unanimidade) e representação por procurações validadas.
- **Votação Eletrônica Auditável**: Mecanismo de voto digital ao vivo ou pré-assembleia por fração ideal ou por unidade, garantindo unicidade de voto e impossibilidade de fraudes.
- **Atas e Homologação**: Registro detalhado dos resultados, geração de ata preliminar para revisão, suporte a assinaturas digitais (ICP-Brasil ou assinatura eletrônica qualificada) e disponibilização pública aos condôminos.
- **Segurança, RBAC e Auditoria**: Matriz de permissões de acesso às funções do sistema e logs imutáveis de auditoria (`audit trail`) de todas as alterações críticas realizadas no sistema.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/governanca/`)
```text
governanca/
├── __init__.py
├── router.py
├── assembleias/           # Editais, pautas, votação digital e atas
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── seguranca_auditoria/   # Matriz RBAC e logs de auditoria
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/governanca/`)
```text
governanca/
├── components/
│   ├── assembleias/       # Convocação, pauta, votação ao vivo e atas
│   └── seguranca-auditoria/ # Matriz de permissões e logs de auditoria
├── services/
│   └── governanca.service.ts
└── governanca.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `assembleia`: Instância da assembleia (`id`, `condominio_id`, `titulo`, `tipo`: `ordinaria`, `extraordinaria`, `data_primeira_chamada`, `data_segunda_chamada`, `status`: `convocada`, `em_andamento`, `em_apuracao`, `encerrada`, `edital_url`, `link_videoconferencia`).
- `pauta_assembleia`: Item de deliberação (`id`, `assembleia_id`, `ordem`, `titulo`, `descricao`, `tipo_quorum`, `status_votacao`: `aberta`, `fechada`).
- `voto_assembleia`: Voto formal da unidade (`id`, `pauta_id`, `unidade_id`, `pessoa_id`, `opcao`: `favoravel`, `contrario`, `abstencao`, `peso_fracao_ideal`, `procuracao_url`, `votado_em`).
- `ata_assembleia`: Documento formal de ata (`id`, `assembleia_id`, `texto_ata`, `arquivo_pdf_url`, `status_assinatura`: `minuta`, `em_assinatura`, `registrada_cartorio`).
- `evento_auditoria`: Trilha de auditoria imutável (`id`, `condominio_id`, `usuario_id`, `acao`, `entidade_afetada`, `dados_anteriores` JSONB, `dados_novos` JSONB, `ip_origem`, `user_agent`, `criado_em`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/governanca/assembleias` | Listagem de assembleias convocadas ou históricas |
| `POST` | `/api/v1/governanca/assembleias` | Convocação de nova assembleia com envio de edital |
| `GET` | `/api/v1/governanca/assembleias/{id}/pautas` | Pautas em deliberação e apuração em tempo real |
| `POST` | `/api/v1/governanca/assembleias/{id}/votar` | Registro de voto da unidade na pauta |
| `POST` | `/api/v1/governanca/assembleias/{id}/encerrar` | Encerramento e apuração oficial da ata |
| `GET` | `/api/v1/governanca/auditoria` | Consulta aos logs de auditoria e segurança |

---

## 5. Rastreabilidade com Documentação Canônica

- **ADRs Vinculadas**:
  - [ADR-006: Isolamento RLS por Condomínio](../../decisoes/ADR-006-isolamento-rls-postgresql.md)
  - [ADR-008: Separação Pessoa e Usuário](../../decisoes/ADR-008-pessoa-e-usuario.md)
- **Especificações Funcionais**:
  - [assembleias-virtuais.md](assembleias-virtuais.md)
  - [repositorio-documentos.md](repositorio-documentos.md)
  - [perfis-e-permissoes.md](../10_transversal_plataforma/perfis-e-permissoes.md)
- **Scripts SQL**:
  - [008-governanca.sql](../../sql/008-governanca.sql) (`assembleia`, `pauta_assembleia`, `voto_assembleia`, `procuracao_assembleia`, `ata_assembleia`, `documento`)
  - [011-transversal-e-auditoria.sql](../../sql/011-transversal-e-auditoria.sql) (`evento_auditoria`)
