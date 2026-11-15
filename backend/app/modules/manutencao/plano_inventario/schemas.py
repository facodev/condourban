from datetime import date, datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field


class ItemPreventivaPMOBase(BaseModel):
    sistema: str = Field(..., max_length=100)
    descricao: str = Field(..., max_length=300)
    periodicidade_dias: int = Field(..., gt=0)
    instrucao_tecnica: str | None = None
    proxima_inspecao: date
    ativo: bool = True


class ItemPreventivaPMOCreate(ItemPreventivaPMOBase):
    pass


class ItemPreventivaPMOUpdate(BaseModel):
    sistema: str | None = None
    descricao: str | None = None
    periodicidade_dias: int | None = None
    instrucao_tecnica: str | None = None
    proxima_inspecao: date | None = None
    ativo: bool | None = None


class ItemPreventivaPMOResponse(ItemPreventivaPMOBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criado_em: datetime


class RegistroInspecaoPMOBase(BaseModel):
    item_preventiva_pmo_id: uuid.UUID
    inspecionado_em: date
    responsavel_tecnico: str = Field(..., max_length=200)
    registro_profissional: str | None = Field(None, max_length=50)
    conforme: bool = True
    parecer_tecnico: str | None = None
    chave_art_laudo: str | None = None


class RegistroInspecaoPMOCreate(RegistroInspecaoPMOBase):
    pass


class RegistroInspecaoPMOResponse(RegistroInspecaoPMOBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criado_em: datetime


# Aliases
PreventiveMaintenanceItemResponse = ItemPreventivaPMOResponse
InspectionRecordResponse = RegistroInspecaoPMOResponse
