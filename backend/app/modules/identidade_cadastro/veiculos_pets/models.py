import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, Uuid, func

from app.core.database import Base


class Veiculo(Base):
    __tablename__ = 'veiculo'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    proprietario_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True)
    vaga_garagem_id = Column(Uuid, nullable=True)
    placa = Column(String(10), nullable=False, index=True)
    tipo = Column(String(30), default='CARRO', nullable=False)
    marca = Column(String(50), nullable=True)
    modelo = Column(String(50), nullable=True)
    cor = Column(String(30), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Pet(Base):
    __tablename__ = 'pet'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    tutor_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True)
    nome = Column(String(100), nullable=False)
    especie = Column(String(50), default='CANINO', nullable=False)
    raca = Column(String(100), nullable=True)
    porte = Column(String(30), default='MEDIO', nullable=False)
    cor = Column(String(50), nullable=True)
    foto_url = Column(Text, nullable=True)
    vacinado = Column(Boolean, default=True, nullable=False)
    status = Column(String(30), default='ATIVO', nullable=False)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
