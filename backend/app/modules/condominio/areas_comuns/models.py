import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    Time,
    Uuid,
    func,
)

from app.core.database import Base


class AreaComum(Base):
    __tablename__ = 'area_comum'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    capacidade = Column(Integer, default=0, nullable=False)
    requer_aprovacao = Column(Boolean, default=False, nullable=False)
    taxa_reserva = Column(Numeric(12, 2), default=0.00, nullable=True)
    valor_caucao = Column(Numeric(12, 2), default=0.00, nullable=True)
    horario_abertura = Column(String(10), default='08:00', nullable=False)
    horario_fechamento = Column(String(10), default='22:00', nullable=False)
    regras_dias = Column(JSON, default=dict, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Propriedades de compatibilidade
    @property
    def status(self) -> str:
        return 'ATIVO' if self.ativo else 'INATIVO'

    @property
    def valor_reserva(self):
        return self.taxa_reserva


# Alias de retrocompatibilidade
CommonArea = AreaComum
