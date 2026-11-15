BEGIN;

-- Contexto: comunicacao
-- Canais de relacionamento institucional e social, murais, enquetes, canal fale conosco e ocorrencias unificadas

CREATE TABLE comunicado (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    titulo VARCHAR(200) NOT NULL,
    conteudo TEXT NOT NULL,
    autor_id UUID NOT NULL REFERENCES pessoa(id),
    urgente BOOLEAN NOT NULL DEFAULT false,
    fixado BOOLEAN NOT NULL DEFAULT false,
    publicado_em TIMESTAMPTZ,
    expira_em TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL DEFAULT 'RASCUNHO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_comunicado_condominio ON comunicado(condominio_id, status, publicado_em DESC);

CREATE TABLE leitura_comunicado (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    comunicado_id UUID NOT NULL REFERENCES comunicado(id) ON DELETE CASCADE,
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    lido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (comunicado_id, pessoa_id)
);

-- Ocorrências Unificadas: Portaria, Morador e Gestão (ADR-013)
CREATE TABLE ocorrencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID REFERENCES unidade(id),
    registrada_por UUID NOT NULL REFERENCES pessoa(id),
    origem VARCHAR(20) NOT NULL DEFAULT 'MORADOR', -- 'MORADOR', 'PORTARIA', 'GESTAO'
    categoria VARCHAR(100),
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    prioridade VARCHAR(30) DEFAULT 'NORMAL',
    status VARCHAR(30) NOT NULL DEFAULT 'ABERTA',
    sigilosa BOOLEAN NOT NULL DEFAULT false,
    responsavel_id UUID REFERENCES pessoa(id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolvida_em TIMESTAMPTZ
);

CREATE INDEX ix_ocorrencia_condominio ON ocorrencia(condominio_id, status, criada_em DESC);

CREATE TABLE historico_ocorrencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ocorrencia_id UUID NOT NULL REFERENCES ocorrencia(id) ON DELETE CASCADE,
    autor_id UUID NOT NULL REFERENCES pessoa(id),
    mensagem TEXT NOT NULL,
    tipo VARCHAR(30) DEFAULT 'COMENTARIO', -- 'COMENTARIO', 'MUDANCA_STATUS', 'PARECER'
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_historico_ocorrencia ON historico_ocorrencia(ocorrencia_id);

-- Enquetes da comunidade
CREATE TABLE enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ NOT NULL,
    anonima BOOLEAN NOT NULL DEFAULT false,
    status VARCHAR(30) NOT NULL DEFAULT 'RASCUNHO',
    criada_por UUID REFERENCES pessoa(id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE opcao_enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enquete_id UUID NOT NULL REFERENCES enquete(id) ON DELETE CASCADE,
    descricao VARCHAR(300) NOT NULL,
    ordem INTEGER NOT NULL
);

CREATE TABLE voto_enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enquete_id UUID NOT NULL REFERENCES enquete(id) ON DELETE CASCADE,
    opcao_id UUID NOT NULL REFERENCES opcao_enquete(id) ON DELETE CASCADE,
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    votado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (enquete_id, pessoa_id)
);

-- Mural Social e Classificados entre condôminos
CREATE TABLE item_comunidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    autor_id UUID NOT NULL REFERENCES pessoa(id),
    tipo VARCHAR(30) NOT NULL DEFAULT 'CLASSIFICADO', -- 'CLASSIFICADO', 'AVISO', 'RECOMENDACAO'
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    preco NUMERIC(12,2),
    contato VARCHAR(100),
    foto_url TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    expira_em TIMESTAMPTZ
);

CREATE INDEX ix_item_comunidade ON item_comunidade(condominio_id, status);

-- Canal direto morador ↔ administração (Fale Conosco)
CREATE TABLE mensagem_fale_conosco (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    remetente_id UUID NOT NULL REFERENCES pessoa(id),
    destinatario_id UUID REFERENCES pessoa(id),
    assunto VARCHAR(200) NOT NULL,
    mensagem TEXT NOT NULL,
    lida_em TIMESTAMPTZ,
    enviada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_fale_conosco_condo ON mensagem_fale_conosco(condominio_id, enviada_em DESC);

COMMIT;
