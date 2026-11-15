BEGIN;

-- Contexto: identidade_cadastro
-- Indivíduos, contas de acesso, perfis de membresia, ocupações, onboarding, veículos e animais domésticos

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
    email CITEXT NOT NULL UNIQUE,
    senha_hash VARCHAR(255),
    google_sub VARCHAR(255) UNIQUE,
    email_verificado BOOLEAN NOT NULL DEFAULT false,
    ultimo_acesso_em TIMESTAMPTZ,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_usuario_tem_fator_auth CHECK (
        senha_hash IS NOT NULL OR google_sub IS NOT NULL
    )
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
    responsavel_ocupacao_id UUID REFERENCES ocupacao_unidade(id),
    tipo_vinculo tipo_vinculo_unidade NOT NULL,
    mora_no_local BOOLEAN NOT NULL DEFAULT true,
    principal BOOLEAN NOT NULL DEFAULT false,
    inicio_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    fim_em TIMESTAMPTZ,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_ocupacao_curto_prazo_datas CHECK (
        tipo_vinculo NOT IN ('TEMPORARIO', 'HOSPEDE')
        OR (inicio_em IS NOT NULL AND fim_em IS NOT NULL)
    ),
    CONSTRAINT ck_ocupacao_fim_maior_inicio CHECK (
        fim_em IS NULL OR fim_em > inicio_em
    )
);

CREATE INDEX ix_ocupacao_unidade ON ocupacao_unidade(unidade_id);
CREATE INDEX ix_ocupacao_pessoa ON ocupacao_unidade(pessoa_id);
CREATE INDEX ix_ocupacao_responsavel ON ocupacao_unidade(responsavel_ocupacao_id);

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

-- Submódulo: veiculos_pets
CREATE TABLE veiculo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    proprietario_id UUID REFERENCES pessoa(id),
    vaga_garagem_id UUID REFERENCES vaga_garagem(id),
    placa VARCHAR(10) NOT NULL,
    tipo tipo_veiculo NOT NULL DEFAULT 'CARRO',
    marca VARCHAR(50),
    modelo VARCHAR(50),
    cor VARCHAR(30),
    status status_registro NOT NULL DEFAULT 'ATIVO',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (condominio_id, placa)
);

CREATE INDEX ix_veiculo_unidade ON veiculo(unidade_id);
CREATE INDEX ix_veiculo_placa ON veiculo(placa);

