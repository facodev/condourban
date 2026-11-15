BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

-- Status genérico de registro
DO $$ BEGIN
    CREATE TYPE status_registro AS ENUM ('ATIVO', 'INATIVO', 'EXCLUIDO');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Status do fluxo de cadastro / onboarding
DO $$ BEGIN
    CREATE TYPE status_cadastro AS ENUM (
        'RASCUNHO', 'ENVIADA', 'EM_ANALISE', 'PENDENTE_CORRECAO',
        'APROVADA', 'REJEITADA', 'CANCELADA', 'EXPIRADA'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Tipos de vínculo com a unidade habitacional
DO $$ BEGIN
    CREATE TYPE tipo_vinculo_unidade AS ENUM (
        'PROPRIETARIO', 'INQUILINO', 'MORADOR', 'DEPENDENTE',
        'TEMPORARIO', 'HOSPEDE', 'OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Status de convites em geral
DO $$ BEGIN
    CREATE TYPE status_convite AS ENUM (
        'ATIVO', 'UTILIZADO', 'EXPIRADO', 'CANCELADO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Tipos de documentos aceitos para comprovação de cadastro
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

-- Tipos de documentos civis de identificação
DO $$ BEGIN
    CREATE TYPE tipo_documento_identificacao AS ENUM (
        'RG', 'CIN', 'CNH', 'PASSAPORTE', 'OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Status de validação de documentos
DO $$ BEGIN
    CREATE TYPE status_validacao_documento AS ENUM (
        'PENDENTE', 'APROVADO', 'REPROVADO', 'INCONCLUSIVO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Verificação facial e biometria
DO $$ BEGIN
    CREATE TYPE resultado_verificacao_facial AS ENUM (
        'PENDENTE', 'APROVADA', 'REPROVADA', 'INCONCLUSIVA', 'ERRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Papel/categoria base da pessoa no condomínio
DO $$ BEGIN
    CREATE TYPE tipo_pessoa_condominio AS ENUM (
        'MORADOR', 'VISITANTE', 'PRESTADOR', 'FUNCIONARIO', 'ADMINISTRADOR'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Veículos e animais domésticos (identidade_cadastro)
DO $$ BEGIN
    CREATE TYPE tipo_veiculo AS ENUM (
        'CARRO', 'MOTO', 'UTILITARIO', 'BICICLETA_ELETRICA', 'OUTRO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE porte_pet AS ENUM ('PEQUENO', 'MEDIO', 'GRANDE');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE especie_pet AS ENUM ('CANINO', 'FELINO', 'AVE', 'OUTRO');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Portaria e vistorias
DO $$ BEGIN
    CREATE TYPE tipo_mudanca AS ENUM ('ENTRADA', 'SAIDA');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_mudanca AS ENUM (
        'SOLICITADA', 'CONFIRMADA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_item_perdido AS ENUM (
        'CUSTODIA', 'DEVOLVIDO', 'DOADO', 'DESCARTADO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE tipo_vistoria AS ENUM ('CHECKIN', 'CHECKOUT');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Manutenção e ordens de serviço
DO $$ BEGIN
    CREATE TYPE status_chamado AS ENUM (
        'ABERTO', 'EM_TRIAGEM', 'AGENDADO', 'EM_EXECUCAO', 'CONCLUIDO', 'CANCELADO'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE prioridade_chamado AS ENUM (
        'BAIXA', 'MEDIA', 'ALTA', 'URGENTE'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_ordem_servico AS ENUM (
        'RASCUNHO', 'APROVADA', 'EM_EXECUCAO', 'AGUARDANDO_PECA', 'FINALIZADA', 'CANCELADA'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Casts implícitos para compatibilidade transparente com ORM (SQLAlchemy / asyncpg)
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN 
        SELECT typname FROM pg_type WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public') AND typtype = 'e'
    LOOP
        BEGIN
            EXECUTE format('CREATE CAST (character varying AS %I) WITH INOUT AS IMPLICIT', t);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END;
        BEGIN
            EXECUTE format('CREATE CAST (text AS %I) WITH INOUT AS IMPLICIT', t);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END;
    END LOOP;
END
$$;

COMMIT;
