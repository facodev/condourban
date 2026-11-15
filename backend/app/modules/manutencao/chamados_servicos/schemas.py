from datetime import date, datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field


class ChamadoManutencaoBase(BaseModel):
    unidade_id: uuid.UUID | None = None
    categoria: str = Field(..., max_length=50)
    titulo: str = Field(..., max_length=200)
    descricao: str
    localizacao: str | None = Field(None, max_length=200)
    foto_url: str | None = None
    prioridade: str = 'MEDIA'
    status: str = 'ABERTO'
    atribuido_a: uuid.UUID | None = None


class ChamadoManutencaoCreate(ChamadoManutencaoBase):
    solicitante_id: uuid.UUID | None = None


class ChamadoManutencaoUpdate(BaseModel):
    categoria: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    localizacao: str | None = None
    foto_url: str | None = None
    prioridade: str | None = None
    status: str | None = None
    atribuido_a: uuid.UUID | None = None
    concluido_em: datetime | None = None


class ChamadoManutencaoResponse(ChamadoManutencaoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    solicitante_id: uuid.UUID
    criado_em: datetime
    concluido_em: datetime | None = None


class OrdemServicoBase(BaseModel):
    chamado_id: uuid.UUID | None = None
    prestador_id: uuid.UUID | None = None
    responsavel_interno_id: uuid.UUID | None = None
    descricao: str
    valor_estimado: Decimal | None = None
    valor_final: Decimal | None = None
    data_agendada: date | None = None
    status: str = 'RASCUNHO'
    laudo_conclusao: str | None = None


class OrdemServicoCreate(OrdemServicoBase):
    pass


class OrdemServicoUpdate(BaseModel):
    descricao: str | None = None
    valor_estimado: Decimal | None = None
    valor_final: Decimal | None = None
    data_agendada: date | None = None
    status: str | None = None
    laudo_conclusao: str | None = None
    iniciado_em: datetime | None = None
    finalizado_em: datetime | None = None


class OrdemServicoResponse(OrdemServicoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    iniciado_em: datetime | None = None
    finalizado_em: datetime | None = None
    criada_em: datetime
    atualizada_em: datetime


# Aliases
MaintenanceTicketResponse = ChamadoManutencaoResponse
WorkOrderResponse = OrdemServicoResponse