CREATE TABLE pet (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    tutor_id UUID REFERENCES pessoa(id),
    nome VARCHAR(100) NOT NULL,
    especie especie_pet NOT NULL DEFAULT 'CANINO',
    raca VARCHAR(100),
    porte porte_pet NOT NULL DEFAULT 'MEDIO',
    cor VARCHAR(50),
    foto_url TEXT,
    vacinado BOOLEAN NOT NULL DEFAULT true,
    status status_registro NOT NULL DEFAULT 'ATIVO',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_pet_unidade ON pet(unidade_id);

-- ============================================================================
-- Triggers e Regras de Negócio de Ocupação da Unidade (PostgreSQL)
-- ============================================================================

CREATE OR REPLACE FUNCTION tg_fn_validar_regras_ocupacao()
RETURNS TRIGGER AS $$
BEGIN
    -- Regra 1: Conflito de Posse Direta
    -- Se proprietário tentar residir no local enquanto há inquilino ativo
    IF NEW.status = 'ATIVO' AND NEW.tipo_vinculo = 'PROPRIETARIO' AND NEW.mora_no_local = TRUE THEN
        IF EXISTS (
            SELECT 1 FROM ocupacao_unidade
            WHERE unidade_id = NEW.unidade_id
              AND tipo_vinculo = 'INQUILINO'
              AND status = 'ATIVO'
              AND id <> COALESCE(NEW.id, '00000000-0000-0000-0000-000000000000'::uuid)
              AND (fim_em IS NULL OR fim_em > now())
        ) THEN
            RAISE EXCEPTION 'CONFLITO_POSSE_DIRETA: Unidade possui inquilino ativo; proprietário não pode residir no local.'
            USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    -- Se inquilino for ativado, desmarca automaticamente mora_no_local do proprietário
    IF NEW.status = 'ATIVO' AND NEW.tipo_vinculo = 'INQUILINO' THEN
        UPDATE ocupacao_unidade
        SET mora_no_local = FALSE, atualizado_em = now()
        WHERE unidade_id = NEW.unidade_id
          AND tipo_vinculo = 'PROPRIETARIO'
          AND mora_no_local = TRUE
          AND status = 'ATIVO'
          AND id <> COALESCE(NEW.id, '00000000-0000-0000-0000-000000000000'::uuid);
    END IF;

    -- Regra 5: Dependentes exigem responsável residente ativo
    IF NEW.status = 'ATIVO' AND NEW.tipo_vinculo = 'DEPENDENTE' THEN
        IF NOT EXISTS (
            SELECT 1 FROM ocupacao_unidade
            WHERE unidade_id = NEW.unidade_id
              AND tipo_vinculo IN ('PROPRIETARIO', 'INQUILINO')
              AND mora_no_local = TRUE
              AND status = 'ATIVO'
              AND id <> COALESCE(NEW.id, '00000000-0000-0000-0000-000000000000'::uuid)
              AND (fim_em IS NULL OR fim_em > now())
              AND (NEW.responsavel_ocupacao_id IS NULL OR id = NEW.responsavel_ocupacao_id)
        ) THEN
            RAISE EXCEPTION 'DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE: Dependentes exigem proprietário morador ou inquilino ativo residente na mesma unidade.'
            USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_validar_regras_ocupacao
BEFORE INSERT OR UPDATE ON ocupacao_unidade
FOR EACH ROW EXECUTE FUNCTION tg_fn_validar_regras_ocupacao();

-- Regra 4: Rotina Diária de Expiração e Bloqueio Automático de Acesso
CREATE OR REPLACE FUNCTION fn_expirar_ocupacoes_vencidas(p_condominio_id UUID DEFAULT NULL)
RETURNS TABLE (
    ocupacoes_inativadas INTEGER,
    dependentes_inativados INTEGER
) AS $$
DECLARE
    v_total_ocupacoes INTEGER := 0;
    v_total_dependentes INTEGER := 0;
    r_expirado RECORD;
BEGIN
    FOR r_expirado IN
        SELECT id, unidade_id, tipo_vinculo
        FROM ocupacao_unidade
        WHERE status = 'ATIVO'
          AND fim_em IS NOT NULL
          AND fim_em < now()
          AND (p_condominio_id IS NULL OR condominio_id = p_condominio_id)
    LOOP
        -- Inativa vínculo vencido
        UPDATE ocupacao_unidade
        SET status = 'INATIVO', atualizado_em = now()
        WHERE id = r_expirado.id;
        v_total_ocupacoes := v_total_ocupacoes + 1;

        -- Regra 5: Cascade nos dependentes se for titular
        IF r_expirado.tipo_vinculo IN ('INQUILINO', 'PROPRIETARIO') THEN
            UPDATE ocupacao_unidade
            SET status = 'INATIVO', atualizado_em = now()
            WHERE status = 'ATIVO'
              AND (
                  responsavel_ocupacao_id = r_expirado.id
                  OR (
                      unidade_id = r_expirado.unidade_id
                      AND tipo_vinculo = 'DEPENDENTE'
                      AND NOT EXISTS (
                          SELECT 1 FROM ocupacao_unidade outros
                          WHERE outros.unidade_id = r_expirado.unidade_id
                            AND outros.tipo_vinculo IN ('PROPRIETARIO', 'INQUILINO')
                            AND outros.mora_no_local = TRUE
                            AND outros.status = 'ATIVO'
                            AND outros.id <> r_expirado.id
                            AND (outros.fim_em IS NULL OR outros.fim_em > now())
                      )
                  )
              );
            GET DIAGNOSTICS v_total_dependentes = ROW_COUNT;
        END IF;
    END LOOP;

    RETURN QUERY SELECT v_total_ocupacoes, v_total_dependentes;
END;
$$ LANGUAGE plpgsql;

COMMIT;
