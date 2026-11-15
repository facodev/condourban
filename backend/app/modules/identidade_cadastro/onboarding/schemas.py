import uuid
from datetime import datetime

from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ConviteCadastroCreate(BaseModel):
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    tipo_vinculo: str = 'MORADOR'
    dias_validade: int = 7


class ConviteCadastroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    tipo_vinculo: str
    codigo: str | None = None
    validade_em: datetime
    status: str


class ConviteEnvioRequest(BaseModel):
    unidade_id: uuid.UUID
    nome_completo: str = 'Morador Convidado'
    email: str
    tipo_vinculo: str = 'MORADOR'
    condominio_id: uuid.UUID | None = None


class ConviteEnvioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    convite_id: uuid.UUID
    token: str
    expira_em: datetime
    unidade_id: uuid.UUID


class SolicitacaoCadastroCreate(BaseModel):
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    convite_id: uuid.UUID | None = None
    tipo_vinculo: str = 'MORADOR'


class SolicitacaoIngressoRequest(BaseModel):
    unidade_id: uuid.UUID
    nome_completo: str
    email: str
    celular: str | None = None
    tipo_vinculo: str = 'MORADOR'
    condominio_id: uuid.UUID | None = None
    convite_id: uuid.UUID | None = None


class SolicitacaoCadastroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    tipo_vinculo: str
    status: str
    etapa_atual: str | None = None
    criada_em: datetime
    enviada_em: datetime | None = None


class AprovarSolicitacaoRequest(BaseModel):
    observacao: str | None = None


class RejeitarSolicitacaoRequest(BaseModel):
    motivo_rejeicao: str | None = None
    motivo: str | None = None

    @model_validator(mode='before')
    @classmethod
    def map_motivo(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('motivo_rejeicao') and data.get('motivo'):
                data['motivo_rejeicao'] = data['motivo']
        return data

    @field_validator('motivo_rejeicao')
    @classmethod
    def validar_motivo(cls, v: str | None) -> str:
        if not v or not v.strip():
            raise ValueError('O motivo da rejeição é obrigatório e não pode ser vazio.')
        return v.strip()


class SolicitacaoAprovacaoResponse(BaseModel):
    solicitacao_id: uuid.UUID
    status: str
    aprovado_em: datetime
    ocupacao_id: uuid.UUID | None = None


class SolicitacaoRejeicaoResponse(BaseModel):
    solicitacao_id: uuid.UUID
    status: str
    rejeitado_em: datetime
    motivo_rejeicao: str


class VerificarCpfOnboardingRequest(BaseModel):
    cpf: str
    condominio_id: uuid.UUID


class VerificarCpfOnboardingResponse(BaseModel):
    status: str  # NOVO_CADASTRO ou EXISTENTE_CONFIRMACAO_PENDENTE
    existe: bool
    email_ofuscado: str | None = None
    mensagem: str
    token_temporario: str | None = None


class ConfirmarMagicLinkRequest(BaseModel):
    token: str


class ConfirmarMagicLinkResponse(BaseModel):
    sucesso: bool
    pessoa_id: uuid.UUID
    nome_completo: str
    email: str
    celular: str | None = None
    mensagem: str


class RevogarVinculoRequest(BaseModel):
    token: str


class RevogarVinculoResponse(BaseModel):
    sucesso: bool
    mensagem: str
    revogado_em: datetime
