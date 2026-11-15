# Segurança da plataforma: auditoria, uso, DDoS e rate limit

> Parte **obrigatória** do plano (não é "nice to have"). Detalhe técnico; o ritual por feature continua em [10](10-seguranca-faq-politicas-ritual.md). Arquitetura geral: [02](02-arquitetura-tecnica.md).

## 1. Princípio

Desde a **Fase 1**:

1. **Tudo sensível deixa rastros** (auditoria).
2. **Uso do produto e da API é mensurável** (logs de uso / métricas).
3. **Abuso e DDoS são tratados na borda + na API** (WAF/CDN, rate limit por *buckets*).
4. **Acessos físicos e acionamentos** também têm limiar anti-abuso (buckets por unidade/usuário/dispositivo).

## 2. Três famílias de log (não misturar)

| Tipo | Nome no modelo (alvo) | Para que serve | Quem vê |
|------|------------------------|----------------|---------|
| **Auditoria** | `AuditLog` | Quem fez o quê, em qual tenant, com qual recurso (imutável, append-only) | Admin plataforma, síndico (escopo), suporte (impersonation) |
| **Uso / produto** | `UsageEvent` (+ agregados) | Telemetria de produto: telas, módulos, volume por condomínio; capacidade e billing SaaS | Admin plataforma (agregado); sem PII desnecessária |
| **Acesso técnico** | `RequestLog` / proxy / APM | HTTP: IP, rota, status, latência, user-agent; detectar abuso | Ops / SIEM; retenção curta |
| **Acesso físico** | `AccessLog` (portaria/Intelbras) | Entrou/saiu, dispositivo, resultado | Portaria + síndico do tenant |

Regras:

- `AuditLog` **não** é analytics de marketing.
- `UsageEvent` **não** substitui auditoria jurídica.
- Logs de request **não** guardam body com senha/face/token.
- Retenção definida por tipo (ver §6) e espelhada na Política de Privacidade.

### 2.1 Campos mínimos — `AuditLog`

- `id`, `occurred_at` (UTC), `actor_user_id` (nullable se sistema), `actor_ip`, `tenant_id` / `condominium_id`
- `action` (ex.: `membership.role_changed`, `visitor.granted`, `face.enrolled`, `document.deleted`)
- `resource_type`, `resource_id`
- `before` / `after` (diff JSON, sem segredos)
- `request_id` / `correlation_id`
- Append-only: **sem UPDATE/DELETE** pela aplicação (só rotina de retenção controlada)

Eventos **obrigatórios** desde Fase 1: login/logout/falha de auth, mudança de papel, aceite de termos, CRUD de documentos sensíveis, exclusão LGPD, impersonation.  
Fase 2+: liberação visitante, facial, reserva, acionamento, convite.

### 2.2 Campos mínimos — `UsageEvent`

- `occurred_at`, `tenant_id`, `user_id` (id ou pseudônimo conforme LGPD), `event_name` (ex.: `screen.home`, `module.reservas.open`)
- `properties` agregáveis (sem texto livre PII)
- Preferir **agregação diária** (`UsageDailyRollup`) para dashboards SaaS

### 2.3 Request / edge

- Proxy (Caddy/Nginx) ou CDN: access log + métricas
- App: middleware estruturado (JSON) + tracing (`request_id`)
- Alertas: taxa de 401/403/429, picos de RPS, erros 5xx

## 3. Rate limit e "buckets" de acesso

Usar **token bucket** (ou sliding window) no **Redis**, por chave composta.

### 3.1 Buckets de API (aplicação)

| Bucket | Chave típica | Exemplo de limiar (ajustar em ops) | Aplicar em |
|--------|--------------|--------------------------------------|------------|
| Global IP | `rl:ip:{ip}` | N req/min | Toda API pública |
| Auth | `rl:auth:{ip}` | Poucas tentativas/min + lockout progressivo | Login, refresh, reset senha |
| Usuário autenticado | `rl:user:{id}` | Teto por minuto | API geral |
| Tenant | `rl:tenant:{id}` | Protege vizinhos de um condomínio abusivo | API autenticada |
| Endpoint sensível | `rl:face:{user}`, `rl:upload:{user}` | Mais restrito | Facial, upload, leads landing |
| Acionamento | `rl:act:{unit}:{user}` | Poucos por minuto/hora | Abrir portão / IoT |
| Convite | `rl:invite:{unit}` | Limite diário de convites | Criação de convites |

