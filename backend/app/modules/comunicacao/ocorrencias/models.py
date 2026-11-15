import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ocorrencia(Base):
    __tablename__ = 'ocorrencia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    registrada_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    origem = Column(String(20), nullable=False, default='MORADOR')  # 'MORADOR', 'PORTARIA', 'GESTAO'
    categoria = Column(String(100), nullable=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    prioridade = Column(String(30), default='NORMAL')
    status = Column(String(30), nullable=False, default='ABERTA')  # 'ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'CANCELADA'
    sigilosa = Column(Boolean, nullable=False, default=False)
    responsavel_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolvida_em = Column(DateTime(timezone=True), nullable=True)

    historico = relationship('HistoricoOcorrencia', back_populates='ocorrencia', cascade='all, delete-orphan', lazy='selectin')

    # Compatibilidade com campo legado
    @property
    def usuario_id(self):
        return self.registrada_por

    @property
    def criado_em(self):
        return self.criada_em


class HistoricoOcorrencia(Base):
    __tablename__ = 'historico_ocorrencia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    ocorrencia_id = Column(Uuid, ForeignKey('ocorrencia.id', ondelete='CASCADE'), nullable=False, index=True)
    autor_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    mensagem = Column(Text, nullable=False)
    tipo = Column(String(30), default='COMENTARIO')  # 'COMENTARIO', 'MUDANCA_STATUS', 'PARECER'
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    ocorrencia = relationship('Ocorrencia', back_populates='historico')


# Aliases de retrocompatibilidade
Occurrence = Ocorrencia
OccurrenceHistory = HistoricoOcorrencia
