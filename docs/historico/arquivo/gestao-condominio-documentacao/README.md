# Gestão Condomínio — ARQUIVO (não canônico)

> **Substituído.** Conteúdo absorvido e atualizado em [`docs/`](../../../README.md) em 2026-09-29.  
> Este pacote ainda menciona **Keycloak** — decisão revertida; auth canônica = [ADR-007](../../../decisoes/ADR-007-autenticacao-jwt-aplicacao.md).  
> Ver [arquivo/README.md](../README.md).

Plataforma SaaS multitenant para gestão condominial, experiência do morador e controle de acesso.

## Stack inicial

- Backend: Python + FastAPI
- Frontend: Angular 22 PWA
- Banco: PostgreSQL
- Cache: Redis
- Identidade: Keycloak / OIDC / JWT
- Arquivos: armazenamento de objetos compatível com S3
- Controle de acesso: Intelbras na primeira fase
- Containers: Docker
- Orquestração: Kubernetes/OpenShift
- CI/CD: GitLab CI
- Observabilidade: OpenTelemetry + Prometheus + Grafana + Loki + Tempo

## Princípios

1. Monólito modular na primeira fase.
2. Isolamento por condomínio com `condominio_id` e PostgreSQL RLS.
3. Keycloak é a fonte de verdade da autenticação.
4. O banco guarda identidade e autorização de negócio, não senhas.
5. Biometria facial é tratada como dado sensível e possui ciclo de vida próprio.
6. A integração com a Intelbras ocorre por adaptador/provedor.
7. Aprovação cadastral e sincronização com controle de acesso são processos distintos.
8. Falha da Intelbras não deve desfazer uma aprovação válida.
9. Arquivos binários ficam fora do PostgreSQL.
10. Todas as operações relevantes devem possuir auditoria.

## Estrutura

```text
docs/
  01-arquitetura.md
  02-adrs.md
  03-fases.md
  04-cadastro-morador.md
  05-controle-acesso.md
  06-seguranca-lgpd.md
  07-api.md

sql/
  001-extensoes-e-tipos.sql
  002-nucleo-condominio.sql
  003-identidade-e-cadastro.sql
  004-controle-acesso.sql
  005-modulos-operacionais.sql
  006-rls.sql
  007-seed-inicial.sql
```

## Ordem de execução SQL

Executar os arquivos de `001` a `007` em ordem.
