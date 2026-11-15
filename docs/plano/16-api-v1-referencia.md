# API v1 — referência inicial por Bounded Contexts

Prefixo canônico da API: `/api/v1`  
Backend oficial: **FastAPI** assíncrono com documentação OpenAPI/Swagger gerada em `/api/v1/docs`.  
Tags do OpenAPI agrupadas estritamente pelos **9 Bounded Contexts em pt-BR** ([ADR-013](../decisoes/ADR-013-organizacao-diretorios.md) e [Estrutura.md](../decisoes/Estrutura.md)).  
Especificações funcionais de comportamento: [`docs/funcionalidades/`](../funcionalidades/README.md).

---

## 1. Identidade e Cadastro (`/api/v1/identidade/`)

Especificações: [onboarding-e-conta.md](../funcionalidades/01_identidade_cadastro/onboarding-e-conta.md), [cadastro-morador-solicitacao.md](../funcionalidades/01_identidade_cadastro/cadastro-morador-solicitacao.md), [veiculos-e-pets.md](../funcionalidades/01_identidade_cadastro/veiculos-e-pets.md).

```http
# Autenticação e Sessão
POST /auth/registro
POST /auth/login
POST /auth/refresh
POST /auth/recuperar-senha
POST /auth/google                # id_token Google OAuth 2.0 → JWT da aplicação (ADR-007)
POST /auth/google/vincular

# Cadastro Civil e Vínculos
GET    /pessoas
POST   /pessoas
GET    /pessoas/{id}
PATCH  /pessoas/{id}

# Solicitação de Cadastro e Auto-Onboarding
POST   /convites-cadastro
GET    /convites-cadastro/{codigo}
POST   /solicitacoes-cadastro
GET    /solicitacoes-cadastro/{id}
PATCH  /solicitacoes-cadastro/{id}
POST   /solicitacoes-cadastro/{id}/documentos
POST   /solicitacoes-cadastro/{id}/verificacao-facial
POST   /solicitacoes-cadastro/{id}/enviar
POST   /solicitacoes-cadastro/{id}/aprovar
POST   /solicitacoes-cadastro/{id}/solicitar-correcao
POST   /solicitacoes-cadastro/{id}/rejeitar

# Veículos e Pets da Unidade
GET    /unidades/{unidade_id}/veiculos
POST   /unidades/{unidade_id}/veiculos
DELETE /veiculos/{id}
GET    /unidades/{unidade_id}/pets
POST   /unidades/{unidade_id}/pets
DELETE /pets/{id}
```

---

## 2. Estrutura Física do Condomínio (`/api/v1/condominio/`)

Especificações: [estrutura-fisica.md](../funcionalidades/02_condominio/estrutura-fisica.md), [configuracao-condominio.md](../funcionalidades/02_condominio/configuracao-condominio.md).

```http
GET    /condominios/{id}
PATCH  /condominios/{id}/configuracoes   # Branding, logotipo, regras de convivência (P5)
GET    /condominios/{id}/blocos
POST   /condominios/{id}/blocos
GET    /blocos/{bloco_id}/unidades
POST   /blocos/{bloco_id}/unidades
GET    /unidades/{id}
GET    /condominios/{id}/vagas-garagem
GET    /condominios/{id}/areas-comuns
POST   /condominios/{id}/areas-comuns
```

---

## 3. Controle de Acesso e IoT (`/api/v1/controle-acesso/`)

Especificações: [biometria-facial-intelbras.md](../funcionalidades/03_controle_acesso/biometria-facial-intelbras.md), [credenciais-e-dispositivos.md](../funcionalidades/03_controle_acesso/credenciais-e-dispositivos.md), [acionamentos-e-eventos.md](../funcionalidades/03_controle_acesso/acionamentos-e-eventos.md).

```http
# Dispositivos e Hardware
GET    /dispositivos-acesso
POST   /dispositivos-acesso
GET    /dispositivos-acesso/{id}/status

# Credenciais e Autorizações
GET    /credenciais-acesso
POST   /credenciais-acesso
POST   /credenciais-acesso/{id}/revogar
GET    /autorizacoes-acesso
POST   /autorizacoes-acesso
PATCH  /autorizacoes-acesso/{id}
POST   /autorizacoes-acesso/{id}/revogar

# Eventos de Passagem e Trilha Pericial
GET    /eventos-acesso                  # Filtro por período, condomínio, unidade, dispositivo

# Integração Intelbras e Provedores (ADR-004, ADR-009)
POST   /integracoes/controle-acesso/sincronizar
POST   /integracoes/controle-acesso/webhook     # Idempotency-Key obrigatória

# Acionamentos Remotos in-app (Fase 4)
POST   /acionamentos/portoes/{dispositivo_id}/abrir
```

