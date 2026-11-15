from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field


class ConvidadoReservaBase(BaseModel):
    nome_completo: str = Field(..., max_length=200)
    documento: str | None = Field(None, max_length=30)
    presente: bool = False
    horario_entrada: datetime | None = None


class ConvidadoReservaCreate(ConvidadoReservaBase):
    pass


class ConvidadoReservaResponse(ConvidadoReservaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    reserva_id: uuid.UUID
    criado_em: datetime


class ReservaBase(BaseModel):
    area_comum_id: uuid.UUID
    unidade_id: uuid.UUID
    solicitante_id: uuid.UUID | None = None
    usuario_id: uuid.UUID | None = None
    inicio_em: datetime
    fim_em: datetime
    valor: Decimal | None = None
    termo_aceito: bool = True
    status: str = 'SOLICITADA'
    observacao: str | None = None


class ReservaCreate(ReservaBase):
    convidados: list[ConvidadoReservaCreate] | None = None


class ReservaUpdate(BaseModel):
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    valor: Decimal | None = None
    termo_aceito: bool | None = None
    status: str | None = None
    observacao: str | None = None


class ReservaResponse(ReservaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    solicitante_id: uuid.UUID
    usuario_id: uuid.UUID
    criado_em: datetime
    atualizado_em: datetime
    convidados: list[ConvidadoReservaResponse] = []


# Aliases de retrocompatibilidade
ReservationBase = ReservaBase
ReservationCreate = ReservaCreate
ReservationResponse = ReservaResponse
