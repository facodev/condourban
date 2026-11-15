import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class AreaComumBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome: str
    descricao: str | None = None
    capacidade: int = 0
    requer_aprovacao: bool = False
    taxa_reserva: Decimal | None = Decimal('0.00')
    valor_caucao: Decimal | None = Decimal('0.00')
    horario_abertura: str = '08:00'
    horario_fechamento: str = '22:00'
    regras_dias: dict[str, Any] = {}
    ativo: bool = True

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'valorReserva' in data and not data.get('taxa_reserva'):
                data['taxa_reserva'] = data['valorReserva']
            if 'taxaReserva' in data and not data.get('taxa_reserva'):
                data['taxa_reserva'] = data['taxaReserva']
            if 'horarioAbertura' in data and not data.get('horario_abertura'):
                data['horario_abertura'] = data['horarioAbertura']
            if 'horarioFechamento' in data and not data.get('horario_fechamento'):
                data['horario_fechamento'] = data['horarioFechamento']
            if 'requerAprovacao' in data and not data.get('requer_aprovacao'):
                data['requer_aprovacao'] = data['requerAprovacao']
            if 'regrasDias' in data and not data.get('regras_dias'):
                data['regras_dias'] = data['regrasDias']
        return data


class AreaComumCreate(AreaComumBase):
    condominio_id: uuid.UUID | None = None


class AreaComumUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome: str | None = None
    descricao: str | None = None
    capacidade: int | None = None
    requer_aprovacao: bool | None = None
    taxa_reserva: Decimal | None = None
    valor_caucao: Decimal | None = None
    horario_abertura: str | None = None
    horario_fechamento: str | None = None
    regras_dias: dict[str, Any] | None = None
    ativo: bool | None = None

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'valorReserva' in data and not data.get('taxa_reserva'):
                data['taxa_reserva'] = data['valorReserva']
            if 'taxaReserva' in data and not data.get('taxa_reserva'):
                data['taxa_reserva'] = data['taxaReserva']
            if 'horarioAbertura' in data and not data.get('horario_abertura'):
                data['horario_abertura'] = data['horarioAbertura']
            if 'horarioFechamento' in data and not data.get('horario_fechamento'):
                data['horario_fechamento'] = data['horarioFechamento']
            if 'requerAprovacao' in data and 'requer_aprovacao' not in data:
                data['requer_aprovacao'] = data['requerAprovacao']
            if 'regrasDias' in data and not data.get('regras_dias'):
                data['regras_dias'] = data['regrasDias']
        return data


class AreaComumResponse(AreaComumBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    status: str = 'ATIVO'
    criado_em: datetime


# Aliases de retrocompatibilidade
CommonAreaBase = AreaComumBase
CommonAreaCreate = AreaComumCreate
CommonAreaResponse = AreaComumResponse
