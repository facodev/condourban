# Guia Mestre de Especificações Funcionais e Regras de Negócio

Este diretório concentra todas as **especificações de requisitos e regras de negócio** do produto CondoUrban, organizadas estritamente de acordo com os **9 Bounded Contexts** (e camada Transversal) estabelecidos na arquitetura modular ([ADR-013](../../docs/decisoes/ADR-013-organizacao-diretorios.md) e [Estrutura.md](../../docs/decisoes/Estrutura.md)).

Cada bounded context conta com seu documento canônico de domínio (`*.md`), detalhando responsabilidades, estrutura de código backend/frontend, entidades SQL, endpoints da API e rastreabilidade, acompanhado das especificações funcionais de cada fluxo.

A matriz completa de correlação técnica está disponível em: **[MAPA.md](MAPA.md)**.

---

## 1. Índice Completo por Bounded Context

### 01. Identidade e Cadastro (`01_identidade_cadastro/`)
Responsável pela modelagem civil de pessoas, contas de acesso autenticáveis, vínculos de membresia e ocupação das unidades, veículos e animais domésticos.
- [identidade-cadastro.md](01_identidade_cadastro/identidade-cadastro.md) — **Documento de Arquitetura do Domínio**: Visão geral, modelos SQL, endpoints e vínculos.
- [onboarding-e-conta.md](01_identidade_cadastro/onboarding-e-conta.md) — Contas de acesso, autenticação JWT + Google OAuth 2.0, convites de membros e tenancy.
- [cadastro-morador-solicitacao.md](01_identidade_cadastro/cadastro-morador-solicitacao.md) — Auto-onboarding de moradores, envio de documentos/selfie e fila de aprovação da gestão.
- [veiculos-e-pets.md](01_identidade_cadastro/veiculos-e-pets.md) — Cadastro de veículos (placas Mercosul/antigas) vinculados a vagas e controle de animais domésticos.

### 02. Estrutura Física do Condomínio (`02_condominio/`)
Representação geoespacial do empreendimento, incluindo torres, unidades residenciais, garagens e áreas de lazer, além das configurações institucionais.
- [condominio.md](02_condominio/condominio.md) — **Documento de Arquitetura do Domínio**: Blocos, unidades, garagens, áreas comuns e configurações.
- [estrutura-fisica.md](02_condominio/estrutura-fisica.md) — Mapeamento de blocos/torres, unidades autônomas, frações ideais, vagas de garagem e áreas comuns.
- [configuracao-condominio.md](02_condominio/configuracao-condominio.md) — Configuração institucional (branding, logotipo, cores) e parâmetros operacionais (horários de silêncio/regras).

### 03. Controle de Acesso e IoT (`03_controle_acesso/`)
Motor operacional de hardware, integrando leitoras faciais, cancelas, antenas RFID/LPR e trilha de eventos de passagem.
- [controle-acesso.md](03_controle_acesso/controle-acesso.md) — **Documento de Arquitetura do Domínio**: Dispositivos IoT, credenciais, regras de acesso e telemetria.
- [biometria-facial-intelbras.md](03_controle_acesso/biometria-facial-intelbras.md) — Captura de templates faciais, integração via adapter `IntelbrasProvider`, sincronização assíncrona e contingência offline.
- [credenciais-e-dispositivos.md](03_controle_acesso/credenciais-e-dispositivos.md) — Gerenciamento de tags RFID, QR Codes dinâmicos com tempo de expiração e antenas LPR para veículos.
- [acionamentos-e-eventos.md](03_controle_acesso/acionamentos-e-eventos.md) — Abertura remota de portões in-app com geofencing e trilha pericial imutável de eventos de passagem.

