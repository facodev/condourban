from datetime import date
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ItemPreventivaPMO(Base):
    __tablename__ = 'item_preventiva_pmo'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    sistema = Column(String(100), nullable=False)  # 'ELEVADORES', 'BOMBAS', 'GERADOR', 'SPDA_PARA_RAIOS', 'PORTOES', 'EXTINTORES'
    descricao = Column(String(300), nullable=False)
    periodicidade_dias = Column(Integer, nullable=False)
    instrucao_tecnica = Column(Text, nullable=True)
    proxima_inspecao = Column(Date, nullable=False, index=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    inspecoes = relationship('RegistroInspecaoPMO', back_populates='item_pmo', cascade='all, delete-orphan')


class RegistroInspecaoPMO(Base):
    __tablename__ = 'registro_inspecao_pmo'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    item_preventiva_pmo_id = Column(Uuid, ForeignKey('item_preventiva_pmo.id', ondelete='CASCADE'), nullable=False, index=True)
    inspecionado_em = Column(Date, nullable=False)
    responsavel_tecnico = Column(String(200), nullable=False)
    registro_profissional = Column(String(50), nullable=True)  # CREA, CFT
    conforme = Column(Boolean, nullable=False, default=True)
    parecer_tecnico = Column(Text, nullable=True)
    chave_art_laudo = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    item_pmo = relationship('ItemPreventivaPMO', back_populates='inspecoes')


# Aliases
PreventiveMaintenanceItem = ItemPreventivaPMO
InspectionRecord = RegistroInspecaoPMO
