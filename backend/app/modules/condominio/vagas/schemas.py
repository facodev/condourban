import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VagaGaragemBase(BaseModel):
    identificacao: str
    tipo: str | None = None
    coberta: bool = False


class VagaGaragemCreate(VagaGaragemBase):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None


class VagaGaragemUpdate(BaseModel):
    identificacao: str | None = None
    unidade_id: uuid.UUID | None = None
    tipo: str | None = None
    coberta: bool | None = None


class VagaGaragemResponse(VagaGaragemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID | None = None
    status: str
    criado_em: datetime

