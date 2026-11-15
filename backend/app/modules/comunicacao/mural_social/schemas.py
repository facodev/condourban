from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field


class OpcaoEnqueteBase(BaseModel):
    descricao: str = Field(..., max_length=300)
    ordem: int


class OpcaoEnqueteCreate(OpcaoEnqueteBase):
    pass


class OpcaoEnqueteResponse(OpcaoEnqueteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    enquete_id: uuid.UUID


class VotoEnqueteCreate(BaseModel):
    opcao_id: uuid.UUID


class VotoEnqueteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    enquete_id: uuid.UUID
    opcao_id: uuid.UUID
    pessoa_id: uuid.UUID
    votado_em: datetime


class EnqueteBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    descricao: str | None = None
    inicio_em: datetime
    fim_em: datetime
    anonima: bool = False
    status: str = 'RASCUNHO'


class EnqueteCreate(EnqueteBase):
    opcoes: list[OpcaoEnqueteCreate] = []


class EnqueteResponse(EnqueteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criada_por: uuid.UUID | None = None
    criada_em: datetime
    opcoes: list[OpcaoEnqueteResponse] = []


class ItemComunidadeBase(BaseModel):
    tipo: str = 'CLASSIFICADO'
    titulo: str = Field(..., max_length=200)
    descricao: str
    preco: Decimal | None = None
    contato: str | None = Field(None, max_length=100)
    foto_url: str | None = None
    status: str = 'ATIVO'
    expira_em: datetime | None = None


class ItemComunidadeCreate(ItemComunidadeBase):
    pass


class ItemComunidadeResponse(ItemComunidadeBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    autor_id: uuid.UUID
    criado_em: datetime


# Aliases
PollResponse = EnqueteResponse
CommunityItemResponse = ItemComunidadeResponse
