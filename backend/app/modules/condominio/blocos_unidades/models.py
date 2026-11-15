import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Uuid,
    func,
)

from app.core.database import Base


class Bloco(Base):
    __tablename__ = 'bloco'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=True)
    ordem = Column(Integer, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Unidade(Base):
    __tablename__ = 'unidade'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    bloco_id = Column(Uuid, ForeignKey('bloco.id'), nullable=True, index=True)
    identificacao = Column(String(50), nullable=False)
    andar = Column(Integer, nullable=True)
    tipo = Column(String(50), nullable=True)
    descricao = Column(String(500), nullable=True)
    area_privativa = Column(Numeric(12, 2), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# Aliases
Block = Bloco
Unit = Unidade

