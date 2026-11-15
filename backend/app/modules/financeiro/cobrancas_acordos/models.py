from datetime import date
import uuid
from sqlalchemy import (
    Column,
    Date,
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

from app.core.database import Base


class CobrancaCondominial(Base):
    __tablename__ = 'cobranca_condominial'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    competencia = Column(Date, nullable=False)
    vencimento = Column(Date, nullable=False)
    valor = Column(Numeric(14, 2), nullable=False)
    valor_multa = Column(Numeric(12, 2), default=0.00)
    valor_juros = Column(Numeric(12, 2), default=0.00)
    valor_desconto = Column(Numeric(12, 2), default=0.00)
    status = Column(String(30), nullable=False, default='PENDENTE')  # 'PENDENTE', 'PAGO', 'VENCIDO', 'CANCELADO', 'EM_ACORDO'
    provedor_pagamento = Column(String(50), nullable=True)
    identificacao_externa = Column(String(200), nullable=True)
    linha_digitavel = Column(String(100), nullable=True)
    codigo_pix = Column(Text, nullable=True)
    pago_em = Column(DateTime(timezone=True), nullable=True)
    valor_pago = Column(Numeric(14, 2), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('unidade_id', 'competencia', name='uq_cobranca_unidade_competencia'),
    )


class TermoAcordo(Base):
    __tablename__ = 'termo_acordo'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    devedor_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    valor_total_original = Column(Numeric(14, 2), nullable=False)
    valor_total_negociado = Column(Numeric(14, 2), nullable=False)
    numero_parcelas = Column(Integer, nullable=False)
    dia_vencimento_parcelas = Column(Integer, nullable=False, default=10)
    status = Column(String(30), nullable=False, default='ATIVO')  # 'ATIVO', 'QUITADO', 'INADIMPLIDO', 'CANCELADO'
    observacao = Column(Text, nullable=True)
    assinado_em = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# Aliases
CondoCharge = CobrancaCondominial
SettlementAgreement = TermoAcordo
