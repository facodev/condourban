BEGIN;

-- Contexto: portaria
-- Operação da guarita humana ou remota: visitantes, prestadores, encomendas, mudanças e achados/perdidos

CREATE TABLE visitante (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID REFERENCES unidade(id),
    responsavel_id UUID REFERENCES pessoa(id),
    observacao TEXT,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_visitante_condominio ON visitante(condominio_id, pessoa_id);

CREATE TABLE convite_visitante (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    visitante_id UUID NOT NULL REFERENCES visitante(id),
    criado_por UUID NOT NULL REFERENCES pessoa(id),
    inicio_validade TIMESTAMPTZ NOT NULL,
    fim_validade TIMESTAMPTZ NOT NULL,
    quantidade_maxima_entradas INTEGER DEFAULT 1,
    codigo VARCHAR(50),
    token_hash VARCHAR(128),
    status status_convite NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    cancelado_em TIMESTAMPTZ,
    CHECK (fim_validade > inicio_validade)
);

CREATE INDEX ix_convite_visitante_validade
ON convite_visitante(condominio_id, inicio_validade, fim_validade);

CREATE TABLE prestador (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    empresa VARCHAR(200),
    documento_empresa VARCHAR(30),
    atividade VARCHAR(200),
    observacao TEXT,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE autorizacao_prestador (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    prestador_id UUID NOT NULL REFERENCES prestador(id),
    unidade_id UUID REFERENCES unidade(id),
    inicio_validade TIMESTAMPTZ NOT NULL,
    fim_validade TIMESTAMPTZ,
    horario_inicio TIME,
    horario_fim TIME,
    dias_semana INTEGER[],
    criado_por UUID REFERENCES pessoa(id),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE registro_visita (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    visitante_id UUID REFERENCES visitante(id),
    prestador_id UUID REFERENCES prestador(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    atendido_por UUID REFERENCES pessoa(id),
    entrada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    saida_em TIMESTAMPTZ,
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_registro_visita_condo ON registro_visita(condominio_id, entrada_em DESC);

-- Submódulo: encomendas
CREATE TABLE encomenda (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    destinatario_id UUID REFERENCES pessoa(id),
    transportadora VARCHAR(150),
    codigo_rastreio VARCHAR(100),
    descricao VARCHAR(500),
    local_armazenamento VARCHAR(100),
    foto_url TEXT,
    codigo_retirada VARCHAR(20),
    recebida_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    recebida_por UUID REFERENCES pessoa(id),
    retirada_em TIMESTAMPTZ,
    retirada_por UUID REFERENCES pessoa(id),
    status VARCHAR(50) NOT NULL DEFAULT 'RECEBIDA',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_encomenda_unidade ON encomenda(condominio_id, unidade_id, status);

CREATE TABLE evento_encomenda (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encomenda_id UUID NOT NULL REFERENCES encomenda(id),
    tipo_evento VARCHAR(50) NOT NULL,
    pessoa_id UUID REFERENCES pessoa(id),
    ocorrido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    observacao TEXT,
    dados JSONB
);

-- Mudanças residenciais e agendamento de elevador
CREATE TABLE agendamento_mudanca (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    solicitante_id UUID NOT NULL REFERENCES pessoa(id),
    tipo_mudanca tipo_mudanca NOT NULL,
    data_hora_inicio TIMESTAMPTZ NOT NULL,
    data_hora_fim TIMESTAMPTZ NOT NULL,
    reserva_elevador BOOLEAN NOT NULL DEFAULT true,
    status status_mudanca NOT NULL DEFAULT 'SOLICITADA',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (data_hora_fim > data_hora_inicio)
);

CREATE INDEX ix_mudanca_periodo ON agendamento_mudanca(condominio_id, data_hora_inicio, data_hora_fim);

-- Achados e perdidos na portaria
CREATE TABLE item_perdido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    descricao VARCHAR(255) NOT NULL,
    categoria VARCHAR(50),
    local_encontrado VARCHAR(100),
    encontrado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    encontrado_por UUID REFERENCES pessoa(id),
    foto_url TEXT,
    status status_item_perdido NOT NULL DEFAULT 'CUSTODIA',
    restituido_para UUID REFERENCES pessoa(id),
    restituido_em TIMESTAMPTZ,
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_item_perdido_condo ON item_perdido(condominio_id, status);

COMMIT;
