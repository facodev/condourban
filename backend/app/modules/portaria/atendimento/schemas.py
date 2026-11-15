import uuid
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict


class VisitanteBase(BaseModel):
    observacao: str | None = None
    nome_completo: str | None = None
    documento: str | None = None


class VisitanteCreate(VisitanteBase):
    condominio_id: uuid.UUID | None = None
    pessoa_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None
    responsavel_id: uuid.UUID | None = None
    status: str = 'AUTORIZADO'


class VisitanteResponse(VisitanteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None
    status: str
    criado_em: datetime


class PrestadorBase(BaseModel):
    empresa: str | None = None
    documento_empresa: str | None = None
    atividade: str | None = None
    observacao: str | None = None


class PrestadorCreate(PrestadorBase):
    condominio_id: uuid.UUID | None = None
    pessoa_id: uuid.UUID | None = None


class PrestadorResponse(PrestadorBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID | None = None
    status: str
    criado_em: datetime


class RegistroVisitaCreate(BaseModel):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    visitante_id: uuid.UUID | None = None
    prestador_id: uuid.UUID | None = None
    atendido_por: uuid.UUID | None = None
    observacao: str | None = None


class RegistroVisitaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    visitante_id: uuid.UUID | None = None
    prestador_id: uuid.UUID | None = None
    entrada_em: datetime
    saida_em: datetime | None = None
    observacao: str | None = None


class AgendamentoMudancaCreate(BaseModel):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    solicitante_id: uuid.UUID
    tipo_mudanca: str = 'ENTRADA'
    data_hora_inicio: datetime
    data_hora_fim: datetime
    reserva_elevador: bool = True
    observacao: str | None = None


class AgendamentoMudancaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    tipo_mudanca: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    criado_em: datetime


class ItemPerdidoCreate(BaseModel):
    condominio_id: uuid.UUID | None = None
    descricao: str
    categoria: str | None = None
    local_encontrado: str | None = None
    foto_url: str | None = None
    observacao: str | None = None


class ItemPerdidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    descricao: str
    categoria: str | None = None
    local_encontrado: str | None = None
    status: str
    encontrado_em: datetime


# Aliases
VisitorCreate = VisitanteCreate
VisitorResponse = VisitanteResponse
