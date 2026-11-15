BEGIN;

-- Contexto: financeiro
-- Toda a operação monetária e tarifação: boletos, Pix dinâmico, despesas, acordos e medições individuais

CREATE TABLE cobranca_condominial (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    competencia DATE NOT NULL,
    vencimento DATE NOT NULL,
    valor NUMERIC(14,2) NOT NULL,
    valor_multa NUMERIC(12,2) DEFAULT 0.00,
    valor_juros NUMERIC(12,2) DEFAULT 0.00,
    valor_desconto NUMERIC(12,2) DEFAULT 0.00,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE', -- 'PENDENTE', 'PAGO', 'VENCIDO', 'CANCELADO', 'EM_ACORDO'
    provedor_pagamento VARCHAR(50),
    identificacao_externa VARCHAR(200),
    linha_digitavel VARCHAR(100),
    codigo_pix TEXT,
    pago_em TIMESTAMPTZ,
    valor_pago NUMERIC(14,2),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (unidade_id, competencia)
);

CREATE INDEX ix_cobranca_condo_status ON cobranca_condominial(condominio_id, status, vencimento);
CREATE INDEX ix_cobranca_unidade ON cobranca_condominial(unidade_id, competencia DESC);

-- Prestação de contas e despesas operacionais do condomínio
CREATE TABLE despesa_condominial (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    categoria VARCHAR(100) NOT NULL,
    fornecedor VARCHAR(200) NOT NULL,
    cnpj_cpf_fornecedor VARCHAR(30),
    descricao TEXT NOT NULL,
    valor NUMERIC(14,2) NOT NULL,
    data_emissao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    chave_comprovante TEXT,
    aprovada_conselho BOOLEAN NOT NULL DEFAULT false,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE', -- 'PENDENTE', 'PAGO', 'CANCELADO'
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_despesa_condo ON despesa_condominial(condominio_id, data_vencimento);

-- Termos de renegociação e confissão de dívida
CREATE TABLE termo_acordo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    devedor_id UUID NOT NULL REFERENCES pessoa(id),
    valor_total_original NUMERIC(14,2) NOT NULL,
    valor_total_negociado NUMERIC(14,2) NOT NULL,
    numero_parcelas INTEGER NOT NULL,
    dia_vencimento_parcelas INTEGER NOT NULL DEFAULT 10,
    status VARCHAR(30) NOT NULL DEFAULT 'ATIVO', -- 'ATIVO', 'QUITADO', 'INADIMPLIDO', 'CANCELADO'
    observacao TEXT,
    assinado_em TIMESTAMPTZ,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_termo_acordo_unidade ON termo_acordo(unidade_id, status);

-- Individualização de consumo (água, gás, energia)
CREATE TABLE medicao_individual (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    tipo_consumo VARCHAR(30) NOT NULL, -- 'AGUA_FRIA', 'AGUA_QUENTE', 'GAS', 'ENERGIA'
    competencia DATE NOT NULL,
    leitura_anterior NUMERIC(12,3) NOT NULL,
    leitura_atual NUMERIC(12,3) NOT NULL,
    consumo NUMERIC(12,3) NOT NULL,
    valor_calculado NUMERIC(12,2) NOT NULL,
    foto_medidor_url TEXT,
    lancado_por UUID REFERENCES pessoa(id),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (unidade_id, tipo_consumo, competencia)
);

CREATE INDEX ix_medicao_consumo ON medicao_individual(condominio_id, tipo_consumo, competencia);

COMMIT;
