from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field


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
