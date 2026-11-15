import re
import uuid
from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator

from app.core.validacoes import validar_cpf, validar_telefone


class TelefoneItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    numero: str
    tipo: Literal['celular', 'residencial', 'comercial'] = 'celular'
    principal: bool = False
    whatsapp: bool = False

    @field_validator('numero')
    @classmethod
    def validar_numero_telefone(cls, v: str) -> str:
        digits = re.sub(r'\D', '', str(v))
        if not validar_telefone(digits):
            raise ValueError('TELEFONE_INVALIDO: O telefone deve ser válido com DDD e 10 ou 11 dígitos.')
        return digits


class PessoaBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome_completo: str = 'Morador'
    nome: str | None = None
    cpf: str | None = None
    nome_social: str | None = None
    email: EmailStr | None = None
    celular: str | None = None
    telefones: list[TelefoneItem] = []
    data_nascimento: date | None = None
    sexo: str | None = None
    foto_url: str | None = None



    @field_validator('telefones')
    @classmethod
    def validar_telefones_unicidade(cls, v: list[TelefoneItem]) -> list[TelefoneItem]:
        if not v:
            return []
        tipos = [item.tipo for item in v]
        if len(tipos) != len(set(tipos)):
            raise ValueError(
                'TIPO_TELEFONE_DUPLICADO: Permitido cadastrar somente um telefone por tipo (celular, residencial, comercial).'
            )
        principais = [item for item in v if item.principal]
        if len(principais) > 1:
            raise ValueError('APENAS_UM_TELEFONE_PRINCIPAL: Apenas um telefone pode ser marcado como principal.')
        if not principais and v:
            v[0].principal = True
        return v

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('nome_completo') and data.get('nome'):
                data['nome_completo'] = data['nome']
            if not data.get('nome') and data.get('nome_completo'):
                data['nome'] = data['nome_completo']
            if not data.get('celular') and data.get('telefone'):
                data['celular'] = data['telefone']

            # Se vier celular mas não vier lista de telefones, sincroniza
            if data.get('celular') and not data.get('telefones'):
                digits = re.sub(r'\D', '', str(data['celular']))
                if validar_telefone(digits):
                    data['telefones'] = [{
                        'numero': digits,
                        'tipo': 'celular',
                        'principal': True,
                        'whatsapp': True
                    }]
        return data


class PessoaCreate(PessoaBase):
    inquilino_id: uuid.UUID | None = None
    cpf: str | None = None
    usuario_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None
    tipo_vinculo: str | None = None

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: str | None) -> str | None:
        if not v:
            return None
        v_limpo = re.sub(r'\D', '', str(v))
        if not v_limpo:
            return None
        if not validar_cpf(v_limpo):
            raise ValueError('CPF_INVALIDO: O CPF informado não é válido.')
        return v_limpo


class PessoaUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome_completo: str | None = None
    nome_social: str | None = None
    email: EmailStr | None = None
    celular: str | None = None
    telefones: list[TelefoneItem] | None = None
    cpf: str | None = None
    foto_url: str | None = None
    status: str | None = None



    @field_validator('telefones')
    @classmethod
    def validar_telefones_unicidade(cls, v: list[TelefoneItem] | None) -> list[TelefoneItem] | None:
        if v is None:
            return None
        if not v:
            return []
        tipos = [item.tipo for item in v]
        if len(tipos) != len(set(tipos)):
            raise ValueError(
                'TIPO_TELEFONE_DUPLICADO: Permitido cadastrar somente um telefone por tipo (celular, residencial, comercial).'
            )
        principais = [item for item in v if item.principal]
        if len(principais) > 1:
            raise ValueError('APENAS_UM_TELEFONE_PRINCIPAL: Apenas um telefone pode ser marcado como principal.')
        if not principais and v:
            v[0].principal = True
        return v

    @model_validator(mode='before')
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('nome_completo') and data.get('nome'):
                data['nome_completo'] = data['nome']
            if not data.get('celular') and data.get('telefone'):
                data['celular'] = data['telefone']
            if data.get('celular') and not data.get('telefones'):
                digits = re.sub(r'\D', '', str(data['celular']))
                if validar_telefone(digits):
                    data['telefones'] = [{
                        'numero': digits,
                        'tipo': 'celular',
                        'principal': True,
                        'whatsapp': True
                    }]
        return data


class PessoaResponse(PessoaBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    inquilino_id: uuid.UUID | None = None
    cpf: str | None = None
    nome: str | None = None
    nomeCompleto: str | None = None
    status: str = 'ATIVO'
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None
    usuario_id: uuid.UUID | None = None
    unidade_id: uuid.UUID | None = None
    tipo_vinculo: str | None = None

    @model_validator(mode='after')
    def preencher_aliases_saida(self) -> 'PessoaResponse':
        if not self.nome and self.nome_completo:
            self.nome = self.nome_completo
        if not self.nomeCompleto and self.nome_completo:
            self.nomeCompleto = self.nome_completo

        # Sincronização retrocompatível de celular <-> telefones
        if not self.telefones and self.celular:
            digits = re.sub(r'\D', '', str(self.celular))
            if digits:
                self.telefones = [
                    TelefoneItem(
                        numero=digits,
                        tipo='celular',
                        principal=True,
                        whatsapp=True
                    )
                ]
        elif self.telefones and not self.celular:
            p = next((t for t in self.telefones if t.principal), self.telefones[0])
            self.celular = p.numero
        return self


class DocumentoIdentificacaoBase(BaseModel):
    tipo: str
    numero: str | None = None
    orgao_emissor: str | None = None
    uf: str | None = None
    data_emissao: date | None = None


class DocumentoIdentificacaoCreate(DocumentoIdentificacaoBase):
    pessoa_id: uuid.UUID


class DocumentoIdentificacaoResponse(DocumentoIdentificacaoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    pessoa_id: uuid.UUID
    criado_em: datetime


# Aliases de retrocompatibilidade
ResidentBase = PessoaBase
ResidentCreate = PessoaCreate
ResidentResponse = PessoaResponse
ResidenteBase = PessoaBase
ResidenteCreate = PessoaCreate
ResidenteResponse = PessoaResponse
