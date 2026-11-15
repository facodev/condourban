import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BlocoBase(BaseModel):
    nome: str
    descricao: str | None = None
    ordem: int | None = None

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('nome') and data.get('name'):
                data['nome'] = data['name']
            if not data.get('descricao') and data.get('description'):
                data['descricao'] = data['description']
        return data


class BlocoCreate(BlocoBase):
    condominio_id: uuid.UUID | None = None


class BlocoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    ordem: int | None = None
    status: str | None = None

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('nome') and data.get('name'):
                data['nome'] = data['name']
            if not data.get('descricao') and data.get('description'):
                data['descricao'] = data['description']
        return data


class BlocoResponse(BlocoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    status: str
    criado_em: datetime


class UnidadeBase(BaseModel):
    identificacao: str
    andar: int | str | None = None
    tipo: str | None = None
    descricao: str | None = None
    area_privativa: Decimal | None = None

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('identificacao') and data.get('number'):
                data['identificacao'] = str(data['number'])
            if not data.get('andar') and data.get('floor'):
                data['andar'] = data['floor']
            if not data.get('bloco_id') and data.get('blocoId'):
                data['bloco_id'] = data['blocoId']
            if not data.get('bloco_id') and data.get('block_id'):
                data['bloco_id'] = data['block_id']
        return data


class UnidadeCreate(UnidadeBase):
    condominio_id: uuid.UUID | None = None
    bloco_id: uuid.UUID | None = None


class UnidadeUpdate(BaseModel):
    identificacao: str | None = None
    andar: int | str | None = None
    bloco_id: uuid.UUID | None = None
    tipo: str | None = None
    descricao: str | None = None
    area_privativa: Decimal | None = None
    status: str | None = None

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('identificacao') and data.get('number'):
                data['identificacao'] = str(data['number'])
            if not data.get('andar') and data.get('floor'):
                data['andar'] = data['floor']
            if not data.get('bloco_id') and data.get('blocoId'):
                data['bloco_id'] = data['blocoId']
        return data


class UnidadeResponse(UnidadeBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    bloco_id: uuid.UUID | None = None
    status: str
    criado_em: datetime


# Aliases
BlockResponse = BlocoResponse
UnitResponse = UnidadeResponse

