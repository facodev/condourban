BEGIN;

-- ==============================================================================
-- 015-rls-completo-e-roles.sql
-- Reforço definitivo do Row Level Security (RLS) e criação da Role de Aplicação
-- ==============================================================================

-- 1. Criação do papel de aplicação condourban_app (sem SUPERUSER / sem BYPASSRLS)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'condourban_app') THEN
        CREATE ROLE condourban_app WITH LOGIN PASSWORD 'condourban_pass' NOSUPERUSER NOBYPASSRLS;
    END IF;
END $$;

-- Concessão de permissões operacionais
GRANT CONNECT ON DATABASE condourban TO condourban_app;
GRANT USAGE ON SCHEMA public TO condourban_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO condourban_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO condourban_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO condourban_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO condourban_app;

-- 2. Garantir FORCE ROW LEVEL SECURITY em todas as 52 tabelas operacionais já cobertas
DO $$
DECLARE
    tabela TEXT;
BEGIN
    FOREACH tabela IN ARRAY ARRAY[
        'bloco', 'unidade', 'vaga_garagem', 'area_comum',
        'membro_condominio', 'ocupacao_unidade', 'convite_cadastro_morador',
        'solicitacao_cadastro_morador', 'documento_cadastro', 'verificacao_facial',
        'veiculo', 'pet', 'integracao_provedor', 'dispositivo_acesso',
        'credencial_acesso', 'autorizacao_acesso', 'evento_acesso', 'sincronizacao_acesso',
        'visitante', 'convite_visitante', 'prestador', 'autorizacao_prestador',
        'registro_visita', 'encomenda', 'agendamento_mudanca', 'item_perdido',
        'reserva', 'convidado_reserva', 'vistoria_reserva', 'comunicado',
        'leitura_comunicado', 'ocorrencia', 'enquete', 'item_comunidade',
        'mensagem_fale_conosco', 'assembleia', 'procuracao_assembleia', 'ata_assembleia',
        'pasta_documento', 'documento', 'cobranca_condominial', 'despesa_condominial',
        'termo_acordo', 'medicao_individual', 'chamado_manutencao', 'ordem_servico',
        'item_preventiva_pmo', 'registro_inspecao_pmo', 'evento_auditoria', 'evento_uso'
    ]
    LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', tabela);
        EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', tabela);
    END LOOP;
END $$;

-- 3. RLS para Pessoa (Entidade Civil Global compartilhada entre condomínios)
-- Visível se:
--   a) app.condominio_id for nulo (operações globais de sistema/auth)
--   b) bypass ativo (app.bypass_rls = 'on')
--   c) a pessoa for membro ativo deste condomínio OU tiver ocupação de unidade nele
ALTER TABLE pessoa ENABLE ROW LEVEL SECURITY;
ALTER TABLE pessoa FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS isolamento_pessoa ON pessoa;
CREATE POLICY isolamento_pessoa ON pessoa
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = pessoa.id
              AND m.condominio_id = obter_condominio_sessao()
        )
        OR EXISTS (
            SELECT 1 FROM ocupacao_unidade o
            WHERE o.pessoa_id = pessoa.id
              AND o.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = pessoa.id
              AND m.condominio_id = obter_condominio_sessao()
        )
    );

-- 4. RLS para Documento de Identificação (Filho de Pessoa)
ALTER TABLE documento_identificacao ENABLE ROW LEVEL SECURITY;
ALTER TABLE documento_identificacao FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS isolamento_documento_identificacao ON documento_identificacao;
CREATE POLICY isolamento_documento_identificacao ON documento_identificacao
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = documento_identificacao.pessoa_id
              AND m.condominio_id = obter_condominio_sessao()
        )
        OR EXISTS (
            SELECT 1 FROM ocupacao_unidade o
            WHERE o.pessoa_id = documento_identificacao.pessoa_id
              AND o.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = documento_identificacao.pessoa_id
              AND m.condominio_id = obter_condominio_sessao()
        )
    );

-- 5. RLS para Usuário (Conta de acesso vinculada a Pessoa)
ALTER TABLE usuario ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuario FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS isolamento_usuario ON usuario;
CREATE POLICY isolamento_usuario ON usuario
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = usuario.pessoa_id
              AND m.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR current_setting('app.bypass_rls', true) = 'on'
        OR EXISTS (
            SELECT 1 FROM membro_condominio m
            WHERE m.pessoa_id = usuario.pessoa_id
              AND m.condominio_id = obter_condominio_sessao()
        )
    );

-- 6. RLS para Tabelas Filhas Operacionais
-- 6.1 Evento Encomenda
ALTER TABLE evento_encomenda ENABLE ROW LEVEL SECURITY;
ALTER TABLE evento_encomenda FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_evento_encomenda ON evento_encomenda;
CREATE POLICY isolamento_evento_encomenda ON evento_encomenda
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM encomenda e
            WHERE e.id = evento_encomenda.encomenda_id
              AND e.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM encomenda e
            WHERE e.id = evento_encomenda.encomenda_id
              AND e.condominio_id = obter_condominio_sessao()
        )
    );

