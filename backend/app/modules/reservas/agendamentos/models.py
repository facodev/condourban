import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reserva(Base):
    __tablename__ = 'reserva'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    area_comum_id = Column(Uuid, ForeignKey('area_comum.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    solicitante_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    inicio_em = Column(DateTime(timezone=True), nullable=False)
    fim_em = Column(DateTime(timezone=True), nullable=False)
    valor = Column(Numeric(12, 2), nullable=True)
    termo_aceito = Column(Boolean, nullable=False, default=True)
    status = Column(String(50), nullable=False, default='SOLICITADA')
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    convidados = relationship('ConvidadoReserva', back_populates='reserva', cascade='all, delete-orphan', lazy='selectin')
    vistorias = relationship('VistoriaReserva', back_populates='reserva', lazy='selectin')

    # Retrocompatibilidade
    @property
    def usuario_id(self):
        return self.solicitante_id


class ConvidadoReserva(Base):
    __tablename__ = 'convidado_reserva'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    reserva_id = Column(Uuid, ForeignKey('reserva.id', ondelete='CASCADE'), nullable=False, index=True)
    nome_completo = Column(String(200), nullable=False)
    documento = Column(String(30), nullable=True)
    presente = Column(Boolean, nullable=False, default=False)
    horario_entrada = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    reserva = relationship('Reserva', back_populates='convidados')


# Aliases de retrocompatibilidade
Reservation = Reserva
GuestReservation = ConvidadoReserva
