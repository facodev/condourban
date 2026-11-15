BEGIN;

CREATE TABLE pessoa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inquilino_id UUID NOT NULL REFERENCES inquilino(id),
    nome_completo VARCHAR(200) NOT NULL,
    nome_social VARCHAR(200),
    cpf_hash VARCHAR(64),
    cpf_criptografado TEXT,
    data_nascimento DATE,
    sexo VARCHAR(30),
    email CITEXT,
    celular VARCHAR(30),
    foto_url TEXT,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    excluido_em TIMESTAMPTZ
);

CREATE INDEX ix_pessoa_cpf_hash ON pessoa(cpf_hash);
CREATE INDEX ix_pessoa_nome ON pessoa(nome_completo);
CREATE INDEX ix_pessoa_email ON pessoa(email);

CREATE TABLE usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pessoa_id UUID REFERENCES pessoa(id),
    chave_usuario_keycloak VARCHAR(200) NOT NULL UNIQUE,
    email CITEXT,
    ultimo_acesso_em TIMESTAMPTZ,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE membro_condominio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    tipo_pessoa tipo_pessoa_condominio NOT NULL,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    entrou_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    saiu_em TIMESTAMPTZ,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, pessoa_id)
);

CREATE TABLE ocupacao_unidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    tipo_vinculo tipo_vinculo_unidade NOT NULL,
    principal BOOLEAN NOT NULL DEFAULT false,
    inicio_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    fim_em TIMESTAMPTZ,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_ocupacao_unidade ON ocupacao_unidade(unidade_id);
CREATE INDEX ix_ocupacao_pessoa ON ocupacao_unidade(pessoa_id);

CREATE TABLE documento_identificacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pessoa_id UUID NOT NULL REFERENCES pessoa(id),
    tipo tipo_documento_identificacao NOT NULL,
    numero VARCHAR(50),
    orgao_emissor VARCHAR(50),
    uf CHAR(2),
    data_emissao DATE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE convite_cadastro_morador (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    tipo_vinculo tipo_vinculo_unidade NOT NULL,
    codigo VARCHAR(20),
    token_hash VARCHAR(128) NOT NULL,
    criado_por UUID REFERENCES pessoa(id),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    validade_em TIMESTAMPTZ NOT NULL,
    usado_em TIMESTAMPTZ,
    status status_convite NOT NULL DEFAULT 'ATIVO'
);

CREATE UNIQUE INDEX ux_convite_codigo ON convite_cadastro_morador(codigo) WHERE codigo IS NOT NULL;
CREATE INDEX ix_convite_token ON convite_cadastro_morador(token_hash);

CREATE TABLE solicitacao_cadastro_morador (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    convite_id UUID REFERENCES convite_cadastro_morador(id),
    pessoa_id UUID REFERENCES pessoa(id),
    tipo_vinculo tipo_vinculo_unidade NOT NULL,
    status status_cadastro NOT NULL DEFAULT 'RASCUNHO',
    etapa_atual VARCHAR(50),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    enviada_em TIMESTAMPTZ,
    analisada_em TIMESTAMPTZ,
    analisada_por UUID REFERENCES pessoa(id),
    motivo_rejeicao TEXT,
    observacao_administrador TEXT,
    criado_por UUID REFERENCES pessoa(id),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_solicitacao_status ON solicitacao_cadastro_morador(condominio_id, status);

CREATE TABLE documento_cadastro (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    solicitacao_cadastro_id UUID NOT NULL REFERENCES solicitacao_cadastro_morador(id),
    tipo_documento tipo_documento_cadastro NOT NULL,
    nome_original VARCHAR(255),
    chave_armazenamento TEXT NOT NULL,
    tipo_mime VARCHAR(100),
    tamanho_bytes BIGINT,
    hash_arquivo VARCHAR(128),
    status_validacao status_validacao_documento NOT NULL DEFAULT 'PENDENTE',
    observacao TEXT,
    enviado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    validado_em TIMESTAMPTZ,
    validado_por UUID REFERENCES pessoa(id)
);

CREATE TABLE verificacao_facial (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    pessoa_id UUID REFERENCES pessoa(id),
    solicitacao_cadastro_id UUID REFERENCES solicitacao_cadastro_morador(id),
    provedor VARCHAR(50) NOT NULL,
    referencia_externa VARCHAR(200),
    tipo_verificacao VARCHAR(50) NOT NULL,
    resultado resultado_verificacao_facial NOT NULL DEFAULT 'PENDENTE',
    pontuacao NUMERIC(8,5),
    prova_de_vida BOOLEAN,
    consentimento_em TIMESTAMPTZ,
    iniciada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    concluida_em TIMESTAMPTZ,
    dados_provedor JSONB,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE historico_analise_cadastro (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    solicitacao_cadastro_id UUID NOT NULL REFERENCES solicitacao_cadastro_morador(id),
    administrador_id UUID NOT NULL REFERENCES pessoa(id),
    acao VARCHAR(50) NOT NULL,
    motivo VARCHAR(100),
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE motivo_correcao_cadastro (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(50) NOT NULL UNIQUE,
    descricao VARCHAR(200) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT true
);

COMMIT;
