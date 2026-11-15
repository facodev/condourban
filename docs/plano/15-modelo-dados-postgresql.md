# Modelo de dados PostgreSQL

DDL de referência em [`docs/sql/`](../sql/README.md). Este documento descreve entidades, glossário EN↔PT e alinhamento com o roadmap vigente ([03](03-roadmap-e-entregas.md), [14](14-revisao-plano-consolidada.md)).

## Princípios (consolidados)

1. Monólito modular com isolamento estrito de módulos pelos **9 Bounded Contexts** ([ADR-013](../decisoes/ADR-013-organizacao-diretorios.md)).
2. Isolamento por condomínio: `condominio_id` + **RLS** no PostgreSQL ([ADR-006](../decisoes/ADR-006-isolamento-rls-postgresql.md)).
3. Autenticação **na aplicação**: e-mail/senha **e** Google OAuth 2.0 (Gmail) — **sem Keycloak** ([ADR-007](../decisoes/ADR-007-autenticacao-jwt-aplicacao.md)).
4. `pessoa` ≠ `usuario` ([ADR-008](../decisoes/ADR-008-pessoa-e-usuario.md)).
5. Aprovação cadastral **≠** sincronização Intelbras ([ADR-004](../decisoes/ADR-004-integracao-intelbras-facial.md), [ADR-009](../decisoes/ADR-009-idempotencia-integracoes.md)).
6. Arquivos binários fora do PostgreSQL (S3-compatible); banco só metadados + chave.
7. Biometria: preferir referência no provedor; template bruto só se necessidade comprovada.
8. Nomes de negócio em **pt-BR** nas tabelas ([ADR-010](../decisoes/ADR-010-nomenclatura-pt-br.md)).

## Glossário (conceito ↔ tabela)

| Conceito (docs EN / arquitetura) | Tabela / enum |
|----------------------------------|---------------|
| Organization / administradora SaaS | `inquilino` |
| Condominium | `condominio` |
| Block / Unit | `bloco` / `unidade` |
| Parking spot / Amenity | `vaga_garagem` / `area_comum` |
| Person / User | `pessoa` / `usuario` |
| Membership | `membro_condominio` + `ocupacao_unidade` |
| Invite (morador) | `convite_cadastro_morador` |
| Cadastro request | `solicitacao_cadastro_morador` |
| Face enrollment | `verificacao_facial` + `credencial_acesso` |
| AccessGrant | `autorizacao_acesso` |
| AccessLog / device | `evento_acesso` / `dispositivo_acesso` |
| Sync job | `sincronizacao_acesso` |
| Visitor / Delivery | `visitante` / `encomenda` |
| Reservation | `reserva` |
| Ticket / Announcement / Poll | `ocorrencia` / `comunicado` / `enquete` |
| Assembly | `assembleia` (+ pautas/votos) |
| Charge | `cobranca_condominial` |
| AuditLog | `evento_auditoria` |
| Plan / Subscription / Feature entitlement | `plano`, `assinatura`, `funcionalidade`, `plano_funcionalidade`, `condominio_funcionalidade` |

## Mapa de Tabelas por Bounded Context (9 Contextos Canônicos)

| # | Bounded Context (`pt-BR`) | Tabelas Principais (DDL pt-BR) | Pilar de Negócio Correspondente |
|---|---------------------------|--------------------------------|---------------------------------|
| 1 | **`identidade_cadastro`** | `pessoa`, `usuario`, `membro_condominio`, `ocupacao_unidade`, `convite_cadastro_morador`, `solicitacao_cadastro_morador`, `documento_cadastro`, `veiculo`, `pet` | 1. Cadastro e Identidade |
| 2 | **`condominio`** | `inquilino`, `condominio`, `bloco`, `unidade`, `vaga_garagem`, `area_comum`, `configuracao_condominio` | 3. Condomínio |
| 3 | **`controle_acesso`** ⭐ | `integracao_provedor`, `dispositivo_acesso`, `credencial_acesso`, `autorizacao_acesso`, `evento_acesso`, `sincronizacao_acesso`, `verificacao_facial` | 2. Controle de Acesso ⭐ |
| 4 | **`portaria`** | `visitante`, `registro_visita`, `encomenda`, `registro_entrega`, `agendamento_mudanca`, `item_perdido` | 4. Experiência do Morador / 2. Acesso |
| 5 | **`reservas`** | `reserva`, `regra_espaco`, `convidado_reserva`, `vistoria_reserva` | 4. Experiência do Morador / 3. Condomínio |
| 6 | **`comunicacao`** | `comunicado`, `leitura_comunicado`, `ocorrencia`, `historico_ocorrencia`, `enquete`, `opcao_enquete`, `voto_enquete`, `item_comunidade`, `mensagem_fale_conosco` | 4. Experiência do Morador |
| 7 | **`governanca`** | `assembleia`, `pauta_assembleia`, `voto_assembleia`, `procuracao_assembleia`, `ata_assembleia`, `documento_normativo` | 4. Experiência do Morador |
| 8 | **`financeiro`** | `cobranca_condominial`, `fatura`, `pagamento`, `conciliacao_bancaria`, `termo_acordo` | 5. Administração |
| 9 | **`manutencao`** | `chamado_manutencao`, `ordem_servico`, `item_preventiva_pmo`, `registro_inspecao_pmo`, `prestador_servico` | 5. Administração / 4. Morador |
| 10 | **`transversal`** | `evento_auditoria`, `plano`, `assinatura`, `funcionalidade`, `plano_funcionalidade`, `condominio_funcionalidade`, `evento_uso` | 5. Administração / Plataforma |

