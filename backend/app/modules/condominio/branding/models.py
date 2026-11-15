import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    JSON,
    String,
    Uuid,
    func,
)

from app.core.database import Base


class Inquilino(Base):
    __tablename__ = 'inquilino'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    nome = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200), nullable=True)
    documento = Column(String(30), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Condominio(Base):
    __tablename__ = 'condominio'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    inquilino_id = Column(Uuid, ForeignKey('inquilino.id'), nullable=False, index=True)
    razao_social = Column(String(200), nullable=True)
    nome = Column(String(200), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    cep = Column(String(9), nullable=True)
    logradouro = Column(String(200), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    fuso_horario = Column(String(50), default='America/Sao_Paulo', nullable=False)
    configuracoes = Column(JSON, default=dict, nullable=False)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

