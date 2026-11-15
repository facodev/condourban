import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Uuid,
    func,
)

from app.core.database import Base


class VagaGaragem(Base):
    __tablename__ = 'vaga_garagem'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    identificacao = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=True)
    coberta = Column(Boolean, default=False, nullable=False)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

