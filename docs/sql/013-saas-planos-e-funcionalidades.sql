BEGIN;

-- Domínio SaaS: Planos comerciais + Catálogo de funcionalidades + Overrides por condomínio (ADR-011)

DO $$ BEGIN
    CREATE TYPE escopo_funcionalidade AS ENUM ('NUCLEO', 'OPCIONAL');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_assinatura AS ENUM (
        'TRIAL', 'ATIVA', 'SUSPENSA', 'CANCELADA', 'ENCERRADA'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Catálogo de módulos/features da plataforma
CREATE TABLE funcionalidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(80) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    escopo escopo_funcionalidade NOT NULL DEFAULT 'OPCIONAL',
    -- Se true, síndico/admin do condo pode desligar mesmo estando no plano (uso operacional)
    permitir_desligar_no_condo BOOLEAN NOT NULL DEFAULT true,
    ordem INTEGER NOT NULL DEFAULT 0,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_funcionalidade_nucleo_nao_desliga
        CHECK (escopo <> 'NUCLEO' OR permitir_desligar_no_condo = false)
);

-- Planos comerciais (tiers SaaS)
CREATE TABLE plano (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(80) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    max_unidades INTEGER,
    preco_mensal_centavos INTEGER,
    preco_exibicao VARCHAR(80),
    publico BOOLEAN NOT NULL DEFAULT true,
    ordem INTEGER NOT NULL DEFAULT 0,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE plano_funcionalidade (
    plano_id UUID NOT NULL REFERENCES plano(id) ON DELETE CASCADE,
    funcionalidade_id UUID NOT NULL REFERENCES funcionalidade(id) ON DELETE CASCADE,
    incluido BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY (plano_id, funcionalidade_id)
);

-- Assinatura / vínculo comercial do condomínio a um plano
CREATE TABLE assinatura (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    plano_id UUID NOT NULL REFERENCES plano(id),
    status status_assinatura NOT NULL DEFAULT 'ATIVA',
    inicia_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    termina_em TIMESTAMPTZ,
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_assinatura_ativa_por_condo
    ON assinatura (condominio_id)
    WHERE status IN ('TRIAL', 'ATIVA');

CREATE INDEX ix_assinatura_plano ON assinatura (plano_id);
CREATE INDEX ix_assinatura_condominio ON assinatura (condominio_id);

-- Override por condomínio (liga/desliga além ou aquém do plano)
CREATE TABLE condominio_funcionalidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    funcionalidade_id UUID NOT NULL REFERENCES funcionalidade(id),
    habilitada BOOLEAN NOT NULL,
    origem VARCHAR(40) NOT NULL DEFAULT 'OPERACIONAL',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, funcionalidade_id)
);

CREATE INDEX ix_condo_func_condo ON condominio_funcionalidade (condominio_id);

-- Resolução efetiva: NÚCLEO → sempre on; senão override do condo; senão inclusão no plano ativo/trial
CREATE OR REPLACE FUNCTION funcionalidade_habilitada(
    p_condominio_id UUID,
    p_codigo VARCHAR
) RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    WITH f AS (
        SELECT id, escopo
        FROM funcionalidade
        WHERE codigo = p_codigo
          AND status = 'ATIVO'
        LIMIT 1
    ),
    ov AS (
        SELECT cf.habilitada
        FROM condominio_funcionalidade cf
        JOIN f ON f.id = cf.funcionalidade_id
        WHERE cf.condominio_id = p_condominio_id
        LIMIT 1
    ),
    pl AS (
        SELECT COALESCE(pf.incluido, false) AS incluido
        FROM assinatura a
        JOIN f ON true
        LEFT JOIN plano_funcionalidade pf
            ON pf.plano_id = a.plano_id
           AND pf.funcionalidade_id = f.id
        WHERE a.condominio_id = p_condominio_id
          AND a.status IN ('TRIAL', 'ATIVA')
          AND (a.termina_em IS NULL OR a.termina_em > now())
        ORDER BY a.inicia_em DESC
        LIMIT 1
    )
    SELECT CASE
        WHEN NOT EXISTS (SELECT 1 FROM f) THEN false
        WHEN (SELECT escopo FROM f) = 'NUCLEO' THEN true
        WHEN EXISTS (SELECT 1 FROM ov) THEN (SELECT habilitada FROM ov)
        WHEN EXISTS (SELECT 1 FROM pl) THEN (SELECT incluido FROM pl)
        ELSE false
    END;
$$;

-- RLS das tabelas vinculadas a condomínio
ALTER TABLE assinatura ENABLE ROW LEVEL SECURITY;
ALTER TABLE condominio_funcionalidade ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS isolamento_condominio ON assinatura;
CREATE POLICY isolamento_condominio ON assinatura
    USING (condominio_id = obter_condominio_sessao())
    WITH CHECK (condominio_id = obter_condominio_sessao());

DROP POLICY IF EXISTS isolamento_condominio ON condominio_funcionalidade;
CREATE POLICY isolamento_condominio ON condominio_funcionalidade
    USING (condominio_id = obter_condominio_sessao())
    WITH CHECK (condominio_id = obter_condominio_sessao());

COMMIT;
