BEGIN;

INSERT INTO motivo_correcao_cadastro (codigo, descricao)
VALUES
    ('DOCUMENTO_ILEGIVEL', 'Documento ilegível'),
    ('DOCUMENTO_INCOMPLETO', 'Documento incompleto'),
    ('DOCUMENTO_INVALIDO', 'Documento inválido'),
    ('DADOS_DIVERGENTES', 'Dados divergentes'),
    ('COMPROVANTE_INSUFICIENTE', 'Comprovante de vínculo insuficiente'),
    ('FACIAL_INCONCLUSIVA', 'Verificação facial inconclusiva'),
    ('PROVA_VIDA_REPROVADA', 'Prova de vida reprovada'),
    ('OUTRO', 'Outro motivo')
ON CONFLICT (codigo) DO UPDATE
SET descricao = EXCLUDED.descricao;

COMMIT;
