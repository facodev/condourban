import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comunicado(Base):
    __tablename__ = 'comunicado'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    conteudo = Column(Text, nullable=False)
    autor_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    urgente = Column(Boolean, nullable=False, default=False)
    fixado = Column(Boolean, nullable=False, default=False)
    publicado_em = Column(DateTime(timezone=True), nullable=True)
    expira_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), nullable=False, default='RASCUNHO')
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    leituras = relationship('LeituraComunicado', back_populates='comunicado', cascade='all, delete-orphan')


class LeituraComunicado(Base):
    __tablename__ = 'leitura_comunicado'
    __table_args__ = (
        UniqueConstraint('comunicado_id', 'pessoa_id', name='uq_leitura_comunicado_pessoa'),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    comunicado_id = Column(Uuid, ForeignKey('comunicado.id', ondelete='CASCADE'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    lido_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    comunicado = relationship('Comunicado', back_populates='leituras')


class MensagemFaleConosco(Base):
    __tablename__ = 'mensagem_fale_conosco'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    remetente_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    destinatario_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    assunto = Column(String(200), nullable=False)
    mensagem = Column(Text, nullable=False)
    sla_horas = Column(Integer, nullable=False, default=48)
    prazo_sla = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), nullable=False, default='NOVA_MENSAGEM')
    lida_em = Column(DateTime(timezone=True), nullable=True)
    enviada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# Aliases de retrocompatibilidade
Notice = Comunicado
NoticeRead = LeituraComunicado
ContactMessage = MensagemFaleConosco

