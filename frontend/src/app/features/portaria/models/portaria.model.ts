export interface AtendimentoPortaria {
  id: string;
  condominioId?: string;
  unidadeId?: string;
  visitanteNome: string;
  documento?: string;
  tipo: 'visitante' | 'prestador' | 'hospede' | 'delivery' | string;
  unidadeDestino?: string;
  status: 'aguardando' | 'autorizado' | 'entrou' | 'saiu' | 'recusado' | string;
  fotoUrl?: string;
  entradaEm?: string;
  saidaEm?: string;
}

export interface Prestador {
  id: string;
  condominioId: string;
  pessoaId: string;
  nome?: string;
  empresa?: string;
  documentoEmpresa?: string;
  atividade?: string;
  status: string;
}

export interface RegistroVisita {
  id: string;
  condominioId: string;
  unidadeId: string;
  visitanteId?: string;
  prestadorId?: string;
  atendidoPor?: string;
  entradaEm: string;
  saidaEm?: string;
  observacao?: string;
}

export interface PacoteEncomenda {
  id: string;
  condominioId?: string;
  unidadeId?: string;
  unidadeDestino?: string;
  destinatarioId?: string;
  moradorNome?: string;
  transportadora?: string;
  codigoRastreio?: string;
  codigoRetirada?: string;
  fotoUrl?: string;
  recebidoEm?: string;
  retiradoEm?: string;
  status: 'RECEBIDA' | 'RETIRADA' | 'pendente' | 'retirado' | string;
}

export interface AgendamentoMudanca {
  id: string;
  condominioId: string;
  unidadeId: string;
  solicitanteId: string;
  tipoMudanca: 'ENTRADA' | 'SAIDA';
  dataHoraInicio: string;
  dataHoraFim: string;
  reservaElevador: boolean;
  status: 'SOLICITADA' | 'CONFIRMADA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  observacao?: string;
}

export interface ItemPerdido {
  id: string;
  condominioId: string;
  descricao: string;
  categoria?: string;
  localEncontrado?: string;
  fotoUrl?: string;
  status: 'CUSTODIA' | 'DEVOLVIDO' | 'DOADO' | 'DESCARTADO';
  encontradoEm: string;
  restituidoEm?: string;
}
