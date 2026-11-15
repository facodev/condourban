import uuid

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=True)
    google_sub = Column(String(255), unique=True, nullable=True)
    email_verificado = Column(Boolean, default=False, nullable=False)
    ultimo_acesso_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    # Campo transiente de compatibilidade
    nome_completo = None


class MembroCondominio(Base):
    __tablename__ = 'membro_condominio'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    tipo_pessoa = Column(String(50), nullable=False)  # MORADOR, VISITANTE, PRESTADOR, FUNCIONARIO, ADMINISTRADOR
    status = Column(String(30), default='ATIVO', nullable=False)
    entrou_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    saiu_em = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class OcupacaoUnidade(Base):
    __tablename__ = 'ocupacao_unidade'
    __table_args__ = (
        CheckConstraint(
            "tipo_vinculo NOT IN ('TEMPORARIO', 'HOSPEDE') OR (inicio_em IS NOT NULL AND fim_em IS NOT NULL)",
            name='ck_ocupacao_curto_prazo_datas',
        ),
        CheckConstraint(
            'fim_em IS NULL OR fim_em > inicio_em',
            name='ck_ocupacao_fim_maior_inicio',
        ),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    responsavel_ocupacao_id = Column(Uuid, ForeignKey('ocupacao_unidade.id'), nullable=True, index=True)
    tipo_vinculo = Column(String(50), nullable=False)  # PROPRIETARIO, INQUILINO, MORADOR, DEPENDENTE, TEMPORARIO, HOSPEDE, COMODATARIO, OUTRO
    mora_no_local = Column(Boolean, default=True, nullable=False)
    principal = Column(Boolean, default=False, nullable=False)
    inicio_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fim_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    dependentes = relationship(
        'OcupacaoUnidade',
        foreign_keys=[responsavel_ocupacao_id],
        remote_side=[responsavel_ocupacao_id],
    )


# Alias de retrocompatibilidade
User = Usuario