> **Idempotência obrigatória:** Operações críticas de biometria facial, autorização, revogação e webhooks exigem cabeçalho `Idempotency-Key: <UUID>` ([ADR-009](../decisoes/ADR-009-idempotencia-integracoes.md)).

---

## 4. Portaria e Atendimento (`/api/v1/portaria/`)

Especificações: [atendimento-visitantes-prestadores.md](../funcionalidades/04_portaria/atendimento-visitantes-prestadores.md), [correspondencias-encomendas.md](../funcionalidades/04_portaria/correspondencias-encomendas.md), [agendamento-mudancas.md](../funcionalidades/04_portaria/agendamento-mudancas.md), [achados-e-perdidos.md](../funcionalidades/04_portaria/achados-e-perdidos.md).

```http
# Atendimento na Guarita
GET    /portaria/visitantes
POST   /portaria/visitantes/entrada-espontanea
POST   /portaria/visitantes/{id}/saida
POST   /portaria/convites-visita
GET    /portaria/convites-visita/validar/{codigo_qr}

# Correspondências e Encomendas
GET    /portaria/encomendas
POST   /portaria/encomendas             # Registro com foto da etiqueta e push notification
POST   /portaria/encomendas/{id}/baixa  # Validação com PIN ou assinatura digital

# Agendamento de Mudanças e Elevador
GET    /portaria/mudancas
POST   /portaria/mudancas/solicitar
PATCH  /portaria/mudancas/{id}/aprovar

# Achados e Perdidos
GET    /portaria/achados-perdidos
POST   /portaria/achados-perdidos
POST   /portaria/achados-perdidos/{id}/restituir
```

---

## 5. Reservas de Espaços Comuns (`/api/v1/reservas/`)

Especificações: [agendamento-espacos.md](../funcionalidades/05_reservas/agendamento-espacos.md), [lista-convidados.md](../funcionalidades/05_reservas/lista-convidados.md), [vistorias-checkin-checkout.md](../funcionalidades/05_reservas/vistorias-checkin-checkout.md).

```http
GET    /reservas/calendario             # Disponibilidade por área comum e data
POST   /reservas/solicitar
GET    /reservas/minhas
DELETE /reservas/{id}/cancelar

# Lista de Convidados da Reserva (visível na Portaria)
GET    /reservas/{id}/convidados
PUT    /reservas/{id}/convidados

# Vistorias Pré e Pós-Uso
POST   /reservas/{id}/vistorias/check-in
POST   /reservas/{id}/vistorias/check-out
```

---

## 6. Comunicação e Convivência (`/api/v1/comunicacao/`)

Especificações: [mural-comunicados.md](../funcionalidades/06_comunicacao/mural-comunicados.md), [ocorrencias-livro.md](../funcionalidades/06_comunicacao/ocorrencias-livro.md), [enquetes-consultas.md](../funcionalidades/06_comunicacao/enquetes-consultas.md), [mural-comunidade.md](../funcionalidades/06_comunicacao/mural-comunidade.md), [canal-fale-conosco.md](../funcionalidades/06_comunicacao/canal-fale-conosco.md).

```http
# Mural de Comunicados
GET    /comunicados
POST   /comunicados
POST   /comunicados/{id}/confirmar-leitura

# Livro de Ocorrências Digital
GET    /ocorrencias
POST   /ocorrencias
GET    /ocorrencias/{id}
POST   /ocorrencias/{id}/mensagens
PATCH  /ocorrencias/{id}/status

# Enquetes e Consultas Públicas
GET    /enquetes
POST   /enquetes/{id}/votar             # Validação estrita: um voto por unidade

# Mural da Comunidade (Classificados)
GET    /comunidade/itens
POST   /comunidade/itens

# Canal Fale Conosco
POST   /fale-conosco/mensagens
```

---

## 7. Governança e Assembleias (`/api/v1/governanca/`)

