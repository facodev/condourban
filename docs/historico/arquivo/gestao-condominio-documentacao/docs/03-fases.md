# Fases do produto

## Fase 0 — Fundação

### Objetivo
Criar a base técnica.

### Entregas
- repositório;
- Docker;
- PostgreSQL;
- Redis;
- Keycloak;
- FastAPI;
- Angular 22;
- CI/CD;
- observabilidade;
- migrations;
- RLS;
- auditoria.

---

## Fase 1 — Condomínio e identidade

### Objetivo
Cadastrar a estrutura física e as pessoas.

### Entregas
- condomínio;
- blocos;
- unidades;
- vagas;
- pessoas;
- usuários;
- papéis;
- membros;
- ocupações;
- veículos;
- animais.

---

## Fase 2 — Auto-cadastro de moradores

### Objetivo
Permitir credenciamento digital.

### Fluxo

```text
Convite
  -> dados pessoais
  -> documento
  -> comprovante de vínculo
  -> facial
  -> prova de vida
  -> aceite/informações
  -> análise
  -> aprovação
```

### Entregas
- convite;
- solicitação;
- upload;
- análise;
- correção;
- aprovação;
- rejeição;
- auditoria.

---

## Fase 3 — Controle facial Intelbras

### Objetivo
Transformar a aprovação em autorização de acesso.

### Entregas
- provedor Intelbras;
- dispositivos;
- credenciais;
- autorizações;
- fila de sincronização;
- eventos;
- revogação;
- tratamento de indisponibilidade;
- reconciliação.

### Regra
A integração deve ser assíncrona e idempotente.

---

## Fase 4 — Visitantes e prestadores

### Entregas
- convite;
- QR Code;
- cadastro facial;
- autorização temporária;
- janela de horário;
- entrada;
- saída;
- histórico.

---

## Fase 5 — Portaria digital

### Entregas
- encomendas;
- ocorrências;
- comunicação;
- notificações;
- painel da portaria;
- autorização rápida de visitante.

---

## Fase 6 — Experiência do morador

### Entregas
- reservas;
- comunicados;
- documentos;
- enquetes;
- mural;
- perfil;
- veículos;
- animais.

---

## Fase 7 — Assembleias

### Entregas
- assembleias;
- Zoom;
- participantes;
- pautas;
- votação;
- quorum;
- auditoria.

---

## Fase 8 — Financeiro

### Entregas
- cobranças;
- boletos;
- pagamentos;
- conciliação;
- relatórios.

Pagamento recorrente por cartão deve ser tratado posteriormente e sem armazenamento de dados de cartão.

---

## Fase 9 — Integrações avançadas

### Entregas
- novos fabricantes;
- automações;
- sensores;
- integrações financeiras;
- notificações externas;
- analytics.

---

# MVP recomendado

O MVP comercial deve priorizar:

1. Condomínio
2. Unidades
3. Pessoas
4. Auto-cadastro
5. Aprovação
6. Facial
7. Intelbras
8. Visitantes
9. Prestadores
10. Portaria
11. Encomendas
12. Comunicação

A assembleia completa e o ERP financeiro podem entrar depois.