### 04. Portaria e Atendimento (`04_portaria/`)
Operação da guarita humana ou remota, atendimento ágil na recepção e guarda de encomendas.
- [portaria.md](04_portaria/portaria.md) — **Documento de Arquitetura do Domínio**: Guarita, atendimento de visitantes/prestadores e custódia de encomendas.
- [atendimento-visitantes-prestadores.md](04_portaria/atendimento-visitantes-prestadores.md) — Terminal da portaria, conferência de convites, identificação civil e liberação de visitantes/prestadores.
- [correspondencias-encomendas.md](04_portaria/correspondencias-encomendas.md) — Recebimento com foto da etiqueta, push notification com PIN de retirada e baixa com assinatura digital.
- [agendamento-mudancas.md](04_portaria/agendamento-mudancas.md) — Calendário de mudanças por torre, autorização prévia, regras de elevador de serviço e vistoria pré e pós-uso.
- [achados-e-perdidos.md](04_portaria/achados-e-perdidos.md) — Mural de pertences encontrados nas áreas comuns, guarda na guarita e termo de restituição ao proprietário.

### 05. Reservas de Espaços Comuns (`05_reservas/`)
Gestão de áreas de lazer, termos de responsabilidade e prevenção de conflitos de agenda.
- [reservas.md](05_reservas/reservas.md) — **Documento de Arquitetura do Domínio**: Ciclo de reservas, listas de convidados e vistorias pré/pós.
- [agendamento-espacos.md](05_reservas/agendamento-espacos.md) — Calendário interativo de reservas (salões de festas, churrasqueiras, quadras), regras de concorrência e taxas.
- [lista-convidados.md](05_reservas/lista-convidados.md) — Cadastro e gestão da lista de convidados embutida na reserva, sincronizada em tempo real com a portaria.
- [vistorias-checkin-checkout.md](05_reservas/vistorias-checkin-checkout.md) — Vistoria de entrada e saída com fotos obrigatórias, checklist de patrimônio e liberação de caução.

### 06. Comunicação e Ocorrências (`06_comunicacao/`)
Canais de relacionamento oficial, livro de ocorrências digital e engajamento da comunidade.
- [comunicacao.md](06_comunicacao/comunicacao.md) — **Documento de Arquitetura do Domínio**: Comunicados, mensageria, ocorrências e mural social.
- [mural-comunicados.md](06_comunicacao/mural-comunicados.md) — Avisos oficiais da gestão, comunicados urgentes, segmentação por bloco e confirmação obrigatória de leitura.
- [ocorrencias-livro.md](06_comunicacao/ocorrencias-livro.md) — Livro de ocorrências unificado (`tipo_origem = 'PORTARIA' | 'MORADOR' | 'GESTAO'`), linha do tempo e controle de sigilo.
- [enquetes-consultas.md](06_comunicacao/enquetes-consultas.md) — Consultas de opinião da comunidade, apuração em tempo real e regra de um voto por unidade.
- [mural-comunidade.md](06_comunicacao/mural-comunidade.md) — Classificados de itens usados, doações, indicações de serviços entre vizinhos e moderação ativa.
- [canal-fale-conosco.md](06_comunicacao/canal-fale-conosco.md) — Canal direto de suporte e mensageria privada do morador com o síndico e a administradora.

### 07. Governança e Assembleias (`07_governanca/`)
Deliberações formais do condomínio, atas digitais e repositório normativo.
- [governanca.md](07_governanca/governanca.md) — **Documento de Arquitetura do Domínio**: Assembleias, pautas, votação digital, atas e auditoria.
- [assembleias-virtuais.md](07_governanca/assembleias-virtuais.md) — Assembleias virtuais e híbridas (Lei 14.309/2022), procurações digitais, quórum qualificado, votações ao vivo e geração de ata.
- [repositorio-documentos.md](07_governanca/repositorio-documentos.md) — Biblioteca digital de convenção, regimento interno, apólices de seguro, contratos e laudos obrigatórios.

