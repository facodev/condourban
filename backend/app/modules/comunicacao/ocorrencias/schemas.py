from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field


class HistoricoOcorrenciaBase(BaseModel):
    autor_id: uuid.UUID
    mensagem: str
    tipo: str = 'COMENTARIO'


class HistoricoOcorrenciaCreate(HistoricoOcorrenciaBase):
    pass


class HistoricoOcorrenciaResponse(HistoricoOcorrenciaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    ocorrencia_id: uuid.UUID
    criado_em: datetime


class OcorrenciaBase(BaseModel):
    unidade_id: uuid.UUID | None = None
    origem: str = 'MORADOR'
    categoria: str | None = None
    titulo: str = Field(..., max_length=200)
    descricao: str
    prioridade: str = 'NORMAL'
    status: str = 'ABERTA'
    sigilosa: bool = False
    responsavel_id: uuid.UUID | None = None


class OcorrenciaCreate(OcorrenciaBase):
    registrada_por: uuid.UUID | None = None
    usuario_id: uuid.UUID | None = None


class OcorrenciaUpdate(BaseModel):
    categoria: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    prioridade: str | None = None
    status: str | None = None
    sigilosa: bool | None = None
    responsavel_id: uuid.UUID | None = None
    resolvida_em: datetime | None = None


class OcorrenciaStatusUpdate(BaseModel):
    status: str
    mensagem: str | None = None


class OcorrenciaResponse(OcorrenciaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    registrada_por: uuid.UUID | None = None
    criada_em: datetime
    resolvida_em: datetime | None = None
    historico: list[HistoricoOcorrenciaResponse] = []

    usuario_id: uuid.UUID | None = None
    criado_em: datetime | None = None



# Aliases de retrocompatibilidade
OccurrenceBase = OcorrenciaBase
OccurrenceCreate = OcorrenciaCreate
OccurrenceResponse = OcorrenciaResponse
OccurrenceHistoryBase = HistoricoOcorrenciaBase
OccurrenceHistoryResponse = HistoricoOcorrenciaResponse
