# ADR-004: Integração Intelbras (reconhecimento facial) + pré-cadastro

- **Status:** Aceito (produto); detalhes de API Intelbras ainda a fechar (I1–I4)
- **Data:** 2026-09-29
- **Relacionado:** [ADR-001](ADR-001-documentacao-e-stack-tecnologica.md), [ADR-009](ADR-009-idempotencia-integracoes.md), [08-intelbras-facial-e-reservas.md](../plano/08-intelbras-facial-e-reservas.md)

## Contexto

O produto deve:

1. Ter **reservas** de áreas comuns (obrigatório; entrega Fase 2 — F3).
2. Integrar com **Intelbras** para **reconhecimento facial**.
3. Liberar pessoas via **pré-cadastro** com captura/associação facial.

Biometria e hardware de acesso não podem ficar acoplados ao front Angular: precisam de adaptador no backend Python, filas e LGPD rigorosa.

## Decisão

1. **Reservas** permanecem no catálogo e na **Fase 2** (obrigatórias).
2. **Pré-cadastro + liberação facial** entram no domínio `access` da API, com consentimento LGPD.
3. Integração Intelbras via **`AccessControlProvider`** (padrão adapter); primeira implementação `IntelbrasProvider`.
4. Entrega da integração: **Fase 2** (junto com portaria), piloto em condomínio real.
5. Eventos de acesso — `AccessLog` no nosso banco; sync assíncrono (Celery).
6. QR/código continua como **fallback** se facial ou Intelbras falhar.

## Alternativas consideradas

1. **Só QR sem facial** — rejeitado (requisito Intelbras/facial).
2. **SDK só no front** — rejeitado (segurança, biometria, multi-tenant).
3. **Acoplar regras de negócio ao software Intelbras** — rejeitado; nosso sistema é fonte da verdade de quem pode entrar.

## Consequências

### Positivas

- Troca/evolução de firmware Intelbras isolada no adaptador.
- Mesmo modelo permite outro fabricante depois.
- Auditoria e LGPD centralizadas.

### Riscos

- APIs/documentação Intelbras variam por linha de produto (Control iD, InControl, SS, etc.) — **fechar I1**.
- Rede do condomínio (VPS na nuvem — dispositivos on-prem) pode exigir VPN/túnel — **fechar I2**.
- Captura de face no browser (webcam) vs tablet de portaria — UX e qualidade da imagem.

## Referências

- [06-produto-completo-modulos.md](../plano/06-produto-completo-modulos.md)
- [05-perguntas-abertas.md](../plano/05-perguntas-abertas.md) (F5, F6, I1–I4)
