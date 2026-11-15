import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VeiculoBase(BaseModel):
    placa: str
    tipo: str = 'CARRO'
    marca: str | None = None
    modelo: str | None = None
    cor: str | None = None
    observacao: str | None = None


class VeiculoCreate(VeiculoBase):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    proprietario_id: uuid.UUID | None = None
    vaga_garagem_id: uuid.UUID | None = None


class VeiculoResponse(VeiculoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    status: str
    criado_em: datetime


class PetBase(BaseModel):
    nome: str
    especie: str = 'CANINO'
    raca: str | None = None
    porte: str = 'MEDIO'
    cor: str | None = None
    foto_url: str | None = None
    vacinado: bool = True
    observacao: str | None = None


class PetCreate(PetBase):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    tutor_id: uuid.UUID | None = None


class PetResponse(PetBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    status: str
    criado_em: datetime
