import uuid
from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, JSON, String, Text, Uuid, func

from app.core.database import Base


class Pessoa(Base):
    __tablename__ = 'pessoa'
    __allow_unmapped__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    inquilino_id = Column(Uuid, default=uuid.uuid4, nullable=False)
    nome_completo = Column(String(200), nullable=False, index=True)
    nome_social = Column(String(200), nullable=True)
    cpf_hash = Column(String(64), nullable=True, index=True)
    cpf_criptografado = Column(Text, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(30), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    celular = Column(String(30), nullable=True)
    telefones = Column(JSON, default=list, nullable=True)
    foto_url = Column(Text, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    excluido_em = Column(DateTime(timezone=True), nullable=True)

    # Campos transientes para compatibilidade
    usuario_id = None
    unidade_id = None
    tipo_vinculo = None
    _cpf_transiente = None

    @property
    def nome(self) -> str:
        return self.nome_completo or ''

    @property
    def cpf(self) -> str | None:
        if self._cpf_transiente:
            return self._cpf_transiente
        if self.cpf_criptografado:
            import base64
            try:
                return base64.b64decode(self.cpf_criptografado.encode('utf-8')).decode('utf-8')
            except Exception:
                return None
        return None

    @cpf.setter
    def cpf(self, valor: str | None):
        self._cpf_transiente = valor


class DocumentoIdentificacao(Base):
    __tablename__ = 'documento_identificacao'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pessoa_id = Column(Uuid, nullable=False, index=True)
    tipo = Column(String(30), nullable=False)  # RG, CIN, CNH, PASSAPORTE
    numero = Column(String(50), nullable=True)
    orgao_emissor = Column(String(50), nullable=True)
    uf = Column(String(2), nullable=True)
    data_emissao = Column(Date, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# Aliases de retrocompatibilidade
Residente = Pessoa
Resident = Pessoa