-- 6.2 Histórico Análise Cadastro
ALTER TABLE historico_analise_cadastro ENABLE ROW LEVEL SECURITY;
ALTER TABLE historico_analise_cadastro FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_historico_analise_cadastro ON historico_analise_cadastro;
CREATE POLICY isolamento_historico_analise_cadastro ON historico_analise_cadastro
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM solicitacao_cadastro_morador s
            WHERE s.id = historico_analise_cadastro.solicitacao_cadastro_id
              AND s.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM solicitacao_cadastro_morador s
            WHERE s.id = historico_analise_cadastro.solicitacao_cadastro_id
              AND s.condominio_id = obter_condominio_sessao()
        )
    );

-- 6.3 Histórico Ocorrência
ALTER TABLE historico_ocorrencia ENABLE ROW LEVEL SECURITY;
ALTER TABLE historico_ocorrencia FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_historico_ocorrencia ON historico_ocorrencia;
CREATE POLICY isolamento_historico_ocorrencia ON historico_ocorrencia
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM ocorrencia o
            WHERE o.id = historico_ocorrencia.ocorrencia_id
              AND o.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM ocorrencia o
            WHERE o.id = historico_ocorrencia.ocorrencia_id
              AND o.condominio_id = obter_condominio_sessao()
        )
    );

-- 6.4 Enquetes: Opções e Votos
ALTER TABLE opcao_enquete ENABLE ROW LEVEL SECURITY;
ALTER TABLE opcao_enquete FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_opcao_enquete ON opcao_enquete;
CREATE POLICY isolamento_opcao_enquete ON opcao_enquete
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM enquete eq
            WHERE eq.id = opcao_enquete.enquete_id
              AND eq.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM enquete eq
            WHERE eq.id = opcao_enquete.enquete_id
              AND eq.condominio_id = obter_condominio_sessao()
        )
    );

ALTER TABLE voto_enquete ENABLE ROW LEVEL SECURITY;
ALTER TABLE voto_enquete FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_voto_enquete ON voto_enquete;
CREATE POLICY isolamento_voto_enquete ON voto_enquete
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM enquete eq
            WHERE eq.id = voto_enquete.enquete_id
              AND eq.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM enquete eq
            WHERE eq.id = voto_enquete.enquete_id
              AND eq.condominio_id = obter_condominio_sessao()
        )
    );

-- 6.5 Assembleia: Pauta, Participante, Votação, Opção e Voto
ALTER TABLE pauta_assembleia ENABLE ROW LEVEL SECURITY;
ALTER TABLE pauta_assembleia FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_pauta_assembleia ON pauta_assembleia;
CREATE POLICY isolamento_pauta_assembleia ON pauta_assembleia
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM assembleia a
            WHERE a.id = pauta_assembleia.assembleia_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM assembleia a
            WHERE a.id = pauta_assembleia.assembleia_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    );

ALTER TABLE participante_assembleia ENABLE ROW LEVEL SECURITY;
ALTER TABLE participante_assembleia FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_participante_assembleia ON participante_assembleia;
CREATE POLICY isolamento_participante_assembleia ON participante_assembleia
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM assembleia a
            WHERE a.id = participante_assembleia.assembleia_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM assembleia a
            WHERE a.id = participante_assembleia.assembleia_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    );

ALTER TABLE votacao_assembleia ENABLE ROW LEVEL SECURITY;
ALTER TABLE votacao_assembleia FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_votacao_assembleia ON votacao_assembleia;
CREATE POLICY isolamento_votacao_assembleia ON votacao_assembleia
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM pauta_assembleia pa
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE pa.id = votacao_assembleia.pauta_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM pauta_assembleia pa
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE pa.id = votacao_assembleia.pauta_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    );

ALTER TABLE opcao_votacao ENABLE ROW LEVEL SECURITY;
ALTER TABLE opcao_votacao FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_opcao_votacao ON opcao_votacao;
CREATE POLICY isolamento_opcao_votacao ON opcao_votacao
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM votacao_assembleia va
            JOIN pauta_assembleia pa ON pa.id = va.pauta_id
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE va.id = opcao_votacao.votacao_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM votacao_assembleia va
            JOIN pauta_assembleia pa ON pa.id = va.pauta_id
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE va.id = opcao_votacao.votacao_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    );

ALTER TABLE voto_assembleia ENABLE ROW LEVEL SECURITY;
ALTER TABLE voto_assembleia FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS isolamento_voto_assembleia ON voto_assembleia;
CREATE POLICY isolamento_voto_assembleia ON voto_assembleia
    FOR ALL
    USING (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM votacao_assembleia va
            JOIN pauta_assembleia pa ON pa.id = va.pauta_id
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE va.id = voto_assembleia.votacao_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    )
    WITH CHECK (
        obter_condominio_sessao() IS NULL
        OR EXISTS (
            SELECT 1 FROM votacao_assembleia va
            JOIN pauta_assembleia pa ON pa.id = va.pauta_id
            JOIN assembleia a ON a.id = pa.assembleia_id
            WHERE va.id = voto_assembleia.votacao_id
              AND a.condominio_id = obter_condominio_sessao()
        )
    );

COMMIT;
