BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

DO $$ BEGIN
    CREATE TYPE status_registro AS ENUM ('ATIVO','INATIVO','EXCLUIDO');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_cadastro AS ENUM (
        'RASCUNHO','ENVIADA','EM_ANALISE','PENDENTE_CORRECAO',
        'APROVADA','REJEITADA','CANCELADA','EXPIRADA'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE tipo_vinculo_unidade AS ENUM (
        'PROPRIETARIO','INQUILINO','MORADOR','DEPENDENTE',
        'COMODATARIO','OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_convite AS ENUM (
        'ATIVO','UTILIZADO','EXPIRADO','CANCELADO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE tipo_documento_cadastro AS ENUM (
        'DOCUMENTO_IDENTIFICACAO_FRENTE',
        'DOCUMENTO_IDENTIFICACAO_VERSO',
        'CPF',
        'COMPROVANTE_PROPRIEDADE',
        'CONTRATO_LOCACAO',
        'AUTORIZACAO_PROPRIETARIO',
        'COMPROVANTE_VINCULO',
        'OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE tipo_documento_identificacao AS ENUM (
        'RG','CIN','CNH','PASSAPORTE','OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_validacao_documento AS ENUM (
        'PENDENTE','APROVADO','REPROVADO','INCONCLUSIVO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE resultado_verificacao_facial AS ENUM (
        'PENDENTE','APROVADA','REPROVADA','INCONCLUSIVA','ERRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE tipo_pessoa_condominio AS ENUM (
        'MORADOR','VISITANTE','PRESTADOR','FUNCIONARIO','ADMINISTRADOR'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

COMMIT;
