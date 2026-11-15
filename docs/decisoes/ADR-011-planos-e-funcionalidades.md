# ADR-011: Planos SaaS e funcionalidades habilitáveis

- **Status:** Aceito
- **Data:** 2026-09-30
- **Autores:** produto / documentação

## Contexto

O produto precisa de **planos diferenciados** (Starter, Essencial, Acesso, Administradora — ver [17](../plano/17-modelos-de-negocio-e-precificacao.md)) e de ligar/desligar módulos **por condomínio**. A personalização (P5) já previa feature flags em `condominio.configuracoes` JSONB, o que não escala para catálogo comercial, comparativo na landing nem enforcement na API.

## Decisão

1. **Catálogo** `funcionalidade` com `codigo` estável (`reservas`, `facial_intelbras`, …) e `escopo` `NUCLEO` | `OPCIONAL`.
2. **Planos** `plano` + inclusão em `plano_funcionalidade`.
3. **Assinatura** `assinatura` liga `condominio` ↔ `plano` (`TRIAL`/`ATIVA` únicos por condo).
4. **Override** `condominio_funcionalidade` permite ligar (cortesia/add-on) ou desligar (operacional) por condo.
5. **Resolução efetiva** (única fonte de verdade): função SQL `funcionalidade_habilitada(condo, codigo)` e espelho na API:
   - `NUCLEO` → sempre habilitada;
   - senão, se existe override → usa `habilitada` do override;
   - senão, se assinatura trial/ativa inclui no plano → habilitada;
   - senão → desabilitada.
6. Branding/regras operacionais continuam em `condominio.configuracoes` JSONB; **flags de módulo saem do JSONB** e passam a estas tabelas.
7. Enforcement: API/UI **escondem e rejeitam** rotas de módulos desabilitados (403/`FEATURE_DISABLED`); RBAC continua separado (perfil ≠ plano).

## Alternativas consideradas

1. Só JSONB em `configuracoes` — rápido, frágil para planos/billing/landing.
2. Feature flags só no código (LaunchDarkly etc.) — útil para rollout, não substitui entitlement comercial por tenant.
3. Schema por plano/cliente — ops pesadas cedo demais.

## Consequências

### Positivas

- Planos comerciais e override por condo no mesmo modelo.
- Seed alinhado aos tiers do doc 17; landing/`PublicPlan` consome o catálogo.
- Função SQL documenta o contrato; app e testes podem reutilizar a mesma regra.

### Negativas / riscos

- Síndico não pode “ligar” o que o plano não inclui (admin plataforma/cortesia sim via override).
- Precisa migrar qualquer flag legada em JSONB quando houver dados.
- Billing/fatura (`InvoicePlatform`) ainda é Fase 4.2 — estas tabelas são o **entitlement**, não o gateway.

## Referências

- DDL: [013-saas-planos-e-funcionalidades.sql](../sql/013-saas-planos-e-funcionalidades.sql), seed [014](../sql/014-seeds.sql)
- Spec: [planos-e-entitlements.md](../funcionalidades/10_transversal_plataforma/planos-e-entitlements.md)
- Roadmap **4.2** / **4.3c**; P5 / personalização
- Domínio `saas` em [02-arquitetura-tecnica.md](../plano/02-arquitetura-tecnica.md)
