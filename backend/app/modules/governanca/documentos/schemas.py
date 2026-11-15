from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.governanca.seguranca_auditoria.schemas import (
    DocumentoBase,
    DocumentoCreate,
    DocumentoResponse,
    PastaDocumentoBase,
    PastaDocumentoCreate,
    PastaDocumentoResponse,
)


class DownloadResponse(BaseModel):
    url: str
    nome: str


class AlertaVencimentoResponse(BaseModel):
    documento_id: uuid.UUID
    nome: str
    vencimento_em: datetime
    dias_restantes: int


__all__ = [
    'DocumentoBase',
    'DocumentoCreate',
    'DocumentoResponse',
    'PastaDocumentoBase',
    'PastaDocumentoCreate',
    'PastaDocumentoResponse',
    'DownloadResponse',
    'AlertaVencimentoResponse',
]
