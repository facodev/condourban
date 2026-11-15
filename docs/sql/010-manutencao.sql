BEGIN;

-- Contexto: manutencao
-- Gestão patrimonial e conservação predial: chamados de reparo, ordens de serviço e cronograma preventivo (PMO / NBR 5674)

CREATE TABLE chamado_manutencao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID REFERENCES unidade(id),
    solicitante_id UUID NOT NULL REFERENCES pessoa(id),
    categoria VARCHAR(50) NOT NULL, -- 'ELETRICA', 'HIDRAULICA', 'CIVIL', 'ELEVADORES', 'PINTURA', 'OUTRO'
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    localizacao VARCHAR(200),
    foto_url TEXT,
    prioridade prioridade_chamado NOT NULL DEFAULT 'MEDIA',
    status status_chamado NOT NULL DEFAULT 'ABERTO',
    atribuido_a UUID REFERENCES pessoa(id),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    concluido_em TIMESTAMPTZ
);

CREATE INDEX ix_chamado_status ON chamado_manutencao(condominio_id, status, prioridade);

CREATE TABLE ordem_servico (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    chamado_id UUID REFERENCES chamado_manutencao(id),
    prestador_id UUID REFERENCES prestador(id),
    responsavel_interno_id UUID REFERENCES pessoa(id),
    descricao TEXT NOT NULL,
    valor_estimado NUMERIC(12,2),
    valor_final NUMERIC(12,2),
    data_agendada DATE,
    status status_ordem_servico NOT NULL DEFAULT 'RASCUNHO',
    laudo_conclusao TEXT,
    iniciado_em TIMESTAMPTZ,
    finalizado_em TIMESTAMPTZ,
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_ordem_servico_condo ON ordem_servico(condominio_id, status);

-- Plano de Manutenção Preventiva Obrigatória (PMO / NBR 5674)
CREATE TABLE item_preventiva_pmo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    sistema VARCHAR(100) NOT NULL, -- 'ELEVADORES', 'BOMBAS', 'GERADOR', 'SPDA_PARA_RAIOS', 'PORTÕES', 'EXTINTORES'
    descricao VARCHAR(300) NOT NULL,
    periodicidade_dias INTEGER NOT NULL,
    instrucao_tecnica TEXT,
    proxima_inspecao DATE NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT true,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_pmo_proxima_inspecao ON item_preventiva_pmo(condominio_id, proxima_inspecao);

CREATE TABLE registro_inspecao_pmo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    item_preventiva_pmo_id UUID NOT NULL REFERENCES item_preventiva_pmo(id) ON DELETE CASCADE,
    inspecionado_em DATE NOT NULL,
    responsavel_tecnico VARCHAR(200) NOT NULL,
    registro_profissional VARCHAR(50), -- CREA, CFT
    conforme BOOLEAN NOT NULL DEFAULT true,
    parecer_tecnico TEXT,
    chave_art_laudo TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_registro_pmo ON registro_inspecao_pmo(item_preventiva_pmo_id, inspecionado_em DESC);

COMMIT;