Especificações: [assembleias-virtuais.md](../funcionalidades/07_governanca/assembleias-virtuais.md), [repositorio-documentos.md](../funcionalidades/07_governanca/repositorio-documentos.md).

```http
# Assembleias Virtuais e Híbridas
GET    /assembleias
POST   /assembleias
GET    /assembleias/{id}
POST   /assembleias/{id}/procuracoes
POST   /assembleias/{id}/pautas/{pauta_id}/votar
GET    /assembleias/{id}/ata

# Repositório Normativo
GET    /documentos-normativos
POST   /documentos-normativos
```

---

## 8. Financeiro e Cobrança (`/api/v1/financeiro/`)

Especificações: [cobranca-e-boletos.md](../funcionalidades/08_financeiro/cobranca-e-boletos.md), [prestacao-contas-e-despesas.md](../funcionalidades/08_financeiro/prestacao-contas-e-despesas.md), [acordos-e-inadimplencia.md](../funcionalidades/08_financeiro/acordos-e-inadimplencia.md).

```http
# Cobrança e Boletos (Fase 4 / pós-P3)
GET    /financeiro/cobrancas/minhas
GET    /financeiro/cobrancas/{id}/boleto-pdf
GET    /financeiro/cobrancas/{id}/pix-qrcode

# Prestação de Contas
GET    /financeiro/balancetes/mensais
GET    /financeiro/balancetes/{id}/documentos

# Acordos e Inadimplência
POST   /financeiro/acordos/simular
POST   /financeiro/acordos/formalizar
```

---

## 9. Manutenção Predial (`/api/v1/manutencao/`)

Especificações: [chamados-e-ordens-servico.md](../funcionalidades/09_manutencao/chamados-e-ordens-servico.md), [manutencao-preventiva-pmo.md](../funcionalidades/09_manutencao/manutencao-preventiva-pmo.md).

```http
# Chamados e Ordens de Serviço
GET    /manutencao/chamados
POST   /manutencao/chamados
POST   /manutencao/chamados/{id}/gerar-os
GET    /manutencao/ordens-servico
PATCH  /manutencao/ordens-servico/{id}/concluir

# Plano de Manutenção Preventiva Obrigatória (PMO / NBR 5674)
GET    /manutencao/pmo/cronograma
POST   /manutencao/pmo/inspecoes/{id}/executar
```

---

## 10. Transversal e SaaS (`/api/v1/transversal/` e `/api/v1/saas/`)

Especificações: [perfis-e-permissoes.md](../funcionalidades/10_transversal_plataforma/perfis-e-permissoes.md), [central-notificacoes.md](../funcionalidades/10_transversal_plataforma/central-notificacoes.md), [planos-e-entitlements.md](../funcionalidades/10_transversal_plataforma/planos-e-entitlements.md).

```http
# Perfil e Contexto do Usuário Conectado
GET    /me
GET    /me/condominios
GET    /me/permissoes

# Notificações PWA
POST   /notificacoes/pwa/inscrever-push
GET    /notificacoes/minhas

# Auditoria Imutável (Somente Administradores)
GET    /auditoria/eventos

# SaaS — Licenciamento e Entitlements (ADR-011)
GET    /saas/planos
GET    /saas/planos/{codigo}
GET    /saas/funcionalidades
GET    /condominios/{id}/assinatura
PUT    /condominios/{id}/assinatura
GET    /condominios/{id}/funcionalidades-habilitadas
PATCH  /condominios/{id}/funcionalidades/{codigo}/override
```

---

## Regras Globais de Autorização e Isolamento

1. **Multi-Tenancy:** O parâmetro `condominio_id` não pode ser forjado pelo cliente; a validação é feita via token JWT + membros da sessão + RLS no PostgreSQL ([ADR-006](../decisoes/ADR-006-isolamento-rls-postgresql.md)).
2. **Feature Entitlements:** Se o condomínio não possuir um módulo ativo no seu plano contratado, a API retorna **HTTP 403 Forbidden** com o payload `{ "detail": "FEATURE_DISABLED", "modulo": "<codigo>" }` ([ADR-011](../decisoes/ADR-011-planos-e-funcionalidades.md)).

## Status deste documento

| Campo | Valor |
|-------|-------|
| Status | `vivo` — referência técnica de rotas |
| Última revisão | 2026-10-17 — Reestruturação completa pelos 9 Bounded Contexts (ADR-013) e 26 specs |
