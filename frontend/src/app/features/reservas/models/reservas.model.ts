export type StatusReserva =
  | 'SOLICITADA'
  | 'APROVADA'
  | 'REJEITADA'
  | 'CANCELADA'
  | 'CONCLUIDA'
  | 'pendente'
  | 'aprovado'
  | 'cancelado'
  | 'concluido';

export type TipoVistoria = 'ENTRADA' | 'SAIDA' | 'pre_uso' | 'pos_uso';

export interface ConvidadoReserva {
  id: string;
  condominioId: string;
  reservaId: string;
  nomeCompleto: string;
  documento?: string;
  presente: boolean;
  horarioEntrada?: string;
  criadoEm: string;
}

export interface Reserva {
  id: string;
  condominioId?: string;
  areaComumId?: string;
  unidadeId?: string;
  solicitanteId?: string;
  inicioEm?: string;
  fimEm?: string;
  valor?: number;
  termoAceito?: boolean;
  status: StatusReserva;
  observacao?: string;
  criadoEm?: string;
  atualizadoEm?: string;
  convidados?: ConvidadoReserva[];

  // Campos amigáveis / visualização
  areaComumNome?: string;
  moradorNome?: string;
  unidade?: string;
  data?: string;
  horarioInicio?: string;
  horarioFim?: string;
  listaConvidados?: string[];
  valorTaxa?: number;
}

export interface VistoriaReserva {
  id: string | number;
  condominioId?: string;
  reservaId: string | number;
  vistoriadorId?: string;
  tipo: TipoVistoria;
  checklist?: Record<string, unknown>;
  avariasDetectadas?: string;
  fotos?: string[];
  valorCaucaoRetido?: number;
  concluidaEm?: string;
  criadoEm?: string;

  // Visualização e retrocompatibilidade
  areaComumNome?: string;
  responsavelNome?: string;
  statusCaucao?: 'retido' | 'devolvido' | 'retido_parcial';
  observacoes?: string;
  fotosUrls?: string[];
  realizadoEm?: string;
}

// Aliases para manter compatibilidade com componentes existentes
export type AgendamentoReserva = Reserva;
