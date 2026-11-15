import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Time, Uuid, func

from app.core.database import Base


class Visitante(Base):
    __tablename__ = 'visitante'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=True, index=True)
    responsavel_id = Column(Uuid, nullable=True)
    observacao = Column(Text, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # Campos transientes de compatibilidade
    nome_completo = None
    documento = None


class ConviteVisitante(Base):
    __tablename__ = 'convite_visitante'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    unidade_id = Column(Uuid, ForeignKey('unidade.id'), nullable=False, index=True)
    visitante_id = Column(Uuid, ForeignKey('visitante.id'), nullable=False, index=True)
    criado_por = Column(Uuid, ForeignKey('pessoa.id'), nullable=False)
    inicio_validade = Column(DateTime(timezone=True), nullable=False)
    fim_validade = Column(DateTime(timezone=True), nullable=False)
    quantidade_maxima_entradas = Column(Integer, default=1, nullable=False)
    codigo = Column(String(50), nullable=True)
    token_hash = Column(String(128), nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cancelado_em = Column(DateTime(timezone=True), nullable=True)


class Prestador(Base):
    __tablename__ = 'prestador'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, ForeignKey('condominio.id'), nullable=False, index=True)
    pessoa_id = Column(Uuid, ForeignKey('pessoa.id'), nullable=False, index=True)
    empresa = Column(String(200), nullable=True)
    documento_empresa = Column(String(30), nullable=True)
    atividade = Column(String(200), nullable=True)
    observacao = Column(Text, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AutorizacaoPrestador(Base):
    __tablename__ = 'autorizacao_prestador'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    prestador_id = Column(Uuid, nullable=False, index=True)
    unidade_id = Column(Uuid, nullable=True)
    inicio_validade = Column(DateTime(timezone=True), nullable=False)
    fim_validade = Column(DateTime(timezone=True), nullable=True)
    horario_inicio = Column(Time, nullable=True)
    horario_fim = Column(Time, nullable=True)
    criado_por = Column(Uuid, nullable=True)
    status = Column(String(30), default='ATIVO', nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class RegistroVisita(Base):
    __tablename__ = 'registro_visita'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    visitante_id = Column(Uuid, nullable=True, index=True)
    prestador_id = Column(Uuid, nullable=True, index=True)
    unidade_id = Column(Uuid, nullable=False, index=True)
    atendido_por = Column(Uuid, nullable=True)
    entrada_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    saida_em = Column(DateTime(timezone=True), nullable=True)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AgendamentoMudanca(Base):
    __tablename__ = 'agendamento_mudanca'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    unidade_id = Column(Uuid, nullable=False, index=True)
    solicitante_id = Column(Uuid, nullable=False)
    tipo_mudanca = Column(String(20), nullable=False)  # ENTRADA, SAIDA
    data_hora_inicio = Column(DateTime(timezone=True), nullable=False)
    data_hora_fim = Column(DateTime(timezone=True), nullable=False)
    reserva_elevador = Column(Boolean, default=True, nullable=False)
    status = Column(String(30), default='SOLICITADA', nullable=False)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ItemPerdido(Base):
    __tablename__ = 'item_perdido'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    condominio_id = Column(Uuid, nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    categoria = Column(String(50), nullable=True)
    local_encontrado = Column(String(100), nullable=True)
    encontrado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    encontrado_por = Column(Uuid, nullable=True)
    foto_url = Column(Text, nullable=True)
    status = Column(String(30), default='CUSTODIA', nullable=False)  # CUSTODIA, DEVOLVIDO, DOADO, DESCARTADO
    restituido_para = Column(Uuid, nullable=True)
    restituido_em = Column(DateTime(timezone=True), nullable=True)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# Aliases
Visitor = Visitante
