import uuid
from sqlalchemy import Column, DateTime, ForeignKey, JSON, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class VistoriaReserva(Base):
    __tablename__ = 'vistoria_reserva'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    reserva_id = Column(Uuid, ForeignKey('reserva.id'), nullable=False, index=True)
    vistoriador_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)  # 'ENTRADA' | 'SAIDA'
    checklist = Column(JSON, nullable=False, default=dict)
    avarias_detectadas = Column(Text, nullable=True)
    fotos = Column(JSON, nullable=False, default=list)
    valor_caucao_retido = Column(Numeric(12, 2), default=0.00)
    concluida_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    reserva = relationship('Reserva', back_populates='vistorias')
