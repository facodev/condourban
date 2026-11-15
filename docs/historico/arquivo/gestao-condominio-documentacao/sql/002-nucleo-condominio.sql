BEGIN;

CREATE TABLE inquilino (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(200) NOT NULL,
    nome_fantasia VARCHAR(200),
    documento VARCHAR(30),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE condominio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inquilino_id UUID NOT NULL REFERENCES inquilino(id),
    razao_social VARCHAR(200),
    nome VARCHAR(200) NOT NULL,
    cnpj VARCHAR(18),
    cep VARCHAR(9),
    logradouro VARCHAR(200),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    fuso_horario VARCHAR(50) NOT NULL DEFAULT 'America/Sao_Paulo',
    configuracoes JSONB NOT NULL DEFAULT '{}'::jsonb,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_condominio_cnpj ON condominio(cnpj) WHERE cnpj IS NOT NULL;

CREATE TABLE bloco (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(500),
    ordem INTEGER,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, nome)
);

CREATE TABLE unidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    bloco_id UUID REFERENCES bloco(id),
    identificacao VARCHAR(50) NOT NULL,
    andar INTEGER,
    tipo VARCHAR(50),
    descricao VARCHAR(500),
    area_privativa NUMERIC(12,2),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, identificacao)
);

CREATE INDEX ix_unidade_bloco ON unidade(bloco_id);

CREATE TABLE vaga_garagem (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID REFERENCES unidade(id),
    identificacao VARCHAR(50) NOT NULL,
    tipo VARCHAR(50),
    coberta BOOLEAN NOT NULL DEFAULT false,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, identificacao)
);

CREATE TABLE area_comum (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    capacidade INTEGER,
    valor_reserva NUMERIC(12,2),
    regras TEXT,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;
