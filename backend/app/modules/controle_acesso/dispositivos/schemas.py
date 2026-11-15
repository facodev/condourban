import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DispositivoAcessoBase(BaseModel):
    nome: str
    tipo: str
    provedor: str
    identificacao_externa: str | None = None
    endereco_ip: str | None = None
    localizacao: str | None = None
    sentido: str | None = 'ENTRADA'


class DispositivoAcessoCreate(DispositivoAcessoBase):
    condominio_id: uuid.UUID


class DispositivoAcessoResponse(DispositivoAcessoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    status: str
    criado_em: datetime
