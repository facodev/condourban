BEGIN;

CREATE TABLE integracao_provedor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    provedor VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT true,
    configuracao JSONB NOT NULL DEFAULT '{}'::jsonb,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, provedor, nome)
);

CREATE TABLE dispositivo_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    provedor VARCHAR(50) NOT NULL,
    identificacao_externa VARCHAR(200),
    endereco_ip INET,
    localizacao VARCHAR(200),
    sentido VARCHAR(30),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    configuracao JSONB NOT NULL DEFAULT '{}'::jsonb,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, identificacao_externa)
);

CREATE TABLE credencial_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    tipo VARCHAR(30) NOT NULL,
    provedor VARCHAR(50) NOT NULL,
    referencia_externa VARCHAR(200),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    ativada_em TIMESTAMPTZ,
    desativada_em TIMESTAMPTZ,
    dados_provedor JSONB
);

CREATE INDEX ix_credencial_pessoa ON credencial_acesso(condominio_id, pessoa_id);
CREATE UNIQUE INDEX ux_credencial_externa
ON credencial_acesso(condominio_id, provedor, referencia_externa)
WHERE referencia_externa IS NOT NULL;

CREATE TABLE autorizacao_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    credencial_acesso_id UUID REFERENCES credencial_acesso(id),
    unidade_id UUID REFERENCES unidade(id),
    tipo_autorizacao VARCHAR(50) NOT NULL,
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ,
    dias_semana INTEGER[],
    horario_inicio TIME,
    horario_fim TIME,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    motivo VARCHAR(500),
    criado_por UUID REFERENCES pessoa(id),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (fim_em IS NULL OR fim_em > inicio_em),
    CHECK (
        dias_semana IS NULL
        OR NOT EXISTS (
            SELECT 1 FROM unnest(dias_semana) d
            WHERE d < 0 OR d > 6
        )
    )
);

CREATE INDEX ix_autorizacao_pessoa ON autorizacao_acesso(condominio_id, pessoa_id);
CREATE INDEX ix_autorizacao_periodo ON autorizacao_acesso(condominio_id, inicio_em, fim_em);

CREATE TABLE evento_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID REFERENCES pessoa(id),
    credencial_acesso_id UUID REFERENCES credencial_acesso(id),
    dispositivo_acesso_id UUID REFERENCES dispositivo_acesso(id),
    autorizacao_acesso_id UUID REFERENCES autorizacao_acesso(id),
    tipo_evento VARCHAR(50) NOT NULL,
    resultado VARCHAR(50),
    ocorrido_em TIMESTAMPTZ NOT NULL,
    identificacao_externa VARCHAR(200),
    pontuacao_facial NUMERIC(8,5),
    imagem_referencia_url TEXT,
    dados_provedor JSONB,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_evento_acesso_pessoa ON evento_acesso(pessoa_id, ocorrido_em DESC);
CREATE INDEX ix_evento_acesso_condominio ON evento_acesso(condominio_id, ocorrido_em DESC);
CREATE UNIQUE INDEX ux_evento_acesso_externo
ON evento_acesso(condominio_id, identificacao_externa)
WHERE identificacao_externa IS NOT NULL;

CREATE TABLE sincronizacao_acesso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    integracao_provedor_id UUID NOT NULL REFERENCES integracao_provedor(id),
    tipo_operacao VARCHAR(50) NOT NULL,
    entidade VARCHAR(100) NOT NULL,
    entidade_id UUID NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',
    tentativas INTEGER NOT NULL DEFAULT 0,
    ultima_tentativa_em TIMESTAMPTZ,
    concluida_em TIMESTAMPTZ,
    erro TEXT,
    resposta_provedor JSONB,
    idempotencia_chave VARCHAR(200),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_sincronizacao_idempotencia
ON sincronizacao_acesso(condominio_id, idempotencia_chave)
WHERE idempotencia_chave IS NOT NULL;

CREATE INDEX ix_sincronizacao_pendente
ON sincronizacao_acesso(status, criada_em);

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

CREATE TABLE convite_visitante (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    visitante_id UUID NOT NULL REFERENCES visitante(id),
    criado_por UUID NOT NULL REFERENCES pessoa(id),
    inicio_validade TIMESTAMPTZ NOT NULL,
    fim_validade TIMESTAMPTZ NOT NULL,
    quantidade_maxima_entradas INTEGER,
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

COMMIT;
