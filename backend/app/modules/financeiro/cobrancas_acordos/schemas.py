from datetime import date, datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field


class CobrancaCondominialBase(BaseModel):
    unidade_id: uuid.UUID
    competencia: date
    vencimento: date
    valor: Decimal
    valor_multa: Decimal = Decimal('0.00')
    valor_juros: Decimal = Decimal('0.00')
    valor_desconto: Decimal = Decimal('0.00')
    status: str = 'PENDENTE'
    provedor_pagamento: str | None = None
    identificacao_externa: str | None = None
    linha_digitavel: str | None = None
    codigo_pix: str | None = None


class CobrancaCondominialCreate(CobrancaCondominialBase):
    pass


class CobrancaCondominialUpdate(BaseModel):
    vencimento: date | None = None
    valor: Decimal | None = None
    valor_multa: Decimal | None = None
    valor_juros: Decimal | None = None
    valor_desconto: Decimal | None = None
    status: str | None = None
    linha_digitavel: str | None = None
    codigo_pix: str | None = None
    pago_em: datetime | None = None
    valor_pago: Decimal | None = None


class CobrancaCondominialResponse(CobrancaCondominialBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pago_em: datetime | None = None
    valor_pago: Decimal | None = None
    criado_em: datetime
    atualizado_em: datetime


class TermoAcordoBase(BaseModel):
    unidade_id: uuid.UUID
    devedor_id: uuid.UUID
    valor_total_original: Decimal
    valor_total_negociado: Decimal
    numero_parcelas: int = Field(..., gt=0)
    dia_vencimento_parcelas: int = Field(10, ge=1, le=31)
    status: str = 'ATIVO'
    observacao: str | None = None


class TermoAcordoCreate(TermoAcordoBase):
    pass


class TermoAcordoResponse(TermoAcordoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    assinado_em: datetime | None = None
    criado_em: datetime
    atualizado_em: datetime


# Aliases
CondoChargeResponse = CobrancaCondominialResponse
