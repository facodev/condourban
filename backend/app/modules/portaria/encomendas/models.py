import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class Encomenda(Base):
    __tablename__ = 'encomenda'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    destinatario_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True)
    transportadora = Column(String(150), nullable=True)
    codigo_rastreio = Column(String(100), nullable=True)
    descricao = Column(String(500), nullable=True)
    local_armazenamento = Column(String(100), nullable=True)
    foto_url = Column(Text, nullable=True)
    codigo_retirada = Column(String(20), nullable=True)
    recebida_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recebida_por = Column(Uuid, nullable=True)
    retirada_em = Column(DateTime(timezone=True), nullable=True)
    retirada_por = Column(Uuid, nullable=True)
    status = Column(String(50), default='RECEBIDA', nullable=False)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class EventoEncomenda(Base):
    __tablename__ = 'evento_encomenda'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    encomenda_id = Column(Uuid, ForeignKey('encomenda.id', ondelete='CASCADE'), nullable=False, index=True)
    tipo_evento = Column(String(50), nullable=False)
    pessoa_id = Column(Uuid, nullable=True)
    ocorrido_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    observacao = Column(Text, nullable=True)


# Alias
Delivery = Encomenda
