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
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Assembleia(Base):
    __tablename__ = 'assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=True)  # 'ORDINARIA', 'EXTRAORDINARIA'
    inicio_em = Column(DateTime(timezone=True), nullable=False)
    fim_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), nullable=False, default='AGENDADA')  # 'AGENDADA', 'EM_ANDAMENTO', 'ENCERRADA', 'CANCELADA'
    link_videochamada = Column(String(500), nullable=True)
    regra_quorum = Column(JSON, nullable=False, default=dict)
    criada_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pautas = relationship('PautaAssembleia', back_populates='assembleia', cascade='all, delete-orphan')
    participantes = relationship('ParticipanteAssembleia', back_populates='assembleia', cascade='all, delete-orphan')
    procuracoes = relationship('ProcuracaoAssembleia', back_populates='assembleia', cascade='all, delete-orphan')
    atas = relationship('AtaAssembleia', back_populates='assembleia', cascade='all, delete-orphan')


class PautaAssembleia(Base):
    __tablename__ = 'pauta_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    assembleia_id = Column(Uuid, ForeignKey('assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    titulo = Column(String(300), nullable=False)
    descricao = Column(Text, nullable=True)
    ordem = Column(Integer, nullable=False)

    assembleia = relationship('Assembleia', back_populates='pautas')
    votacoes = relationship('VotacaoAssembleia', back_populates='pauta', cascade='all, delete-orphan')


class ParticipanteAssembleia(Base):
    __tablename__ = 'participante_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    assembleia_id = Column(Uuid, ForeignKey('assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    entrou_em = Column(DateTime(timezone=True), nullable=True)
    saiu_em = Column(DateTime(timezone=True), nullable=True)
    presente = Column(Boolean, nullable=False, default=False)

    assembleia = relationship('Assembleia', back_populates='participantes')


class ProcuracaoAssembleia(Base):
    __tablename__ = 'procuracao_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    assembleia_id = Column(Uuid, ForeignKey('assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    outorgante_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    outorgado_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    chave_documento = Column(Text, nullable=True)
    validada_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    status = Column(String(30), nullable=False, default='PENDENTE')  # 'PENDENTE', 'VALIDADA', 'REJEITADA'
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assembleia = relationship('Assembleia', back_populates='procuracoes')


class VotacaoAssembleia(Base):
    __tablename__ = 'votacao_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pauta_id = Column(Uuid, ForeignKey('pauta_assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    inicio_em = Column(DateTime(timezone=True), nullable=True)
    fim_em = Column(DateTime(timezone=True), nullable=True)
    quorum_necessario = Column(Numeric(8, 4), nullable=True)
    status = Column(String(30), nullable=False, default='AGUARDANDO')  # 'AGUARDANDO', 'ABERTA', 'ENCERRADA'

    pauta = relationship('PautaAssembleia', back_populates='votacoes')
    opcoes = relationship('OpcaoVotacao', back_populates='votacao', cascade='all, delete-orphan')
    votos = relationship('VotoAssembleia', back_populates='votacao', cascade='all, delete-orphan')


class OpcaoVotacao(Base):
    __tablename__ = 'opcao_votacao'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    votacao_id = Column(Uuid, ForeignKey('votacao_assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    descricao = Column(String(200), nullable=False)

    votacao = relationship('VotacaoAssembleia', back_populates='opcoes')
    votos = relationship('VotoAssembleia', back_populates='opcao', cascade='all, delete-orphan')


class VotoAssembleia(Base):
    __tablename__ = 'voto_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    votacao_id = Column(Uuid, ForeignKey('votacao_assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    opcao_id = Column(Uuid, ForeignKey('opcao_votacao.id'), nullable=False, index=True)
    peso = Column(Numeric(12, 4), nullable=False, default=1.0)
    votado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    hash_auditoria = Column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint('votacao_id', 'pessoa_id', name='uq_voto_assembleia_pessoa'),
    )

    votacao = relationship('VotacaoAssembleia', back_populates='votos')
    opcao = relationship('OpcaoVotacao', back_populates='votos')


class AtaAssembleia(Base):
    __tablename__ = 'ata_assembleia'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    assembleia_id = Column(Uuid, ForeignKey('assembleia.id', ondelete='CASCADE'), nullable=False, index=True)
    texto_ata = Column(Text, nullable=False)
    chave_documento_assinado = Column(Text, nullable=True)
    redigida_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    aprovada = Column(Boolean, nullable=False, default=False)
    registrada_em = Column(DateTime(timezone=True), nullable=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assembleia = relationship('Assembleia', back_populates='atas')


# Aliases
Assembly = Assembleia
AssemblyTopic = PautaAssembleia
AssemblyVote = VotoAssembleia
AssemblyMinutes = AtaAssembleia
