BEGIN;

-- 1. Motivos padronizados de correção no onboarding cadastral
INSERT INTO motivo_correcao_cadastro (codigo, descricao)
VALUES
    ('DOCUMENTO_ILEGIVEL', 'Documento ilegível ou com baixa resolução'),
    ('DOCUMENTO_INCOMPLETO', 'Documento incompleto (falta frente ou verso)'),
    ('DOCUMENTO_INVALIDO', 'Documento vencido ou inválido'),
    ('DADOS_DIVERGENTES', 'Dados preenchidos divergentes do documento anexado'),
    ('COMPROVANTE_INSUFICIENTE', 'Comprovante de vínculo com a unidade insuficiente'),
    ('FACIAL_INCONCLUSIVA', 'Foto de selfie / biometria facial inconclusiva'),
    ('PROVA_VIDA_REPROVADA', 'Prova de vida reprovada ou com iluminação inadequada'),
    ('OUTRO', 'Outro motivo informado nas observações')
ON CONFLICT (codigo) DO UPDATE
SET descricao = EXCLUDED.descricao;

-- 2. Catálogo canônico de funcionalidades da plataforma (códigos estáveis)
INSERT INTO funcionalidade (codigo, nome, descricao, escopo, permitir_desligar_no_condo, ordem)
VALUES
    -- Módulos de Núcleo (Core Obrigatório)
    ('comunicados', 'Comunicados Oficiais', 'Mural e avisos institucionais do condomínio', 'NUCLEO', false, 10),
    ('ocorrencias', 'Livro de Ocorrências', 'Registro unificado de ocorrências (morador e portaria)', 'NUCLEO', false, 20),
    ('documentos', 'Repositório de Documentos', 'Biblioteca regulatória e atas', 'NUCLEO', false, 30),
    ('notificacoes', 'Central de Notificações', 'Notificações push PWA, e-mail e in-app', 'NUCLEO', false, 40),
    ('onboarding', 'Onboarding e Cadastro', 'Convites, solicitações de moradores e aprovação', 'NUCLEO', false, 50),
    ('fale_conosco', 'Canal Fale Conosco', 'Mensageria privada morador ↔ administração', 'NUCLEO', false, 60),

    -- Módulos Operacionais Opcionais
    ('reservas', 'Reservas de Espaços', 'Áreas comuns, convidados e vistorias com caução', 'OPCIONAL', true, 100),
    ('correspondencias', 'Gestão de Encomendas', 'Recebimento com foto e baixa por código', 'OPCIONAL', true, 110),
    ('visitantes', 'Portaria e Visitantes', 'Terminal de guarita, visitantes e prestadores', 'OPCIONAL', true, 120),
    ('veiculos_pets', 'Veículos e Pets', 'Cadastro de veículos (LPR) e animais da unidade', 'OPCIONAL', true, 125),
    ('enquetes', 'Enquetes e Votações Rápidas', 'Consultas de opinião à comunidade', 'OPCIONAL', true, 130),
    ('assembleias', 'Assembleias Virtuais', 'Convocação, procurações, votação ao vivo e atas', 'OPCIONAL', true, 140),
    ('mudanca', 'Agendamento de Mudança', 'Reserva de elevador de serviço e vistorias', 'OPCIONAL', true, 150),
    ('achados_perdidos', 'Achados e Perdidos', 'Custódia e devolução de pertences na portaria', 'OPCIONAL', true, 160),

    -- Módulos de Controle de Acesso e Hardware (IoT)
    ('facial_intelbras', 'Biometria Facial Intelbras', 'Sync automático de faces e credenciais com hardware', 'OPCIONAL', true, 200),
    ('acionamentos', 'Acionamento Remoto', 'Abertura remota in-app de portas e portões com geofence', 'OPCIONAL', true, 210),

    -- Manutenção e Operação Predial
    ('manutencao_os', 'Ordens de Serviço e Reparos', 'Chamados corretivos e acompanhamento de OS', 'OPCIONAL', true, 300),
    ('pmo_preventivo', 'Manutenção Preventiva (PMO)', 'Cronograma NBR 5674 e laudos técnicos com ART', 'OPCIONAL', true, 310),

    -- Módulos Avançados e Financeiro
    ('financeiro', 'Financeiro e Cobrança', 'Boletos, Pix instantâneo, conciliação e balancetes', 'OPCIONAL', true, 400),
    ('medicao_individual', 'Medições Individuais', 'Leitura e rateio de água e gás', 'OPCIONAL', true, 410),
    ('comunidade', 'Mural Social e Classificados', 'Classificados e avisos sociais entre condôminos', 'OPCIONAL', true, 500),
    ('personalizacao', 'Branding Institucional', 'Logo, cores e personalização do condomínio', 'OPCIONAL', false, 600),
    ('whatsapp', 'Notificações WhatsApp', 'Disparo de avisos urgentes via bot de WhatsApp', 'OPCIONAL', true, 700)
