from datetime import date
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)

from app.core.database import Base


class DespesaCondominial(Base):
    __tablename__ = 'despesa_condominial'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    categoria = Column(String(100), nullable=False)
    fornecedor = Column(String(200), nullable=False)
    cnpj_cpf_fornecedor = Column(String(30), nullable=True)
    descricao = Column(Text, nullable=False)
    valor = Column(Numeric(14, 2), nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    chave_comprovante = Column(Text, nullable=True)
    aprovada_conselho = Column(Boolean, nullable=False, default=False)
    status = Column(String(30), nullable=False, default='PENDENTE')  # 'PENDENTE', 'PAGO', 'CANCELADO'
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class MedicaoIndividual(Base):
    __tablename__ = 'medicao_individual'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    tipo_consumo = Column(String(30), nullable=False)  # 'AGUA_FRIA', 'AGUA_QUENTE', 'GAS', 'ENERGIA'
    competencia = Column(Date, nullable=False)
    leitura_anterior = Column(Numeric(12, 3), nullable=False)
    leitura_atual = Column(Numeric(12, 3), nullable=False)
    consumo = Column(Numeric(12, 3), nullable=False)
    valor_calculado = Column(Numeric(12, 2), nullable=False)
    foto_medidor_url = Column(Text, nullable=True)
    lancado_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('unidade_id', 'tipo_consumo', 'competencia', name='uq_medicao_unidade_tipo_comp'),
    )


# Aliases
CondoExpense = DespesaCondominial
IndividualMeasurement = MedicaoIndividual
