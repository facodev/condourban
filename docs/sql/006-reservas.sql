BEGIN;

-- Contexto: reservas
-- Ciclo de agendamento de áreas comuns, validação de regras, lista de convidados e vistorias/caução

CREATE TABLE reserva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    area_comum_id UUID NOT NULL REFERENCES area_comum(id),
    unidade_id UUID NOT NULL REFERENCES unidade(id),
    solicitante_id UUID NOT NULL REFERENCES pessoa(id),
    inicio_em TIMESTAMPTZ NOT NULL,
    fim_em TIMESTAMPTZ NOT NULL,
    valor NUMERIC(12,2),
    termo_aceito BOOLEAN NOT NULL DEFAULT true,
    status VARCHAR(50) NOT NULL DEFAULT 'SOLICITADA',
    observacao TEXT,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (fim_em > inicio_em)
);

CREATE INDEX ix_reserva_area_periodo
ON reserva(area_comum_id, inicio_em, fim_em);
CREATE INDEX ix_reserva_unidade ON reserva(condominio_id, unidade_id);

-- Sub-recurso: Lista de convidados da reserva
CREATE TABLE convidado_reserva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    reserva_id UUID NOT NULL REFERENCES reserva(id) ON DELETE CASCADE,
    nome_completo VARCHAR(200) NOT NULL,
    documento VARCHAR(30),
    presente BOOLEAN NOT NULL DEFAULT false,
    horario_entrada TIMESTAMPTZ,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_convidado_reserva ON convidado_reserva(reserva_id);

-- Submódulo: Vistorias pré/pós evento e conferência de caução
CREATE TABLE vistoria_reserva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    condominio_id UUID NOT NULL REFERENCES condominio(id),
    reserva_id UUID NOT NULL REFERENCES reserva(id),
    vistoriador_id UUID NOT NULL REFERENCES pessoa(id),
    tipo tipo_vistoria NOT NULL,
    checklist JSONB NOT NULL DEFAULT '{}'::jsonb,
    avarias_detectadas TEXT,
    fotos JSONB NOT NULL DEFAULT '[]'::jsonb,
    valor_caucao_retido NUMERIC(12,2) DEFAULT 0.00,
    concluida_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_vistoria_reserva ON vistoria_reserva(reserva_id);

COMMIT;
