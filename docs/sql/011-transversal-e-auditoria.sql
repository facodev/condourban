BEGIN;

-- Contexto: transversal
-- Logs estruturados de auditoria de segurança e telemetria de uso da plataforma

CREATE TABLE evento_auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID REFERENCES condominio(id),
    usuario_id UUID,
    pessoa_id UUID REFERENCES pessoa(id),
    acao VARCHAR(100) NOT NULL,
    entidade VARCHAR(100) NOT NULL,
    entidade_id UUID,
    ocorrido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    endereco_ip VARCHAR(50),
    agente_usuario TEXT,
    id_correlacao VARCHAR(100),
    dados_anteriores JSONB,
    dados_posteriores JSONB
);

CREATE INDEX ix_auditoria_condominio_data
ON evento_auditoria(condominio_id, ocorrido_em DESC);

CREATE TABLE evento_uso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID REFERENCES condominio(id),
    usuario_id UUID,
    modulo VARCHAR(50) NOT NULL,
    funcionalidade_codigo VARCHAR(80),
    acao VARCHAR(50) NOT NULL,
    ocorrido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadados JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX ix_evento_uso_condo ON evento_uso(condominio_id, ocorrido_em DESC);

COMMIT;
