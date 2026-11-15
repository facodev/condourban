BEGIN;

-- Contrato de Isolamento Multi-tenant via Row Level Security (RLS)
-- O backend FastAPI deve executar no início da transação:
--   SET LOCAL app.condominio_id = '<uuid-do-condominio>';
-- após validar o token JWT e o membership do usuário no condomínio selecionado.

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
        -- 2. Condomínio (Estrutura Física)
        'bloco',
        'unidade',
        'vaga_garagem',
        'area_comum',

        -- 1. Identidade e Cadastro
        'membro_condominio',
        'ocupacao_unidade',
        'convite_cadastro_morador',
        'solicitacao_cadastro_morador',
        'documento_cadastro',
        'verificacao_facial',
        'veiculo',
        'pet',

        -- 3. Controle de Acesso (IoT / Hardware)
        'integracao_provedor',
        'dispositivo_acesso',
        'credencial_acesso',
        'autorizacao_acesso',
        'evento_acesso',
        'sincronizacao_acesso',

        -- 4. Portaria e Atendimento
        'visitante',
        'convite_visitante',
        'prestador',
        'autorizacao_prestador',
        'registro_visita',
        'encomenda',
        'agendamento_mudanca',
        'item_perdido',

        -- 5. Reservas e Espaços Comuns
        'reserva',
        'convidado_reserva',
        'vistoria_reserva',

        -- 6. Comunicação e Convivência
        'comunicado',
        'leitura_comunicado',
        'ocorrencia',
        'enquete',
        'item_comunidade',
        'mensagem_fale_conosco',

        -- 7. Governança e Administração Legal
        'assembleia',
        'procuracao_assembleia',
        'ata_assembleia',
        'pasta_documento',
        'documento',

        -- 8. Financeiro e Tarifação
        'cobranca_condominial',
        'despesa_condominial',
        'termo_acordo',
        'medicao_individual',

        -- 9. Manutenção e PMO Preventivo
        'chamado_manutencao',
        'ordem_servico',
        'item_preventiva_pmo',
        'registro_inspecao_pmo',

        -- Transversal / Auditoria
        'evento_auditoria',
        'evento_uso'
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
