import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class CondominioInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    inquilino_id: uuid.UUID | None = None
    nome: str
    razao_social: str | None = None
    cnpj: str | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None
    fuso_horario: str = 'America/Sao_Paulo'
    configuracoes: dict = {}
    status: str = 'ATIVO'
    criado_em: datetime

    @computed_field
    @property
    def razaoSocial(self) -> str | None:
        return self.razao_social


class CondominioInfoUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome: str | None = None
    razao_social: str | None = None
    cnpj: str | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None

    @model_validator(mode='before')
    @classmethod
    def harmonize_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'razaoSocial' in data and not data.get('razao_social'):
                data['razao_social'] = data['razaoSocial']
        return data


class ConfiguracaoCondominioUpdate(BaseModel):
    branding: dict | None = None
    regras_operacionais: dict | None = None
    contato_administracao: dict | None = None

