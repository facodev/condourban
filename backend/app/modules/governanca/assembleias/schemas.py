from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
from pydantic import BaseModel, ConfigDict, Field


class OpcaoVotacaoBase(BaseModel):
    descricao: str = Field(..., max_length=200)


class OpcaoVotacaoCreate(OpcaoVotacaoBase):
    pass


class OpcaoVotacaoResponse(OpcaoVotacaoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    votacao_id: uuid.UUID


class VotoAssembleiaCreate(BaseModel):
    opcao_id: uuid.UUID
    unidade_id: uuid.UUID | None = None
    peso: Decimal = Decimal('1.0')


class VotoAssembleiaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    votacao_id: uuid.UUID
    pessoa_id: uuid.UUID
    unidade_id: uuid.UUID | None = None
    opcao_id: uuid.UUID
    peso: Decimal
    votado_em: datetime
    hash_auditoria: str | None = None


class VotacaoAssembleiaBase(BaseModel):
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    quorum_necessario: Decimal | None = None
    status: str = 'AGUARDANDO'


class VotacaoAssembleiaCreate(VotacaoAssembleiaBase):
    opcoes: list[OpcaoVotacaoCreate] = []


class VotacaoAssembleiaResponse(VotacaoAssembleiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    pauta_id: uuid.UUID
    opcoes: list[OpcaoVotacaoResponse] = []


class PautaAssembleiaBase(BaseModel):
    titulo: str = Field(..., max_length=300)
    descricao: str | None = None
    ordem: int


class PautaAssembleiaCreate(PautaAssembleiaBase):
    votacao: VotacaoAssembleiaCreate | None = None


class PautaAssembleiaResponse(PautaAssembleiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    assembleia_id: uuid.UUID
    votacoes: list[VotacaoAssembleiaResponse] = []


class ParticipanteAssembleiaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    assembleia_id: uuid.UUID
    pessoa_id: uuid.UUID
    unidade_id: uuid.UUID | None = None
    entrou_em: datetime | None = None
    saiu_em: datetime | None = None
    presente: bool = False


class ProcuracaoAssembleiaBase(BaseModel):
    outorgante_id: uuid.UUID
    outorgado_id: uuid.UUID
    unidade_id: uuid.UUID
    chave_documento: str | None = None


class ProcuracaoAssembleiaCreate(ProcuracaoAssembleiaBase):
    pass


class ProcuracaoAssembleiaResponse(ProcuracaoAssembleiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    assembleia_id: uuid.UUID
    validada_por: uuid.UUID | None = None
    status: str
    criada_em: datetime


class AtaAssembleiaBase(BaseModel):
    texto_ata: str
    chave_documento_assinado: str | None = None
    aprovada: bool = False
    registrada_em: datetime | None = None


class AtaAssembleiaCreate(AtaAssembleiaBase):
    pass


class AtaAssembleiaResponse(AtaAssembleiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    assembleia_id: uuid.UUID
    redigida_por: uuid.UUID | None = None
    criada_em: datetime


class AssembleiaBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    tipo: str | None = Field('ORDINARIA', description="'ORDINARIA' ou 'EXTRAORDINARIA'")
    inicio_em: datetime
    fim_em: datetime | None = None
    status: str = 'AGENDADA'
    link_videochamada: str | None = None
    regra_quorum: dict[str, Any] = Field(default_factory=dict)


class AssembleiaCreate(AssembleiaBase):
    pautas: list[PautaAssembleiaCreate] = []


class AssembleiaUpdate(BaseModel):
    titulo: str | None = None
    tipo: str | None = None
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    status: str | None = None
    link_videochamada: str | None = None
    regra_quorum: dict[str, Any] | None = None


class AssembleiaResponse(AssembleiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    criada_por: uuid.UUID | None = None
    criada_em: datetime
    pautas: list[PautaAssembleiaResponse] = []
    atas: list[AtaAssembleiaResponse] = []


# Aliases
AssemblyResponse = AssembleiaResponse