ON CONFLICT (codigo) DO UPDATE
SET
    nome = EXCLUDED.nome,
    descricao = EXCLUDED.descricao,
    escopo = EXCLUDED.escopo,
    permitir_desligar_no_condo = EXCLUDED.permitir_desligar_no_condo,
    ordem = EXCLUDED.ordem,
    atualizado_em = now();

-- 3. Planos Comerciais (Tiers SaaS)
INSERT INTO plano (codigo, nome, descricao, max_unidades, preco_mensal_centavos, preco_exibicao, publico, ordem)
VALUES
    (
        'starter',
        'Starter',
        'Comunicação, comunicados e operação básica para condomínios compactos',
        40,
        14900,
        'A partir de R$ 149/mês',
        true,
        10
    ),
    (
        'essencial',
        'Essencial',
        'Portaria digital, encomendas, visitantes, reservas e assembleias',
        120,
        34900,
        'A partir de R$ 349/mês',
        true,
        20
    ),
    (
        'acesso',
        'Acesso & IoT',
        'Integração total com reconhecimento facial Intelbras e acionamento remoto',
        300,
        59900,
        'A partir de R$ 599/mês',
        true,
        30
    ),
    (
        'administradora',
        'Administradora / Enterprise',
        'Plataforma completa: financeiro, manutenção preventiva PMO e multi-condomínio',
        NULL,
        99900,
        'Sob consulta',
        true,
        40
    )
ON CONFLICT (codigo) DO UPDATE
SET
    nome = EXCLUDED.nome,
    descricao = EXCLUDED.descricao,
    max_unidades = EXCLUDED.max_unidades,
    preco_mensal_centavos = EXCLUDED.preco_mensal_centavos,
    preco_exibicao = EXCLUDED.preco_exibicao,
    publico = EXCLUDED.publico,
    ordem = EXCLUDED.ordem,
    atualizado_em = now();

-- 4. Associação de Funcionalidades aos Planos
-- Starter: Núcleo + Reservas
INSERT INTO plano_funcionalidade (plano_id, funcionalidade_id, incluido)
SELECT p.id, f.id, true
FROM plano p, funcionalidade f
WHERE p.codigo = 'starter'
  AND f.codigo IN ('comunicados', 'ocorrencias', 'documentos', 'notificacoes', 'onboarding', 'fale_conosco', 'reservas', 'enquetes', 'veiculos_pets')
ON CONFLICT (plano_id, funcionalidade_id) DO UPDATE SET incluido = EXCLUDED.incluido;

-- Essencial: Starter + Portaria, Encomendas, Assembleias, Mudança, Achados
INSERT INTO plano_funcionalidade (plano_id, funcionalidade_id, incluido)
SELECT p.id, f.id, true
FROM plano p, funcionalidade f
WHERE p.codigo = 'essencial'
  AND f.codigo IN (
      'comunicados', 'ocorrencias', 'documentos', 'notificacoes', 'onboarding', 'fale_conosco',
      'reservas', 'enquetes', 'veiculos_pets', 'correspondencias', 'visitantes', 'assembleias',
      'mudanca', 'achados_perdidos'
  )
ON CONFLICT (plano_id, funcionalidade_id) DO UPDATE SET incluido = EXCLUDED.incluido;

-- Acesso & IoT: Essencial + Facial Intelbras + Acionamentos
INSERT INTO plano_funcionalidade (plano_id, funcionalidade_id, incluido)
SELECT p.id, f.id, true
FROM plano p, funcionalidade f
WHERE p.codigo = 'acesso'
  AND f.codigo IN (
      'comunicados', 'ocorrencias', 'documentos', 'notificacoes', 'onboarding', 'fale_conosco',
      'reservas', 'enquetes', 'veiculos_pets', 'correspondencias', 'visitantes', 'assembleias',
      'mudanca', 'achados_perdidos', 'facial_intelbras', 'acionamentos'
  )
ON CONFLICT (plano_id, funcionalidade_id) DO UPDATE SET incluido = EXCLUDED.incluido;

-- Administradora: Todas as funcionalidades
INSERT INTO plano_funcionalidade (plano_id, funcionalidade_id, incluido)
SELECT p.id, f.id, true
FROM plano p, funcionalidade f
WHERE p.codigo = 'administradora'
ON CONFLICT (plano_id, funcionalidade_id) DO UPDATE SET incluido = EXCLUDED.incluido;

COMMIT;
