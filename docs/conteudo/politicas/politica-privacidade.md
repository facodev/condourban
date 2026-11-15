# Política de Privacidade (rascunho 0.2-draft)

> **Status:** rascunho — não é texto jurídico final. Revisar com assessoria antes de publicar.
> **Versão:** 0.2-draft · **Última revisão:** 2026-09-29

## 1. Controlador e contato

**CondoUrban** opera a plataforma de gestão de condomínios. Contato do encarregado/DPO: [a definir].

## 2. Dados que tratamos

- Cadastro: nome, e-mail, telefone, unidade, papel no condomínio
- Conteúdo gerado: comunicados lidos, ocorrências, reservas, autorizações
- Dependentes/menores: com cuidados e consentimento do responsável (C2)
- **Biometria facial** (quando o condomínio ativar Intelbras): imagem/template para controle de acesso, com consentimento (F5/F6)
- Dados técnicos: logs de acesso ao sistema, IP, dispositivo (segurança)
- **Auditoria**: registro de ações sensíveis (ex.: mudança de papel, liberação de acesso)
- **Logs de uso**: eventos de produto/API agregáveis (capacidade, melhoria do serviço) — sem vender dados pessoais

## 3. Finalidades

Prestação do serviço SaaS; comunicação do condomínio; segurança de acesso físico e da plataforma (incluindo prevenção a abuso/DDoS); cumprimento legal; melhoria do produto (agregado/anônimo quando possível); garantia de continuidade e suporte enquanto o serviço estiver ativo (ver Termos §5–§6).

## 4. Compartilhamento

- Com a **administradora/síndico** do seu condomínio (operadores no tenant)
- Com **Intelbras** (ou equipamento no local), somente para sync de liberação facial quando habilitado
- Prestadores de infra (VPS, e-mail, storage) sob contrato

## 5. Retenção, exclusão e continuidade do app

1. Retemos dados enquanto houver **vínculo com o condomínio/conta**, obrigação legal ou necessidade de segurança/auditoria (prazos por tipo de log — plano de segurança doc 13).
2. Você pode solicitar **exportação** e **exclusão** conforme fluxos da Fase 1 (C1), observados direitos de outros titulares e deveres do controlador do condomínio.
3. Se o serviço for **descontinuado** ou o contrato encerrado (Termos §6), disponibilizamos janela razoável de exportação; após isso, dados são eliminados ou anonimizados, salvo retenção legal.
4. Cópias em backups de segurança são purgadas conforme ciclo de backup (provisão: até o prazo do backup + rotina de limpeza).

## 6. Disponibilidade e tratamento durante indisponibilidade

Durante manutenção ou incidente, o tratamento de dados continua submetido a esta política. Logs de incidente/ops podem ser gerados para diagnóstico, com retenção curta e acesso restrito. Detalhes de uptime e aviso de manutenção estão nos **Termos de Uso §5**.

## 7. Atualizações desta política

Mudanças materiais geram **nova versão** e, quando aplicável, novo aceite no app. Ver ritual em `docs/plano/10-seguranca-faq-politicas-ritual.md`.

## Changelog legal

| Versão | Data | Mudança |
|--------|------|---------|
| 0.1-draft | 2026-09-29 | Estrutura inicial + biometria/Intelbras prevista |
| 0.1.1-draft | 2026-09-29 | Auditoria, logs de uso e segurança de plataforma |
| 0.2-draft | 2026-09-29 | Retenção/continuidade do app; disponibilidade e incidentes |
