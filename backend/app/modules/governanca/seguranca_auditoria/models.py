import uuid
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class PastaDocumento(Base):
    __tablename__ = 'pasta_documento'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    pasta_pai_id = Column(Uuid, ForeignKey('pasta_documento.id'), nullable=True, index=True)
    nome = Column(String(200), nullable=False)
    visibilidade = Column(String(50), nullable=False, default='ADMINISTRADORES')
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    subpastas = relationship('PastaDocumento')
    documentos = relationship('Documento', back_populates='pasta')


class Documento(Base):
    __tablename__ = 'documento'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    pasta_id = Column(Uuid, ForeignKey('pasta_documento.id'), nullable=True, index=True)
    nome = Column(String(255), nullable=False)
    chave_armazenamento = Column(Text, nullable=False)
    tipo_mime = Column(String(100), nullable=True)
    tamanho_bytes = Column(BigInteger, nullable=True)
    hash_arquivo = Column(String(128), nullable=True)
    versao = Column(Integer, nullable=False, default=1)
    enviado_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    vencimento_em = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    excluido_em = Column(DateTime(timezone=True), nullable=True)

    pasta = relationship('PastaDocumento', back_populates='documentos')



class EventoAuditoria(Base):
    __tablename__ = 'evento_auditoria'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=True, index=True)
    usuario_id = Column(Uuid, nullable=True, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=True, index=True)
    acao = Column(String(100), nullable=False)
    entidade = Column(String(100), nullable=False)
    entidade_id = Column(Uuid, nullable=True)
    ocorrido_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    endereco_ip = Column(String(45), nullable=True)
    agente_usuario = Column(Text, nullable=True)
    id_correlacao = Column(String(100), nullable=True)
    dados_anteriores = Column(JSON, nullable=True)
    dados_posteriores = Column(JSON, nullable=True)


class EventoUso(Base):
    __tablename__ = 'evento_uso'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=True, index=True)
    usuario_id = Column(Uuid, nullable=True, index=True)
    modulo = Column(String(50), nullable=False)
    funcionalidade_codigo = Column(String(80), nullable=True)
    acao = Column(String(50), nullable=False)
    ocorrido_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metadados = Column(JSON, nullable=False, default=dict)


# Aliases
AuditLog = EventoAuditoria
UsageEvent = EventoUso
DocumentFolder = PastaDocumento
DocumentFile = Documento
