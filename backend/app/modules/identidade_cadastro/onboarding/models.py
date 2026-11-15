import uuid

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Numeric, String, Text, Uuid, func

from app.core.database import Base


class ConviteCadastroMorador(Base):
    __tablename__ = 'convite_cadastro_morador'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    unidade_id = Column(Uuid, nullable=False, index=True)
    tipo_vinculo = Column(String(50), nullable=False)
    codigo = Column(String(20), unique=True, nullable=True)
    token_hash = Column(String(128), nullable=False, index=True)
    criado_por = Column(Uuid, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    validade_em = Column(DateTime(timezone=True), nullable=False)
    usado_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)


class SolicitacaoCadastroMorador(Base):
    __tablename__ = 'solicitacao_cadastro_morador'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    unidade_id = Column(Uuid, nullable=False, index=True)
    convite_id = Column(Uuid, nullable=True)
    pessoa_id = Column(Uuid, nullable=True)
    tipo_vinculo = Column(String(50), nullable=False)
    status = Column(String(50), default='RASCUNHO', nullable=False)
    etapa_atual = Column(String(50), nullable=True)
    criada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    enviada_em = Column(DateTime(timezone=True), nullable=True)
    analisada_em = Column(DateTime(timezone=True), nullable=True)
    analisada_por = Column(Uuid, nullable=True)
    motivo_rejeicao = Column(Text, nullable=True)
    observacao_administrador = Column(Text, nullable=True)
    criado_por = Column(Uuid, nullable=True)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class DocumentoCadastro(Base):
    __tablename__ = 'documento_cadastro'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    solicitacao_cadastro_id = Column(Uuid, nullable=False, index=True)
    tipo_documento = Column(String(50), nullable=False)
    nome_original = Column(String(255), nullable=True)
    chave_armazenamento = Column(Text, nullable=False)
    tipo_mime = Column(String(100), nullable=True)
    tamanho_bytes = Column(BigInteger, nullable=True)
    hash_arquivo = Column(String(128), nullable=True)
    status_validacao = Column(String(30), default='PENDENTE', nullable=False)
    observacao = Column(Text, nullable=True)
    enviado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    validado_em = Column(DateTime(timezone=True), nullable=True)
    validado_por = Column(Uuid, nullable=True)


class VerificacaoFacial(Base):
    __tablename__ = 'verificacao_facial'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    pessoa_id = Column(Uuid, nullable=True)
    solicitacao_cadastro_id = Column(Uuid, nullable=True)
    provedor = Column(String(50), nullable=False)
    referencia_externa = Column(String(200), nullable=True)
    tipo_verificacao = Column(String(50), nullable=False)
    resultado = Column(String(30), default='PENDENTE', nullable=False)
    pontuacao = Column(Numeric(8, 5), nullable=True)
    prova_de_vida = Column(Boolean, nullable=True)
    consentimento_em = Column(DateTime(timezone=True), nullable=True)
    iniciada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    concluida_em = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
