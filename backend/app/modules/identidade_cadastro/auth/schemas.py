import uuid
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    senha: str | None = None
    password: str | None = None

    @model_validator(mode='before')
    @classmethod
    def set_senha(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('senha') and data.get('password'):
                data['senha'] = data['password']
        return data

    @model_validator(mode='after')
    def validate_has_senha(self) -> 'LoginRequest':
        if not self.senha:
            raise ValueError('A senha é obrigatória.')
        return self


class GoogleLoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_token: str


class SelecionarCondominioRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    condominio_id: uuid.UUID


class CondominioVinculado(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nome: str
    papel: str


class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_tipo: str = 'bearer'
    condominios: list[CondominioVinculado] = []
    condominio_ativo: uuid.UUID | None = None
    pessoa_id: uuid.UUID | None = None
    unidade_ids: list[uuid.UUID] = []
