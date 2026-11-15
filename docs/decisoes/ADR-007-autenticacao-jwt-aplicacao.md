# ADR-007: Autenticação na aplicação (e-mail/senha + Google)

- **Status:** Aceito
- **Data:** 2026-09-29
- **Autores:** consolidação gestao-condominio-documentacao + stakeholder

## Contexto

O produto precisa de login simples para moradores e também de **entrar com Gmail (Google OAuth)**, comum em apps mobile/PWA.

## Decisão

1. Dois meios de autenticação, ambos emitindo **JWT + refresh** da própria API:
   - **E-mail + senha** (hash argon2/bcrypt em `usuario.senha_hash`).
   - **Google (Gmail)** via OAuth 2.0 / OpenID Connect — “Entrar com Google” (Google Identity / GIS).
2. Modelo `usuario`:
   - `email` obrigatório e único;
   - `senha_hash` **nullable** (conta só-Google não tem senha local);
   - `google_sub` nullable e único (subject do Google);
   - pelo menos um fator: senha **ou** `google_sub` (ou ambos, se o usuário vincular).
3. Fluxos:
   - Cadastro/login local → JWT.
   - Callback/token Google → validar `id_token` na API → achar/criar `usuario` por `google_sub` ou e-mail verificado → JWT da app.
   - Vincular Google a conta existente (mesmo e-mail verificado) com confirmação.
4. Credenciais Google (`client_id` / `client_secret` se necessário): só em secret/env; nunca no Git.
5. Autorização de **negócio** (membership, papéis, RLS) continua 100% no domínio ([ADR-006](ADR-006-isolamento-rls-postgresql.md), [ADR-008](ADR-008-pessoa-e-usuario.md)).
6. MFA adicional (TOTP etc.) — opcional Fase 5; Google já pode trazer 2FA da conta Google.

## Alternativas consideradas

1. Só e-mail/senha — pior UX; stakeholder pediu Gmail também.
3. Só Google — exclui quem não usa Gmail; manter senha local.

## Consequências

### Positivas

- Onboarding rápido com Gmail; senha local para quem preferir.
- Infra leve (só Client ID Google Cloud + API).

### Negativas / riscos

- Conta Google-only: fluxo de “definir senha” se quiser login local depois.
- Política de e-mail: conflito se Google e-mail já existir com senha — exigir vínculo explícito.
- Apps nas lojas: configurar OAuth redirect / SHA corretos (Fase 6).

## Referências

- [15-modelo-dados-postgresql.md](../plano/15-modelo-dados-postgresql.md)
- [onboarding-e-conta.md](../funcionalidades/01_identidade_cadastro/onboarding-e-conta.md)
- [16-api-v1-referencia.md](../plano/16-api-v1-referencia.md)
- [003-identidade-cadastro.sql](../sql/003-identidade-cadastro.sql)
