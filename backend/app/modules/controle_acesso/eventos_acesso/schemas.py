import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class EventoAcessoBase(BaseModel):
    tipo_evento: str
    resultado: str | None = None
    ocorrido_em: datetime
    identificacao_externa: str | None = None
    pontuacao_facial: Decimal | None = None
    imagem_referencia_url: str | None = None


class EventoAcessoCreate(EventoAcessoBase):
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID | None = None
    credencial_acesso_id: uuid.UUID | None = None
    dispositivo_acesso_id: uuid.UUID | None = None


class EventoAcessoResponse(EventoAcessoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID | None = None
    dispositivo_acesso_id: uuid.UUID | None = None
    criado_em: datetime


class SincronizacaoAcessoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    tipo_operacao: str
    entidade: str
    entidade_id: uuid.UUID
    status: str
    tentativas: int
    criada_em: datetime
