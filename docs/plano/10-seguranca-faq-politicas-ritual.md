# Ritual permanente: Segurança + FAQ + Políticas

**Regra do produto:** em **toda** entrega de funcionalidade (ou mudança relevante), o time **deve** tratar segurança, atualizar o FAQ e revisar/atualizar políticas de privacidade (e termos relacionados). Não é opcional nem "fase futura".

Espelhado no checklist de Pronto do [roadmap](03-roadmap-e-entregas.md) e no ritual de sessão em [`../README.md`](../README.md).

---

## 1. Segurança (pensar sempre)

Para **cada** feature / módulo / integração, responder antes de implementar e no PR/review:

| Pergunta | Exemplos |
|----------|----------|
| Quem pode ver/fazer? | RBAC por perfil e por condomínio (tenant) |
| Há dados pessoais ou sensíveis? | Face, documentos, menores, localização |
| Como autenticar e autorizar? | Sessão/JWT, guards no Angular + policy no Python |
| Auditoria? | `AuditLog` em liberação de acesso, exclusão, mudança de papel, acionamento |
| Logs de uso? | `UsageEvent` sem PII excessiva; não misturar com auditoria |
| Abuso / rate limit (buckets)? | Login, upload de face, leads, acionamentos, convites — Redis token bucket |
| DDoS / volumétrico? | CDN/WAF na borda; proxy; 429 na API — ver [13](13-seguranca-plataforma-logs-e-ddos.md) |
| Dados em trânsito e em repouso? | HTTPS, secrets na VPS, storage com acesso controlado |
| Integração externa? | Intelbras: escopo mínimo, falha segura, sem credenciais no front |
| LGPD nesta feature? | Base legal, consentimento, retenção, exclusão |

### Tipos de risco frequentes neste produto

- Multi-tenant (vazamento entre condomínios)
- Biometria / Intelbras (doc 08, ADR-004)
- Uploads (ocorrências, documentos, foto facial)
- Portaria e pré-cadastro de visitantes
- Exportação/exclusão LGPD (C1)
- Landing (leads, cookies, analytics)
- Flood / credential stuffing / abuso de acionamento remoto

Registrar decisões de segurança relevantes em ADR ou no journal da sessão. Detalhe de plataforma: [13-seguranca-plataforma-logs-e-ddos.md](13-seguranca-plataforma-logs-e-ddos.md).

---

## 2. FAQ (sempre acrescentar dúvidas)

**Regra:** toda funcionalidade nova ou mudança de comportamento gera **pelo menos 1 pergunta** no FAQ (fonte única — landing + app, doc 07).

### Quando adicionar

- Feature nova em qualquer versão (V1–V5)
- Mudança de fluxo (ex.: como autorizar visitante)
- Dúvida recorrente do síndico/morador/portaria
- Tema de privacidade ("o que fazem com minha face"?)
- Limitação consciente (ex.: "por que não pago boleto no app"? — P3)

### Como registrar (até existir CMS)

1. Esboçar Q&A em `docs/conteudo/faq/` (Markdown por categoria) **ou** lista no journal + ticket.
2. Categoria sugerida: Conta · Reservas · Acesso/Facial · Ocorrências · Comunicados · Privacidade · Planos SaaS · Portaria.
3. Marcar `visible_public` / `visible_in_app` quando o modelo `FaqItem` existir.
4. Entrada no CHANGELOG: "FAQ: "?

### Template de item FAQ

```markdown
### [Categoria] Pergunta clara?

Resposta objetiva (2?6 frases). Link para política/versão se for dado pessoal.
Última atualização: AAAA-MM-DD · Feature relacionada: ?
```

---

## 3. Políticas e privacidade (sempre atualizar)

**Regra:** se a feature **coleta, trata, compartilha ou retém** dado pessoal (ou muda cookies/analytics), **obrigatório** revisar:

| Documento | Atualizar quando? |
|-----------|-------------------|
| Política de Privacidade | Novo dado, nova finalidade, novo parceiro (ex.: Intelbras), biometria, menores |
| Termos de Uso | Novos direitos/deveres do usuário ou do condomínio |
| Política de Cookies | Novo tracker na landing/app |
| Termos SaaS B2B | Cobrança do software, SLA, subprocessadores |
| Política biométrica (anexo ou seção) | Pré-cadastro facial / reconhecimento |

### Processo de versão

1. Editar conteúdo na **fonte única** (`LegalDocument` versionado — doc 07).
2. Incrementar **versão** + `effective_date`.
3. Se mudança material: exigir **novo aceite** no app (`UserTermsAcceptance`).
4. Publicar na landing e no app **na mesma versão**.
5. CHANGELOG + nota no FAQ ("Atualizamos a Política de Privacidade em "?).

### Checklist mínimo por release

- [ ] Matriz de dados da feature (o que coleta / por quê / por quanto tempo)
- [ ] Texto da política atualizado **ou** confirmação explícita "sem impacto"
- [ ] FAQ com dúvida do usuário final
- [ ] Segurança: tenant, authz, **auditoria**, **uso**, buckets/rate limit, uploads revisados

---

## 4. Definition of Done (DoD) — conteúdo + segurança

Uma tarefa de feature **só está pronta** se:

1. Código + testes de isolamento tenant (quando aplicável)
2. **Revisão de segurança** (checklist §1)
3. **≥1 item FAQ** novo ou atualizado (§2) — ou N/A justificado no PR
4. **Políticas** revisadas (§3) — atualizadas ou "sem impacto" documentado
5. Docs de plano/CHANGELOG atualizados se mudar escopo

---

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` — regra permanente |
| Última revisão | 2026-09-29 |
