from datetime import date
import uuid
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChamadoManutencao(Base):
    __tablename__ = 'chamado_manutencao'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    solicitante_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    categoria = Column(String(50), nullable=False)  # 'ELETRICA', 'HIDRAULICA', 'CIVIL', 'ELEVADORES', 'PINTURA', 'OUTRO'
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    localizacao = Column(String(200), nullable=True)
    foto_url = Column(Text, nullable=True)
    prioridade = Column(String(30), nullable=False, default='MEDIA')  # 'BAIXA', 'MEDIA', 'ALTA', 'URGENTE'
    status = Column(String(30), nullable=False, default='ABERTO')  # 'ABERTO', 'EM_ANDAMENTO', 'CONCLUIDO', 'CANCELADO'
    atribuido_a = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    concluido_em = Column(DateTime(timezone=True), nullable=True)

    ordens_servico = relationship('OrdemServico', back_populates='chamado')


class OrdemServico(Base):
    __tablename__ = 'ordem_servico'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    chamado_id = Column(Uuid, ForeignKey('chamado_manutencao.id'), nullable=True, index=True)
    prestador_id = Column(Uuid, ForeignKey('prestador.id'), nullable=True, index=True)
    responsavel_interno_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    descricao = Column(Text, nullable=False)
    valor_estimado = Column(Numeric(12, 2), nullable=True)
    valor_final = Column(Numeric(12, 2), nullable=True)
    data_agendada = Column(Date, nullable=True)
    status = Column(String(30), nullable=False, default='RASCUNHO')  # 'RASCUNHO', 'AGENDADA', 'EM_EXECUCAO', 'CONCLUIDA', 'CANCELADA'
    laudo_conclusao = Column(Text, nullable=True)
    iniciado_em = Column(DateTime(timezone=True), nullable=True)
    finalizado_em = Column(DateTime(timezone=True), nullable=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizada_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    chamado = relationship('ChamadoManutencao', back_populates='ordens_servico')


# Aliases
MaintenanceTicket = ChamadoManutencao
WorkOrder = OrdemServico
