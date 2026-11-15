import uuid
from datetime import datetime, timezone

from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UsuarioLogin(BaseModel):
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
    def validate_has_senha(self) -> 'UsuarioLogin':
        if not self.senha:
            raise ValueError('A senha é obrigatória.')
        return self


class UsuarioBase(BaseModel):
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    model_config = ConfigDict(populate_by_name=True)

    senha: str | None = None
    pessoa_id: uuid.UUID | None = None
    google_sub: str | None = None
    papel_sistema: str | None = None
    papel: str | None = None
    nome_completo: str | None = None
    condominio_id: uuid.UUID | None = None

    @model_validator(mode='before')
    @classmethod
    def harmonize_create(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'nome' in data and not data.get('nome_completo'):
                data['nome_completo'] = data['nome']
            if 'papel' in data and not data.get('papel_sistema'):
                data['papel_sistema'] = data['papel']
            if 'roles' in data and isinstance(data['roles'], list) and data['roles'] and not data.get('papel_sistema'):
                data['papel_sistema'] = data['roles'][0]
            if 'papeis' in data and isinstance(data['papeis'], list) and data['papeis'] and not data.get('papel_sistema'):
                data['papel_sistema'] = data['papeis'][0]
        return data


class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None = None
    senha: str | None = None
    pessoa_id: uuid.UUID | None = None
    nome_completo: str | None = None
    papel_sistema: str | None = None
    papel: str | None = None
    status: str | None = None
    ativo: bool | None = None
    condominio_id: uuid.UUID | None = None

    @model_validator(mode='before')
    @classmethod
    def harmonize_update(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'nome' in data and not data.get('nome_completo'):
                data['nome_completo'] = data['nome']
            if 'papel' in data and not data.get('papel_sistema'):
                data['papel_sistema'] = data['papel']
            if 'roles' in data and isinstance(data['roles'], list) and data['roles'] and not data.get('papel_sistema'):
                data['papel_sistema'] = data['roles'][0]
            if 'papeis' in data and isinstance(data['papeis'], list) and data['papeis'] and not data.get('papel_sistema'):
                data['papel_sistema'] = data['papeis'][0]
            if 'ativo' in data and 'status' not in data:
                data['status'] = 'ATIVO' if data['ativo'] else 'INATIVO'
        return data


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    pessoa_id: uuid.UUID | None = None
    email_verificado: bool = False
    status: str = 'ATIVO'
    ultimo_acesso_em: datetime | None = None
    criado_em: datetime | None = None
    nome_completo: str | None = None
    nome: str | None = None
    ativo: bool = True
    papeis: list[str] = []
    roles: list[str] = []
    condominio_id: uuid.UUID | None = None


class MembroCondominioCreate(BaseModel):
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID
    tipo_pessoa: str = 'MORADOR'


class MembroCondominioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    pessoa_id: uuid.UUID
    tipo_pessoa: str
    status: str
    entrou_em: datetime
    saiu_em: datetime | None = None


class OcupacaoUnidadeCreate(BaseModel):
    condominio_id: uuid.UUID | None = None
    unidade_id: uuid.UUID
    pessoa_id: uuid.UUID
    tipo_vinculo: str = 'MORADOR'
    mora_no_local: bool = True
    principal: bool = False
    responsavel_ocupacao_id: uuid.UUID | None = None
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    data_inicio: datetime | None = None
    data_fim: datetime | None = None

    @model_validator(mode='before')
    @classmethod
    def preparar_datas_e_vinculo(cls, data: any) -> any:
        if isinstance(data, dict):
            # Compatibilidade de aliases data_inicio -> inicio_em e data_fim -> fim_em
            if 'data_inicio' in data and data['data_inicio'] is not None and not data.get('inicio_em'):
                data['inicio_em'] = data['data_inicio']
            if 'data_fim' in data and data['data_fim'] is not None and not data.get('fim_em'):
                data['fim_em'] = data['data_fim']
            if 'tipo_vinculo' in data and isinstance(data['tipo_vinculo'], str):
                data['tipo_vinculo'] = data['tipo_vinculo'].upper()
        return data

    @model_validator(mode='after')
    def validar_regras_temporais(self) -> 'OcupacaoUnidadeCreate':
        # Se inicio_em for omitido e não for temporário, padrão é agora
        if self.inicio_em is None and self.tipo_vinculo not in ('TEMPORARIO', 'HOSPEDE'):
            self.inicio_em = datetime.now(timezone.utc)

        # Regra 2: Curtos prazos exigem inicio_em e fim_em
        if self.tipo_vinculo in ('TEMPORARIO', 'HOSPEDE'):
            if not self.inicio_em or not self.fim_em:
                raise ValueError(
                    'DATAS_OBRIGATORIAS_CURTO_PRAZO: Para vínculos TEMPORARIO ou HOSPEDE, as datas de início e fim são obrigatórias.'
                )

        # Regra 3: Validação de retroatividade (fim_em > inicio_em)
        if self.inicio_em and self.fim_em and self.fim_em <= self.inicio_em:
            raise ValueError(
                'DATA_FIM_DEVE_SER_MAIOR_QUE_INICIO: A data_fim deve ser estritamente maior que a data_inicio.'
            )

        return self


class OcupacaoUnidadeUpdate(BaseModel):
    unidade_id: uuid.UUID | None = None
    tipo_vinculo: str | None = None
    mora_no_local: bool | None = None
    principal: bool | None = None
    responsavel_ocupacao_id: uuid.UUID | None = None
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    status: str | None = None

    @model_validator(mode='before')
    @classmethod
    def preparar_dados(cls, data: any) -> any:
        if isinstance(data, dict) and 'tipo_vinculo' in data and isinstance(data['tipo_vinculo'], str):
            data['tipo_vinculo'] = data['tipo_vinculo'].upper()
        return data

    @model_validator(mode='after')
    def validar_datas(self) -> 'OcupacaoUnidadeUpdate':
        if self.inicio_em and self.fim_em and self.fim_em <= self.inicio_em:
            raise ValueError(
                'DATA_FIM_DEVE_SER_MAIOR_QUE_INICIO: A data_fim deve ser estritamente maior que a data_inicio.'
            )
        return self


class InativarOcupacaoRequest(BaseModel):
    cascade_dependentes: bool = True
    novo_responsavel_ocupacao_id: uuid.UUID | None = None


class RotinaExpiracaoResponse(BaseModel):
    ocupacoes_inativadas: int
    dependentes_inativados: int


class OcupacaoUnidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condominio_id: uuid.UUID
    unidade_id: uuid.UUID
    pessoa_id: uuid.UUID
    tipo_vinculo: str
    mora_no_local: bool
    principal: bool
    responsavel_ocupacao_id: uuid.UUID | None = None
    inicio_em: datetime
    fim_em: datetime | None = None
    status: str
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None


# Aliases de retrocompatibilidade
UserBase = UsuarioBase
UserCreate = UsuarioCreate
UserResponse = UsuarioResponse
UserLogin = UsuarioLogin
