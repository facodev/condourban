import uuid

from sqlalchemy import Column, DateTime, String, Time, Uuid, func

from app.core.database import Base


class CredencialAcesso(Base):
    __tablename__ = 'credencial_acesso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    pessoa_id = Column(Uuid, nullable=False, index=True)
    tipo = Column(String(30), nullable=False)  # TAG_RFID, FACIAL, QR_CODE, SENHA
    provedor = Column(String(50), nullable=False)
    referencia_externa = Column(String(200), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ativada_em = Column(DateTime(timezone=True), nullable=True)
    desativada_em = Column(DateTime(timezone=True), nullable=True)


class AutorizacaoAcesso(Base):
    __tablename__ = 'autorizacao_acesso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    pessoa_id = Column(Uuid, nullable=False, index=True)
    credencial_acesso_id = Column(Uuid, nullable=True)
    unidade_id = Column(Uuid, nullable=True)
    tipo_autorizacao = Column(String(50), nullable=False)
    inicio_em = Column(DateTime(timezone=True), nullable=False)
    fim_em = Column(DateTime(timezone=True), nullable=True)
    horario_inicio = Column(Time, nullable=True)
    horario_fim = Column(Time, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    motivo = Column(String(500), nullable=True)
    criado_por = Column(Uuid, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