### 08. Financeiro e Cobrança (`08_financeiro/`)
Operações financeiras, emissão de cobranças, transparência e controle de inadimplência.
- [financeiro.md](08_financeiro/financeiro.md) — **Documento de Arquitetura do Domínio**: Boletos bancários, Pix, conciliação, acordos e medições.
- [cobranca-e-boletos.md](08_financeiro/cobranca-e-boletos.md) — Emissão de cotas condominiais, linha digitável, Pix dinâmico instantâneo, 2ª via atualizada e conciliação bancária.
- [prestacao-contas-e-despesas.md](08_financeiro/prestacao-contas-e-despesas.md) — Painel digital de balancetes mensais, gráficos de receitas/despesas, visualização de notas fiscais e parecer do conselho fiscal.
- [acordos-e-inadimplencia.md](08_financeiro/acordos-e-inadimplencia.md) — Simulação e formalização de termos de confissão e parcelamento de dívidas e régua de cobrança amigável.

### 09. Manutenção Predial (`09_manutencao/`)
Conservação física do patrimônio, vistorias prediais e cumprimento da NBR 5674.
- [manutencao.md](09_manutencao/manutencao.md) — **Documento de Arquitetura do Domínio**: Chamados corretivos, ordens de serviço, cronograma PMO e inventário.
- [chamados-e-ordens-servico.md](09_manutencao/chamados-e-ordens-servico.md) — Chamados de manutenção corretiva, triagem, atribuição de Ordens de Serviço (OS) ao zelador e fotos do reparo.
- [manutencao-preventiva-pmo.md](09_manutencao/manutencao-preventiva-pmo.md) — Plano de Manutenção Obrigatória (PMO), cronograma de inspeções preventivas (extintores, gerador, caixas d'água).

### 10. Transversal e Plataforma (`10_transversal_plataforma/`)
Infraestrutura de segurança, notificações e modelo comercial SaaS.
- [transversal.md](10_transversal_plataforma/transversal.md) — **Documento de Arquitetura do Domínio**: Fundações transversais, RLS, segurança JWT, PWA e notificações.
- [perfis-e-permissoes.md](10_transversal_plataforma/perfis-e-permissoes.md) — Matriz canônica de Controle de Acesso Baseado em Papéis (RBAC) e guards de rota.
- [central-notificacoes.md](10_transversal_plataforma/central-notificacoes.md) — Motor de notificações multicanal (Push PWA via VAPID, e-mails transacionais e alertas na interface).
- [planos-e-entitlements.md](10_transversal_plataforma/planos-e-entitlements.md) — Catálogo de planos SaaS, modelo de entitlements (`funcionalidade_habilitada`) e bloqueio 403 `FEATURE_DISABLED`.

---

## 2. Matriz de Perfis de Usuário no Sistema

| Papel no Sistema | Escopo Operacional | Módulos com Acesso Típico |
| :--- | :--- | :--- |
| **Morador (Titular)** | Unidade residencial | Onboarding, Veículos/Pets, Encomendas, Visitantes, Reservas, Ocorrências, Boletos/Pix, Assembleias, Documentos. |
| **Dependente** | Unidade residencial | Perfil do titular com restrição padrão a finanças e votação de assembleia (conforme convenção). |
| **Porteiro / Guarita** | Controle de Acesso e Guarita | Terminal de Atendimento (Visitantes/Prestadores), Recebimento e Baixa de Encomendas, Ocorrências da Portaria, Painel de Presentes. |
| **Zelador** | Operação e Manutenção | Ordens de Serviço (OS), Checklist do PMO, Vistorias de Áreas Comuns (Check-in/Check-out), Ocorrências de Manutenção. |
| **Síndico / Subsíndico** | Condomínio | Gestão total de todos os 9 módulos do condomínio, aprovação de cadastros, comunicados, assembleias, finanças e regras. |
| **Conselho Fiscal** | Fiscalização Contábil | Acesso de leitura aos balancetes mensais, notas fiscais, lançamentos de despesas e emissão de pareceres do conselho. |
| **Administradora** | Multi-Condomínio | Operação financeira, emissão de faturamento em lote, apoio ao síndico e atendimento aos moradores. |
| **Admin da Plataforma** | Global (SaaS) | Gestão de planos comerciais, overrides operacionais, auditoria de segurança e infraestrutura. |

---

## 3. Padrão de Manutenção de Especificações

Todas as novas especificações funcionais ou alterações em comportamentos de telas e fluxos devem seguir rigorosamente o modelo documentado em [\_template.md](_template.md).