Resposta padrão: **HTTP 429** + `Retry-After`. Nunca revelar se usuário existe nos fluxos de auth.

### 3.2 Buckets de acesso físico / portaria

- Limite de liberações e acionamentos por unidade/período
- Bloqueio temporário após N falhas (anti-enumeração de QR/código)
- Auditoria de cada acionamento (`AuditLog` + `AccessLog`)

## 4. Proteção contra DDoS e abuso volumétrico

Camadas (da borda para o app):

| Camada | Medida | Fase alvo |
|--------|--------|-----------|
| DNS / CDN / WAF | Cloudflare (ou similar) na frente da VPS: proxy, WAF gerenciado, challenge bot, cache estático | **Fase 1** (produção) |
| TLS / proxy VPS | Caddy ou Nginx: limite de conexões, `limit_req`, timeouts, buffers | Fase 1 |
| App | Rate limit Redis (§3), CORS estrito, headers de segurança | Fase 1 |
| Host | fail2ban / ban de IPs ruidosos no SSH e no proxy; SSH só chave | Fase 1 |
| Rede | Firewall VPS (só 80/443 públicos; DB/Redis internos); WireGuard para Intelbras se preciso | Fase 1–2 |
| Capacidade | Na VPS única, priorizar **absorver na borda** + degradar com 429 | Contínuo |
| Observabilidade | Alertas de RPS, 429, origem anômala | Fase 1+ |

**Não depender só do app** para DDoS: ataque volumétrico deve ser cortado no **WAF/CDN** antes de saturar a VPS.

Checklist produção Fase 1:

- [ ] Domínio atrás de CDN/WAF (modo emergência documentado)
- [ ] IP de origem da VPS **não** publicado (só proxy)
- [ ] Healthchecks sem vazar stack
- [ ] Backups e plano se origin cair

## 5. Outros controles de segurança (plano)

| Controle | Notas |
|----------|--------|
| Isolamento tenant | Filtro na app + **RLS Postgres** (`SET LOCAL app.condominio_id`) — [ADR-006](../decisoes/ADR-006-isolamento-rls-postgresql.md), [sql/](../sql/README.md) |
| Secrets | `.env` fora do git; rotação; nunca no front |
| Headers | HSTS, CSP, X-Content-Type-Options, Referrer-Policy |
| Uploads | Tipo/tamanho, antivírus em produção, storage privado + URL assinada |
| Auth | JWT na API: e-mail/senha **+ Google (Gmail)**; **sem Keycloak** — [ADR-007](../decisoes/ADR-007-autenticacao-jwt-aplicacao.md) |
| CPF | Preferir `cpf_hash` (busca) + `cpf_criptografado` (exibição sob demanda); nunca em log |
| Biometria | Consentimento, retenção, mínimo necessário; preferir referência no provedor (doc 08 / ADR-004) |
| MFA | Obrigatória perfis críticos na Fase 5 (ou antes se exigido) |
| Backup | Cifrado; restore testado; acesso restrito |
| Dependências | Scan de CVE no CI (pip/npm) |
| Impersonation | Sempre com `AuditLog` |
| Logs proibidos | CPF em claro, token, segredo, biometria, conteúdo integral de documentos |

## 6. Retenção (provisão — fechar com jurídico)

| Tipo | Retenção sugerida |
|------|-------------------|
| `AuditLog` | 12–24 meses (ou exigência contratual B2B) |
| `UsageEvent` bruto | 30–90 dias; rollups até 24 meses |
| Request / proxy | 7–30 dias |
| `AccessLog` físico | Conforme política do condomínio + LGPD |

## 7. Entrega por fase (roadmap)

| Fase | Entrega de segurança |
|------|----------------------|
| **1** | `AuditLog` base; `UsageEvent` mínimo; Redis rate limit + buckets auth/API/tenant; CDN/WAF; headers; logs estruturados; FAQ/política |
| **2** | Buckets acionamento/convite/facial; `AccessLog` completo; auditoria de liberações |
| **5** | MFA; revisão SIEM/alertas; endurecimento PWA; revisão de limiares |
| **8** | Anti-abuso IoT multi-dispositivo alinhado aos buckets |

Itens espelhados em [03-roadmap-e-entregas.md](03-roadmap-e-entregas.md).

## 8. FAQ / políticas

- Privacidade: declarar logs técnicos, auditoria e telemetria de uso (sem vender dado).
- FAQ: "Vocês registram o que eu faço no app?" / "Por que meu acesso foi temporariamente bloqueado?"

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-09-29 |
