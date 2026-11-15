# Segurança e LGPD

## Dados sensíveis

O produto poderá processar:

- CPF;
- documentos de identificação;
- contratos;
- fotografias;
- dados faciais;
- eventos de acesso.

Dados biométricos exigem governança específica.

## Princípios

- finalidade;
- necessidade;
- segurança;
- transparência;
- controle de acesso;
- retenção;
- descarte;
- auditoria.

## CPF

Armazenar:

```text
cpf_hash
cpf_criptografado
```

O hash é usado para busca/identificação técnica.

O valor original deve ser recuperado somente quando necessário.

## Biometria

Preferência:

```text
Aplicação
   |
   v
Provedor de controle de acesso
   |
   v
Referência externa
```

Evitar armazenar template biométrico bruto no PostgreSQL.

## Documentos

Os arquivos devem ter:

- hash;
- controle de acesso;
- versionamento;
- retenção;
- trilha de auditoria.

## RLS

Toda consulta de dados condominiais deve respeitar:

```text
usuário
  -> associação
  -> condomínio
  -> RLS
```

## Auditoria

Registrar principalmente:

- aprovação;
- rejeição;
- correção;
- acesso a documento;
- criação de credencial;
- alteração de autorização;
- revogação;
- acesso autorizado;
- acesso negado;
- alterações administrativas.

## Logs

Não registrar:

- CPF em claro;
- token;
- segredo;
- biometria;
- conteúdo integral de documentos.

## Retenção

Cada categoria deve possuir política específica:

| Categoria | Política |
|---|---|
| Solicitação de cadastro | conforme necessidade operacional/jurídica |
| Documento | conforme finalidade e obrigação aplicável |
| Biometria | mínimo necessário |
| Evento de acesso | conforme política do condomínio e obrigações |
| Auditoria | conforme governança |

As políticas definitivas devem ser validadas juridicamente.
