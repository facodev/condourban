import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Uuid, func
from sqlalchemy.dialects.postgresql import INET, JSONB

from app.core.database import Base


class IntegracaoProvedor(Base):
    __tablename__ = 'integracao_provedor'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    provedor = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)
    nome = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class DispositivoAcesso(Base):
    __tablename__ = 'dispositivo_acesso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # CATRACA, CANCELA, LEITORA_FACIAL, ANTENA_RFID
    provedor = Column(String(50), nullable=False)
    identificacao_externa = Column(String(200), nullable=True)
    endereco_ip = Column(String(45), nullable=True)  # INET / IPv4 / IPv6
    localizacao = Column(String(200), nullable=True)
    sentido = Column(String(30), nullable=True)  # ENTRADA, SAIDA, BIDIRECIONAL
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
