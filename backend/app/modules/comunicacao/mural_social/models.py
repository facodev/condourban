import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Enquete(Base):
    __tablename__ = 'enquete'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    inicio_em = Column(DateTime(timezone=True), nullable=False)
    fim_em = Column(DateTime(timezone=True), nullable=False)
    anonima = Column(Boolean, nullable=False, default=False)
    status = Column(String(30), nullable=False, default='RASCUNHO')
    criada_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    opcoes = relationship('OpcaoEnquete', back_populates='enquete', cascade='all, delete-orphan')
    votos = relationship('VotoEnquete', back_populates='enquete', cascade='all, delete-orphan')


class OpcaoEnquete(Base):
    __tablename__ = 'opcao_enquete'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    enquete_id = Column(Uuid, ForeignKey('enquete.id', ondelete='CASCADE'), nullable=False, index=True)
    descricao = Column(String(300), nullable=False)
    ordem = Column(Integer, nullable=False)

    enquete = relationship('Enquete', back_populates='opcoes')
    votos = relationship('VotoEnquete', back_populates='opcao', cascade='all, delete-orphan')


class VotoEnquete(Base):
    __tablename__ = 'voto_enquete'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    enquete_id = Column(Uuid, ForeignKey('enquete.id', ondelete='CASCADE'), nullable=False, index=True)
    opcao_id = Column(Uuid, ForeignKey('opcao_enquete.id', ondelete='CASCADE'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    votado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('enquete_id', 'pessoa_id', name='uq_voto_enquete_pessoa'),
    )

    enquete = relationship('Enquete', back_populates='votos')
    opcao = relationship('OpcaoEnquete', back_populates='votos')


class ItemComunidade(Base):
    __tablename__ = 'item_comunidade'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    autor_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    tipo = Column(String(30), nullable=False, default='CLASSIFICADO')  # 'CLASSIFICADO', 'AVISO', 'RECOMENDACAO'
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    preco = Column(Numeric(12, 2), nullable=True)
    contato = Column(String(100), nullable=True)
    foto_url = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default='ATIVO')
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expira_em = Column(DateTime(timezone=True), nullable=True)


# Aliases de retrocompatibilidade
Poll = Enquete
PollOption = OpcaoEnquete
PollVote = VotoEnquete
CommunityItem = ItemComunidade
