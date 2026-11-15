# Bounded Context: Comunicação e Convivência (`comunicacao`)

Este bounded context é o ecossistema de convivência social e comunicação institucional, concentrando os canais oficiais entre a gestão do condomínio e os moradores, registros de ocorrências e interação comunitária.

---

## 1. Responsabilidade do Domínio

- **Mensageria e Comunicados Oficiais**: Emissão de avisos, comunicados formais da administração e alertas com marcação de urgência (ex.: falta d'água, manutenções emergenciais). Suporte a recibo de leitura e push notifications automáticas.
- **Canal Direto Morador-Gestão**: Mensagens direcionadas entre a unidade e o síndico/administração para esclarecimento de dúvidas e solicitações administrativas.
- **Ocorrências Unificadas**: Canal padronizado para abertura, acompanhamento e mediação de reclamações (barulho, animais, vagas, vazamentos), integrando chamados abertos diretamente pelo morador com os registros do livro de ocorrências da portaria.
- **Mural Social e Enquetes**: Participação comunitária através de enquetes de opinião prévias a assembleias, módulo de achados e perdidos com fotos e classificados de compra/venda/serviços entre vizinhos.

---

## 2. Estrutura de Código no Projeto

Conforme definido em [Estrutura.md](../../decisoes/Estrutura.md):

### Backend (`backend/app/modulos/comunicacao/`)
```text
comunicacao/
├── __init__.py
├── router.py
├── mensageria/            # Comunicados oficiais e canal morador-gestão
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── ocorrencias/           # Ocorrências unificadas (morador e livro da portaria)
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── service.py
└── mural_social/          # Enquetes, achados/perdidos e classificados
    ├── router.py
    ├── models.py
    ├── schemas.py
    └── service.py
```

### Frontend (`frontend/src/app/features/comunicacao/`)
```text
comunicacao/
├── components/
│   ├── mensageria/        # Feed de comunicados oficiais e chat morador-gestão
│   ├── ocorrencias/       # Ocorrências unificadas com status de atendimento
│   └── mural-social/      # Enquetes comunitárias, achados e classificados
├── services/
│   └── comunicacao.service.ts
└── comunicacao.routes.ts
```

---

## 3. Entidades Principais e Modelo Relacional (SQL)

- `comunicado`: Mensagens oficiais (`id`, `condominio_id`, `autor_pessoa_id`, `titulo`, `conteudo`, `urgente`, `publicado_em`, `expira_em`, `anexos_urls` JSONB).
- `leitura_comunicado`: Rastreamento de leitura (`comunicado_id`, `usuario_id`, `lido_em`).
- `ocorrencia`: Chamado de convivência (`id`, `condominio_id`, `unidade_id`, `autor_pessoa_id`, `categoria`, `titulo`, `descricao`, `status`: `pendente`, `em_analise`, `resolvido`, `cancelado`, `fotos_urls` JSONB, `criado_em`).
- `comentario_ocorrencia`: Interações na ocorrência (`id`, `ocorrencia_id`, `autor_pessoa_id`, `mensagem`, `interno_gestao`, `criado_em`).
- `enquete`: Consulta de opinião (`id`, `condominio_id`, `titulo`, `descricao`, `data_limite`, `fechada`).
- `opcao_enquete`: Alternativa de voto (`id`, `enquete_id`, `texto_opcao`).
- `voto_enquete`: Registro do voto (`enquete_id`, `unidade_id`, `opcao_id`, `votado_em`).
- `item_achado_perdido`: (`id`, `condominio_id`, `titulo`, `descricao`, `local_encontrado`, `status`: `guardado`, `devolvido`, `foto_url`).
- `anuncio_classificado`: (`id`, `condominio_id`, `unidade_id`, `titulo`, `descricao`, `preco`, `contato`, `ativo`).

---

## 4. Endpoints Principais da API (OpenAPI)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/comunicacao/mensageria` | Feed de comunicados oficiais do condomínio |
| `POST` | `/api/v1/comunicacao/mensageria` | Emissão de novo comunicado oficial |
| `POST` | `/api/v1/comunicacao/mensageria/{id}/leitura` | Confirmação de ciência/leitura pelo usuário |
| `GET` | `/api/v1/comunicacao/ocorrencias` | Listagem de ocorrências do usuário ou da gestão |
| `POST` | `/api/v1/comunicacao/ocorrencias` | Abertura de nova ocorrência |
| `POST` | `/api/v1/comunicacao/ocorrencias/{id}/comentarios` | Resposta ou atualização de status da ocorrência |
| `GET` | `/api/v1/comunicacao/mural-social` | Visualização do feed do mural social |
| `POST` | `/api/v1/comunicacao/mural-social/enquetes/{id}/votar` | Registro de voto na enquete |

---

## 5. Rastreabilidade com Documentação Canônica

- **Especificações Funcionais**:
  - [mural-comunicados.md](mural-comunicados.md)
  - [ocorrencias-livro.md](ocorrencias-livro.md)
  - [enquetes-consultas.md](enquetes-consultas.md)
  - [mural-comunidade.md](mural-comunidade.md)
  - [canal-fale-conosco.md](canal-fale-conosco.md)
- **Scripts SQL**:
  - [007-comunicacao.sql](../../sql/007-comunicacao.sql)
