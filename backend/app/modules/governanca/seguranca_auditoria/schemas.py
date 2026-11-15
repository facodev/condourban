from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, ConfigDict, Field


class PastaDocumentoBase(BaseModel):
    pasta_pai_id: uuid.UUID | None = None
    nome: str = Field(..., max_length=200)
    visibilidade: str = 'ADMINISTRADORES'


class PastaDocumentoCreate(PastaDocumentoBase):
    pass


class PastaDocumentoResponse(PastaDocumentoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criada_em: datetime


class DocumentoBase(BaseModel):
    pasta_id: uuid.UUID | None = None
    nome: str = Field(..., max_length=255)
    tipo_mime: str | None = None
    tamanho_bytes: int | None = None
    versao: int = 1
    vencimento_em: datetime | None = None


class DocumentoCreate(DocumentoBase):
    chave_armazenamento: str
    hash_arquivo: str | None = None


class DocumentoResponse(DocumentoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    chave_armazenamento: str
    hash_arquivo: str | None = None
    enviado_por: uuid.UUID | None = None
    criado_em: datetime
    excluido_em: datetime | None = None



class EventoAuditoriaBase(BaseModel):
    acao: str = Field(..., max_length=100)
    entidade: str = Field(..., max_length=100)
    entidade_id: uuid.UUID | None = None
    endereco_ip: str | None = None
    agente_usuario: str | None = None
    id_correlacao: str | None = None
    dados_anteriores: dict[str, Any] | None = None
    dados_posteriores: dict[str, Any] | None = None


class EventoAuditoriaCreate(EventoAuditoriaBase):
    usuario_id: uuid.UUID | None = None
    pessoa_id: uuid.UUID | None = None


class EventoAuditoriaResponse(EventoAuditoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID | None = None
    usuario_id: uuid.UUID | None = None
    pessoa_id: uuid.UUID | None = None
    ocorrido_em: datetime

    # Compatibilidade com UI
    @property
    def timestamp(self) -> str:
        return self.ocorrido_em.isoformat()


class EventoUsoCreate(BaseModel):
    modulo: str = Field(..., max_length=50)
    funcionalidade_codigo: str | None = None
    acao: str = Field(..., max_length=50)
    metadados: dict[str, Any] = Field(default_factory=dict)


class EventoUsoResponse(EventoUsoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID | None = None
    usuario_id: uuid.UUID | None = None
    ocorrido_em: datetime


# Aliases
AuditLogResponse = EventoAuditoriaResponse
