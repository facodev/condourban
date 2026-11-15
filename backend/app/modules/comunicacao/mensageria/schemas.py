from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field


class ComunicadoBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    conteudo: str
    urgente: bool = False
    fixado: bool = False
    status: str = 'RASCUNHO'
    publicado_em: datetime | None = None
    expira_em: datetime | None = None


class ComunicadoCreate(ComunicadoBase):
    autor_id: uuid.UUID | None = None
    bloco_ids: list[uuid.UUID] | None = None


class ComunicadoUpdate(BaseModel):
    titulo: str | None = None
    conteudo: str | None = None
    urgente: bool | None = None
    fixado: bool | None = None
    status: str | None = None
    publicado_em: datetime | None = None
    expira_em: datetime | None = None


class ComunicadoResponse(ComunicadoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    autor_id: uuid.UUID
    criado_em: datetime
    lido: bool | None = False


class LeituraComunicadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    comunicado_id: uuid.UUID
    pessoa_id: uuid.UUID
    lido_em: datetime


class ConfirmarLeituraResponse(BaseModel):
    confirmado_em: datetime
    status: str = 'CONFIRMADO'
    comunicado_id: uuid.UUID
    pessoa_id: uuid.UUID


class MensagemFaleConoscoBase(BaseModel):
    destinatario_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None
    assunto: str = Field(..., max_length=200)
    mensagem: str


class MensagemFaleConoscoCreate(MensagemFaleConoscoBase):
    remetente_id: uuid.UUID | None = None


class MensagemFaleConoscoResponse(MensagemFaleConoscoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    remetente_id: uuid.UUID
    sla_horas: int = 48
    prazo_sla: datetime | None = None
    status: str = 'NOVA_MENSAGEM'
    lida_em: datetime | None = None
    enviada_em: datetime


# Aliases de retrocompatibilidade
NoticeBase = ComunicadoBase
NoticeCreate = ComunicadoCreate
NoticeResponse = ComunicadoResponse

