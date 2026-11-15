from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
from pydantic import BaseModel, ConfigDict, Field


class VistoriaReservaBase(BaseModel):
    reserva_id: uuid.UUID
    vistoriador_id: uuid.UUID
    tipo: str = Field(..., description="'ENTRADA' ou 'SAIDA'")
    checklist: dict[str, Any] = Field(default_factory=dict)
    avarias_detectadas: str | None = None
    fotos: list[str] = Field(default_factory=list)
    valor_caucao_retido: Decimal = Decimal('0.00')


class VistoriaReservaCreate(VistoriaReservaBase):
    pass


class VistoriaReservaResponse(VistoriaReservaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    concluida_em: datetime
    criado_em: datetime
