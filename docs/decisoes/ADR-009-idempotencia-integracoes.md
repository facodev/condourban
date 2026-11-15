# ADR-009: Idempotência em integrações e webhooks

- **Status:** Aceito
- **Data:** 2026-09-29
- **Autores:** consolidação gestao-condominio-documentacao

## Contexto

Sincronização com Intelbras (e futuros provedores), webhooks e retries de fila podem repetir a mesma operação. Aprovação cadastral não deve depender da disponibilidade do hardware ([ADR-004](ADR-004-integracao-intelbras-facial.md)).

## Decisão

1. Operações repetíveis usam **chave de idempotência** e/ou referência externa (tabela `sincronizacao_acesso`, header `Idempotency-Key` na API).
2. Escopo mínimo: cadastro facial, criar/revogar autorização, ingestão de eventos, pagamentos futuros.
3. Fila: `PENDENTE` → `PROCESSANDO` → `CONCLUIDA` | `FALHA` (retry com backoff e limite).
4. Falha do provedor **não desfaz** aprovação cadastral válida.

## Alternativas consideradas

1. Só “best effort” sem chave — risco de duplicar credenciais no equipamento.

## Consequências

### Positivas

- Reprocessamento seguro; reconciliação periódica viável.

### Negativas / riscos

- Exige índice único e disciplina no adaptador.

## Referências

- [16-api-v1-referencia.md](../plano/16-api-v1-referencia.md)
- [biometria-facial-intelbras.md](../funcionalidades/03_controle_acesso/biometria-facial-intelbras.md)
- [08-intelbras-facial-e-reservas.md](../plano/08-intelbras-facial-e-reservas.md)
- [004-controle-acesso.sql](../sql/004-controle-acesso.sql)
