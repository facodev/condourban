# Bounded Context: Manutenção e Operação Predial (`manutencao`)

Este bounded context é o gestor técnico da conservação física das edificações, cobrindo ordens de serviço corretivas, gestão de chamados com evidências visuais e o Plano de Manutenção e Operação (PMO) preventivo de ativos e patrimônio.

---

## 1. Responsabilidade do Domínio

- **Chamados e Reparos Prediais**: Registro de pedidos de manutenção corretiva por moradores, zelador ou síndico (elétrica, hidráulica, iluminação, pintura, portões) com anexos de fotos do problema.
- **Ordens de Serviço (OS)**: Acompanhamento das etapas de execução dos serviços (aberta, em cotação, aprovada, em andamento, concluída, cancelada), prestadores de serviço atribuídos e custos de peças/mão de obra.
- **Plano de Manutenção Preventiva (PMO)**: Cronograma periódico de inspeções técnicas e manutenções exigidas por normas (ABNT NBR 5674 e correlatas), prevenindo falhas críticas em elevadores, bombas de recalque, geradores a diesel, SPDA (para-raios), reservatórios de água e sistemas de combate a incêndio.
- **Inventário e Patrimônio**: Cadastro e controle de ativos físicos de propriedade do condomínio (mobiliário, ferramentas, motores, maquinários) com código de tombamento, garantia e manual técnico.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/manutencao/`)
```text
manutencao/
├── __init__.py
├── router.py
├── chamados_servicos/     # Chamados de reparo, agendamentos e ordens de serviço
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── plano_inventario/      # PMO preventivo e inventário/patrimônio
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/manutencao/`)
```text
manutencao/
├── components/
│   ├── chamados-servicos/ # Abertura de chamados com foto e acompanhamento de OS
│   └── plano-inventario/  # Cronograma preventivo (PMO) e gestão de patrimônio
├── services/
│   └── manutencao.service.ts
└── manutencao.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `chamado_manutencao`: Solicitação de reparo (`id`, `condominio_id`, `solicitante_pessoa_id`, `titulo`, `descricao`, `local_especifico`, `prioridade`: `baixa`, `media`, `alta`, `urgente`, `status`: `aberto`, `em_andamento`, `concluido`, `cancelado`, `fotos_urls` JSONB, `criado_em`).
- `ordem_servico_manutencao`: Execução da OS (`id`, `chamado_id`, `prestador_pessoa_id`, `custo_estimado`, `custo_real`, `data_inicio_prevista`, `data_conclusao`, `observacoes_tecnicas`).
- `equipamento_patrimonio`: Ativo físico (`id`, `condominio_id`, `nome_equipamento`, `numero_patrimonio`, `fabricante`, `modelo`, `localizacao`, `data_aquisicao`, `valor_aquisicao`, `fim_garantia`).
- `plano_manutencao_preventiva`: Tarefa do PMO (`id`, `equipamento_id`, `descricao_tarefa`, `periodicidade`: `semanal`, `mensal`, `trimestral`, `semestral`, `anual`, `proxima_data_execucao`, `empresa_responsavel`, `status`: `em_dia`, `alerta`, `atrasado`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/manutencao/chamados` | Listagem de chamados e reparos |
| `POST` | `/api/v1/manutencao/chamados` | Abertura de chamado corretivo com upload de foto |
| `PATCH` | `/api/v1/manutencao/chamados/{id}/status` | Atualização do status ou encerramento do chamado |
| `GET` | `/api/v1/manutencao/inventario` | Inventário de equipamentos e patrimônio |
| `GET` | `/api/v1/manutencao/pmo` | Cronograma e calendário preventivo de manutenções |
| `POST` | `/api/v1/manutencao/pmo/{id}/concluir` | Registro de conclusão de rotina preventiva |

---

## 5. Rastreabilidade com Documentação Canônica

- **Especificações Funcionais**:
  - [chamados-e-ordens-servico.md](chamados-e-ordens-servico.md)
  - [manutencao-preventiva-pmo.md](manutencao-preventiva-pmo.md)
- **Scripts SQL**:
  - [010-manutencao.sql](../../sql/010-manutencao.sql)