## Identidade (diagrama)

```text
E-mail+senha  e/ou  Google OAuth (Gmail)
        |
        v
     usuario  (senha_hash? · google_sub?)
        |
        v
     pessoa
        |
        +--> membro_condominio
        +--> ocupacao_unidade
        +--> credencial_acesso --> autorizacao_acesso --> dispositivo
```

## Multitenancy e arquivos

- Isolamento operacional = **condomínio**.
- Sessão: `SET LOCAL app.condominio_id = '…'` após validar associação.
- Objetos:

```text
condominio/{condominio_id}/
  cadastros/{solicitacao_id}/
  documentos/{documento_id}/
  pessoas/{pessoa_id}/
  ocorrencias/{ocorrencia_id}/
```

## Eventos de domínio (assíncronos)

`CadastroAprovado` · `PessoaAtivada` · `CredencialCriada` · `AutorizacaoCriada` · `CredencialSincronizada` · `AcessoAutorizado` · `AcessoNegado` · `EncomendaRecebida` · `ReservaCriada`

## Crosswalk de fases (export legado × roadmap vigente)

O pacote arquivado `historico/arquivo/gestao-condominio-documentacao` numerava fases de forma diferente. **Canônico = docs 03/06/14.**

| Export legado | Roadmap vigente |
|---------------|-----------------|
| Fase 0 Fundação (Docker, auth, RLS…) | Etapa 0 docs + **Fase 1** fundação (SQLite→Postgres; JWT na API — sem Keycloak) |
| Fase 1 Estrutura + pessoas + veículos/pets | **Fase 1** (blocos/unidades/pessoas) + **Fase 2** (auto/pets) |
| Fase 2 Auto-cadastro morador | **Fase 1–2** (onboarding F1; solicitação+docs+facial na F2 com acesso) |
| Fase 3 Facial Intelbras | **Fase 2** |
| Fase 4 Visitantes/prestadores | **Fase 2** (visitantes) / **Fase 3** (prestadores/OS) |
| Fase 5 Portaria digital | **Fase 2** (encomendas, notificações, portal portaria) |
| Fase 6 Experiência morador (reservas, comunicados…) | Comunicados **F1**; reservas/enquetes **F2** |
| Fase 7 Assembleias | **Fase 3** |
| Fase 8 Financeiro | Pós-**P3** / **Fase 4** |
| Fase 9 Integrações avançadas | **Fases 4–9** (acionamentos, IoT, analytics) |

**MVP do export** (condomínio → facial → portaria → encomendas) ≈ fatia **F1 + F2** do roadmap atual.

## Lacunas do DDL vs produto

- Sem tabelas de veículos/pets/RBAC granular / `UsageEvent`.
- Chat (`conversa`) no DDL mas **fora do escopo**.
- Faturas da plataforma (`InvoicePlatform`) ainda conceituais; **entitlement** já em [013](../sql/013-saas-planos-e-funcionalidades.sql) / [ADR-011](../decisoes/ADR-011-planos-e-funcionalidades.md).

## Status

| Campo | Valor |
|-------|-------|
| Status | `vivo` |
| Última revisão | 2026-10-17 — mapeamento completo por 9 Bounded Contexts (ADR-013) |
