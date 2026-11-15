import uuid
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict


class CredencialAcessoBase(BaseModel):
    tipo: str  # TAG_RFID, FACIAL, QR_CODE, SENHA
    provedor: str
    referencia_externa: str | None = None


class CredencialAcessoCreate(CredencialAcessoBase):
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID


class CredencialAcessoResponse(CredencialAcessoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID
    status: str
    criada_em: datetime


class AutorizacaoAcessoBase(BaseModel):
    tipo_autorizacao: str
    inicio_em: datetime
    fim_em: datetime | None = None
    horario_inicio: time | None = None
    horario_fim: time | None = None
    motivo: str | None = None


class AutorizacaoAcessoCreate(AutorizacaoAcessoBase):
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID
    credencial_acesso_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None


class AutorizacaoAcessoResponse(AutorizacaoAcessoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID
    status: str
    criado_em: datetime
