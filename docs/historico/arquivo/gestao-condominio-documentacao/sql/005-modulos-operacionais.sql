BEGIN;

CREATE TABLE encomenda (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    destinatario_id UUID REFERENCES pessoa(id),
    transportadora VARCHAR(150),
    codigo_rastreio VARCHAR(100),
    descricao VARCHAR(500),
    local_armazenamento VARCHAR(100),
    recebida_em TIMESTAMPTZ,
    recebida_por UUID REFERENCES pessoa(id),
    retirada_em TIMESTAMPTZ,
    retirada_por UUID REFERENCES pessoa(id),
    status VARCHAR(50) NOT NULL DEFAULT 'RECEBIDA',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE evento_encomenda (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encomenda_id UUID NOT NULL REFERENCES encomenda(id),
    tipo_evento VARCHAR(50) NOT NULL,
    pessoa_id UUID REFERENCES pessoa(id),
    ocorrido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    observacao TEXT,
    dados JSONB
);

CREATE TABLE reserva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    area_comum_id UUID NOT NULL REFERENCES area_comum(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    solicitante_id UUID NOT NULL REFERENCES pessoa(id),
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ NOT NULL,
    valor NUMERIC(12,2),
    status VARCHAR(50) NOT NULL DEFAULT 'SOLICITADA',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (fim_em > inicio_em)
);

CREATE INDEX ix_reserva_area_periodo
ON reserva(area_comum_id, inicio_em, fim_em);

CREATE TABLE conversa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    assunto VARCHAR(200),
    aberta_por UUID NOT NULL REFERENCES pessoa(id),
    responsavel_id UUID REFERENCES pessoa(id),
    status VARCHAR(30) NOT NULL DEFAULT 'ABERTA',
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    encerrada_em TIMESTAMPTZ
);

CREATE TABLE mensagem_conversa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID NOT NULL REFERENCES conversa(id),
    remetente_id UUID NOT NULL REFERENCES pessoa(id),
    mensagem TEXT NOT NULL,
    enviada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    lida_em TIMESTAMPTZ
);

CREATE TABLE ocorrencia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID REFERENCES unidade(id),
    registrada_por UUID NOT NULL REFERENCES pessoa(id),
    categoria VARCHAR(100),
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    prioridade VARCHAR(30) DEFAULT 'NORMAL',
    status VARCHAR(30) NOT NULL DEFAULT 'ABERTA',
    responsavel_id UUID REFERENCES pessoa(id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolvida_em TIMESTAMPTZ
);

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

CREATE TABLE comunicado (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    titulo VARCHAR(200) NOT NULL,
    conteudo TEXT NOT NULL,
    autor_id UUID NOT NULL REFERENCES pessoa(id),
    publicado_em TIMESTAMPTZ,
    expira_em TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL DEFAULT 'RASCUNHO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

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
    enquete_id UUID NOT NULL REFERENCES enquete(id),
    descricao VARCHAR(300) NOT NULL,
    ordem INTEGER NOT NULL
);

CREATE TABLE voto_enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enquete_id UUID NOT NULL REFERENCES enquete(id),
    opcao_id UUID NOT NULL REFERENCES opcao_enquete(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    votado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (enquete_id, pessoa_id)
);

CREATE TABLE assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    titulo VARCHAR(200) NOT NULL,
    tipo VARCHAR(50),
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL DEFAULT 'AGENDADA',
    zoom_reuniao_id VARCHAR(200),
    regra_quorum JSONB,
    criada_por UUID REFERENCES pessoa(id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE pauta_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id),
    titulo VARCHAR(300) NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL
);

CREATE TABLE participante_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assembleia_id UUID NOT NULL REFERENCES assembleia(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID REFERENCES unidade(id),
    entrou_em TIMESTAMPTZ,
    saiu_em TIMESTAMPTZ,
    presente BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE votacao_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pauta_id UUID NOT NULL REFERENCES pauta_assembleia(id),
    inicio_em TIMESTAMPTZ,
    fim_em TIMESTAMPTZ,
    quorum_necessario NUMERIC(8,4),
    status VARCHAR(30) NOT NULL DEFAULT 'AGUARDANDO'
);

CREATE TABLE opcao_votacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    votacao_id UUID NOT NULL REFERENCES votacao_assembleia(id),
    descricao VARCHAR(200) NOT NULL
);

CREATE TABLE voto_assembleia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    votacao_id UUID NOT NULL REFERENCES votacao_assembleia(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    unidade_id UUID REFERENCES unidade(id),
    opcao_id UUID NOT NULL REFERENCES opcao_votacao(id),
    peso NUMERIC(12,4) NOT NULL DEFAULT 1,
    votado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    hash_auditoria VARCHAR(128),
    UNIQUE (votacao_id, pessoa_id)
);

CREATE TABLE cobranca_condominial (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    competencia DATE NOT NULL,
    vencimento DATE NOT NULL,
    valor NUMERIC(14,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',
    provedor_pagamento VARCHAR(50),
    identificacao_externa VARCHAR(200),
    pago_em TIMESTAMPTZ,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (unidade_id, competencia)
);

CREATE TABLE evento_auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID REFERENCES condominio(id),
    usuario_id UUID,
    pessoa_id UUID REFERENCES pessoa(id),
    acao VARCHAR(100) NOT NULL,
    entidade VARCHAR(100) NOT NULL,
    entidade_id UUID,
    ocorrido_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    endereco_ip INET,
    agente_usuario TEXT,
    id_correlacao VARCHAR(100),
    dados_anteriores JSONB,
    dados_posteriores JSONB
);

CREATE INDEX ix_auditoria_condominio_data
ON evento_auditoria(condominio_id, ocorrido_em DESC);

COMMIT;
