from datetime import date, datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field


class DespesaCondominialBase(BaseModel):
    categoria: str = Field(..., max_length=100)
    fornecedor: str = Field(..., max_length=200)
    cnpj_cpf_fornecedor: str | None = Field(None, max_length=30)
    descricao: str
    valor: Decimal
    data_emissao: date
    data_vencimento: date
    data_pagamento: date | None = None
    chave_comprovante: str | None = None
    aprovada_conselho: bool = False
    status: str = 'PENDENTE'


class DespesaCondominialCreate(DespesaCondominialBase):
    pass


class DespesaCondominialUpdate(BaseModel):
    categoria: str | None = None
    fornecedor: str | None = None
    cnpj_cpf_fornecedor: str | None = None
    descricao: str | None = None
    valor: Decimal | None = None
    data_vencimento: date | None = None
    data_pagamento: date | None = None
    chave_comprovante: str | None = None
    aprovada_conselho: bool | None = None
    status: str | None = None


class DespesaCondominialResponse(DespesaCondominialBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criado_em: datetime
    atualizado_em: datetime


class MedicaoIndividualBase(BaseModel):
    unidade_id: uuid.UUID
    tipo_consumo: str = Field(..., description="'AGUA_FRIA', 'AGUA_QUENTE', 'GAS', 'ENERGIA'")
    competencia: date
    leitura_anterior: Decimal
    leitura_atual: Decimal
    consumo: Decimal
    valor_calculado: Decimal
    foto_medidor_url: str | None = None


class MedicaoIndividualCreate(MedicaoIndividualBase):
    lancado_por: uuid.UUID | None = None


class MedicaoIndividualResponse(MedicaoIndividualBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    lancado_por: uuid.UUID | None = None
    criado_em: datetime


# Aliases
CondoExpenseResponse = DespesaCondominialResponse
IndividualMeasurementResponse = MedicaoIndividualResponse
