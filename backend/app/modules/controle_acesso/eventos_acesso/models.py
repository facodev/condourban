import uuid

from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text, Uuid, func

from app.core.database import Base


class EventoAcesso(Base):
    __tablename__ = 'evento_acesso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    pessoa_id = Column(Uuid, nullable=True, index=True)
    credencial_acesso_id = Column(Uuid, nullable=True)
    dispositivo_acesso_id = Column(Uuid, nullable=True)
    autorizacao_acesso_id = Column(Uuid, nullable=True)
    tipo_evento = Column(String(50), nullable=False)
    resultado = Column(String(50), nullable=True)
    ocorrido_em = Column(DateTime(timezone=True), nullable=False, index=True)
    identificacao_externa = Column(String(200), nullable=True)
    pontuacao_facial = Column(Numeric(8, 5), nullable=True)
    imagem_referencia_url = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SincronizacaoAcesso(Base):
    __tablename__ = 'sincronizacao_acesso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    integracao_provedor_id = Column(Uuid, nullable=False)
    tipo_operacao = Column(String(50), nullable=False)
    entidade = Column(String(100), nullable=False)
    entidade_id = Column(Uuid, nullable=False)
    status = Column(String(30), default='PENDENTE', nullable=False, index=True)
    tentativas = Column(Integer, default=0, nullable=False)
    ultima_tentativa_em = Column(DateTime(timezone=True), nullable=True)
    concluida_em = Column(DateTime(timezone=True), nullable=True)
    erro = Column(Text, nullable=True)
    idempotencia_chave = Column(String(200), nullable=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
