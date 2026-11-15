BEGIN;

-- Contexto: governanca
-- Gestão deliberativa formal, assembleias virtuais, procurações, atas, quórum e repositório de documentos

CREATE TABLE assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    titulo VARCHAR(200) NOT NULL,
    tipo VARCHAR(50), -- 'ORDINARIA', 'EXTRAORDINARIA'
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL DEFAULT 'AGENDADA', -- 'AGENDADA', 'EM_ANDAMENTO', 'ENCERRADA', 'CANCELADA'
    link_videochamada VARCHAR(500),
    regra_quorum JSONB NOT NULL DEFAULT '{}'::jsonb,
    criada_por UUID REFERENCES pessoa(id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_assembleia_condo ON assembleia(condominio_id, status, inicio_em DESC);

CREATE TABLE pauta_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id) ON DELETE CASCADE,
    titulo VARCHAR(300) NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL
);

CREATE TABLE participante_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id) ON DELETE CASCADE,
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID REFERENCES unidade(id),
    entrou_em TIMESTAMPTZ,
    saiu_em TIMESTAMPTZ,
    presente BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE procuracao_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id) ON DELETE CASCADE,
    outorgante_id UUID NOT NULL REFERENCES pessoa(id),
    outorgado_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    chave_documento TEXT,
    validada_por UUID REFERENCES pessoa(id),
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE', -- 'PENDENTE', 'VALIDADA', 'REJEITADA'
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE votacao_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pauta_id UUID NOT NULL REFERENCES pauta_assembleia(id) ON DELETE CASCADE,
    inicio_em TIMESTAMPTZ,
    fim_em TIMESTAMPTZ,
    quorum_necessario NUMERIC(8,4),
    status VARCHAR(30) NOT NULL DEFAULT 'AGUARDANDO' -- 'AGUARDANDO', 'ABERTA', 'ENCERRADA'
);

CREATE TABLE opcao_votacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    votacao_id UUID NOT NULL REFERENCES votacao_assembleia(id) ON DELETE CASCADE,
    descricao VARCHAR(200) NOT NULL
);

CREATE TABLE voto_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    votacao_id UUID NOT NULL REFERENCES votacao_assembleia(id) ON DELETE CASCADE,
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID REFERENCES unidade(id),
    opcao_id UUID NOT NULL REFERENCES opcao_votacao(id),
    peso NUMERIC(12,4) NOT NULL DEFAULT 1.0,
    votado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    hash_auditoria VARCHAR(128),
    UNIQUE (votacao_id, pessoa_id)
);

CREATE TABLE ata_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id) ON DELETE CASCADE,
    texto_ata TEXT NOT NULL,
    chave_documento_assinado TEXT,
    redigida_por UUID REFERENCES pessoa(id),
    aprovada BOOLEAN NOT NULL DEFAULT false,
    registrada_em TIMESTAMPTZ,
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Repositório regulatório e documental
CREATE TABLE pasta_documento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pasta_pai_id UUID REFERENCES pasta_documento(id),
    nome VARCHAR(200) NOT NULL,
    visibilidade VARCHAR(50) NOT NULL DEFAULT 'ADMINISTRADORES',
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE documento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pasta_id UUID REFERENCES pasta_documento(id),
    nome VARCHAR(255) NOT NULL,
    chave_armazenamento TEXT NOT NULL,
    tipo_mime VARCHAR(100),
    tamanho_bytes BIGINT,
    hash_arquivo VARCHAR(128),
    versao INTEGER NOT NULL DEFAULT 1,
    enviado_por UUID REFERENCES pessoa(id),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    excluido_em TIMESTAMPTZ
);

CREATE INDEX ix_documento_condo ON documento(condominio_id, pasta_id);

COMMIT;
