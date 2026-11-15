export type PrioridadeChamado =
  | 'BAIXA'
  | 'MEDIA'
  | 'ALTA'
  | 'URGENTE'
  | 'baixa'
  | 'media'
  | 'alta'
  | 'urgente';

export type StatusChamado =
  | 'ABERTO'
  | 'EM_ANDAMENTO'
  | 'CONCLUIDO'
  | 'CANCELADO'
  | 'aberto'
  | 'em_andamento'
  | 'concluido'
  | 'cancelado';

export type StatusOrdemServico =
  | 'RASCUNHO'
  | 'AGENDADA'
  | 'EM_EXECUCAO'
  | 'CONCLUIDA'
  | 'CANCELADA';

export interface ChamadoManutencao {
  id: string | number;
  condominioId?: string;
  unidadeId?: string;
  solicitanteId?: string;
  categoria?: string;
  titulo: string;
  descricao: string;
  localizacao?: string;
  fotoUrl?: string;
  prioridade: PrioridadeChamado;
  status: StatusChamado;
  atribuidoA?: string;
  criadoEm?: string;
  concluidoEm?: string;

  // Campos de compatibilidade com a UI existente
  local?: string;
  abertoPor?: string;
  abertoEm?: string;
}

export interface OrdemServico {
  id: string;
  condominioId: string;
  chamadoId?: string;
  prestadorId?: string;
  responsavelInternoId?: string;
  descricao: string;
  valorEstimado?: number;
  valorFinal?: number;
  dataAgendada?: string;
  status: StatusOrdemServico;
  laudoConclusao?: string;
  iniciadoEm?: string;
  finalizadoEm?: string;
  criadaEm: string;
  atualizadaEm: string;
}

export interface ItemPreventivaPMO {
  id: string | number;
  condominioId?: string;
  sistema?: string;
  descricao?: string;
  periodicidadeDias?: number;
  instrucaoTecnica?: string;
  proximaInspecao?: string;
  ativo?: boolean;
  criadoEm?: string;

  // Campos de compatibilidade com UI existente
  equipamento?: string;
  localizacao?: string;
  periodicidade?: string;
  proximaManutencao?: string;
  responsavelTecnico?: string;
  status?: 'em_dia' | 'alerta' | 'atrasado';
}

export interface RegistroInspecaoPMO {
  id: string;
  condominioId: string;
  itemPreventivaPmoId: string;
  inspecionadoEm: string;
  responsavelTecnico: string;
  registroProfissional?: string;
  conforme: boolean;
  parecerTecnico?: string;
  chaveArtLaudo?: string;
  criadoEm: string;
}

// Aliases de retrocompatibilidade com UI existente
export type ChamadoServico = ChamadoManutencao;
export type ItemInventarioPMO = ItemPreventivaPMO;
