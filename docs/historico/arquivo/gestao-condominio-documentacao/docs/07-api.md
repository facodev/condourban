# API inicial

Prefixo:

```text
/api/v1
```

## Identidade

```http
GET /me
GET /me/condominios
GET /me/permissoes
```

## Condomínio

```http
GET /condominio
GET /blocos
POST /blocos
GET /unidades
POST /unidades
GET /unidades/{id}
```

## Pessoas

```http
GET /pessoas
POST /pessoas
GET /pessoas/{id}
PATCH /pessoas/{id}
```

## Cadastro de morador

```http
POST /convites-cadastro
GET /convites-cadastro/{codigo}

POST /solicitacoes-cadastro
GET /solicitacoes-cadastro/{id}
PATCH /solicitacoes-cadastro/{id}

POST /solicitacoes-cadastro/{id}/documentos
POST /solicitacoes-cadastro/{id}/verificacao-facial

POST /solicitacoes-cadastro/{id}/enviar
POST /solicitacoes-cadastro/{id}/aprovar
POST /solicitacoes-cadastro/{id}/solicitar-correcao
POST /solicitacoes-cadastro/{id}/rejeitar
```

## Controle de acesso

```http
GET /credenciais-acesso
POST /credenciais-acesso
POST /credenciais-acesso/{id}/revogar

GET /autorizacoes-acesso
POST /autorizacoes-acesso
PATCH /autorizacoes-acesso/{id}
POST /autorizacoes-acesso/{id}/revogar

GET /dispositivos-acesso
GET /eventos-acesso
```

## Intelbras

A aplicação externa não deve expor endpoints proprietários.

```http
POST /integracoes/controle-acesso/sincronizar
POST /integracoes/controle-acesso/webhook
```

## Idempotência

Operações críticas aceitam:

```http
Idempotency-Key: UUID
```

Principalmente:

- cadastro facial;
- autorização;
- revogação;
- processamento de webhook.

## Webhook

Todo evento recebido do provedor deve:

1. validar autenticidade;
2. localizar referência externa;
3. garantir idempotência;
4. persistir evento;
5. publicar evento de domínio;
6. responder rapidamente.
