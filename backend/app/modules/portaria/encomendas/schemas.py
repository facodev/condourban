import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EncomendaBase(BaseModel):
    transportadora: str | None = None
    codigo_rastreio: str | None = None
    descricao: str | None = None
    local_armazenamento: str | None = None
    foto_url: str | None = None
    observacao: str | None = None
    status: str = 'RECEBIDA'


class EncomendaCreate(EncomendaBase):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    destinatario_id: uuid.UUID | None = None


class EncomendaResponse(EncomendaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    destinatario_id: uuid.UUID | None = None
    codigo_retirada: str | None = None
    status: str
    recebida_em: datetime | None = None
    retirada_em: datetime | None = None


class BaixaEncomendaRequest(BaseModel):
    codigo_retirada: str


# Aliases de retrocompatibilidade
DeliveryBase = EncomendaBase
DeliveryCreate = EncomendaCreate
DeliveryResponse = EncomendaResponse
