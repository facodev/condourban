BEGIN;

-- O FastAPI deve executar:
-- SET LOCAL app.condominio_id = '<uuid>';
-- após validar o JWT e a associação do usuário ao condomínio.

CREATE OR REPLACE FUNCTION obter_condominio_sessao()
RETURNS UUID
LANGUAGE sql
STABLE
AS $$
    SELECT NULLIF(current_setting('app.condominio_id', true), '')::uuid
$$;

DO $$
DECLARE
    tabela TEXT;
BEGIN
    FOREACH tabela IN ARRAY ARRAY[
        'unidade',
        'bloco',
        'vaga_garagem',
        'area_comum',
        'membro_condominio',
        'ocupacao_unidade',
        'convite_cadastro_morador',
        'solicitacao_cadastro_morador',
        'documento_cadastro',
        'verificacao_facial',
        'historico_analise_cadastro',
        'integracao_provedor',
        'dispositivo_acesso',
        'credencial_acesso',
        'autorizacao_acesso',
        'evento_acesso',
        'sincronizacao_acesso',
        'visitante',
        'convite_visitante',
        'prestador',
        'autorizacao_prestador',
        'encomenda',
        'ocorrencia',
        'pasta_documento',
        'documento',
        'comunicado',
        'enquete',
        'assembleia',
        'reserva',
        'cobranca_condominial',
        'evento_auditoria'
    ]
    LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', tabela);

        EXECUTE format(
            'DROP POLICY IF EXISTS isolamento_condominio ON %I',
            tabela
        );

        EXECUTE format(
            'CREATE POLICY isolamento_condominio ON %I
             USING (condominio_id = obter_condominio_sessao())
             WITH CHECK (condominio_id = obter_condominio_sessao())',
            tabela
        );
    END LOOP;
END $$;

COMMIT;
