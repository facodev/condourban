# ADR-008: Separar Pessoa de Usuário

- **Status:** Aceito
- **Data:** 2026-09-29
- **Autores:** consolidação gestao-condominio-documentacao

## Contexto

Visitantes, prestadores e moradores pré-aprovados existem como identidade de negócio antes (ou sem) conta de login. A conta autenticável (`usuario`) não deve poluir o cadastro cadastral (`pessoa`).

## Decisão

- `pessoa` = identidade de negócio (dados cadastrais, vínculos, biometria operacional).
- `usuario` = conta autenticável na API (e-mail + `senha_hash` e/ou `google_sub`) — [ADR-007](ADR-007-autenticacao-jwt-aplicacao.md).
- Uma **pessoa pode existir sem usuário**.
- Um usuário referencia no máximo uma pessoa (regra inicial; revisar se multi-perfil exigir).

## Alternativas consideradas

1. Um único `User` com flags — acopla login a cadastro e dificulta visitantes/prestadores.

## Consequências

### Positivas

- Fluxos de portaria e auto-cadastro naturais.
- LGPD: apagar conta ≠ apagar histórico operacional sem política.

### Negativas / riscos

- Joins e regras de “quem pode logar”.
- UX de “criar conta depois da aprovação”.

## Referências

- [cadastro-morador-solicitacao.md](../funcionalidades/01_identidade_cadastro/cadastro-morador-solicitacao.md)
- [onboarding-e-conta.md](../funcionalidades/01_identidade_cadastro/onboarding-e-conta.md)
- [15-modelo-dados-postgresql.md](../plano/15-modelo-dados-postgresql.md)
