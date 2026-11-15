export type TipoAssembleia = 'ORDINARIA' | 'EXTRAORDINARIA' | 'ordinaria' | 'extraordinaria';
export type StatusAssembleia =
  | 'AGENDADA'
  | 'EM_ANDAMENTO'
  | 'ENCERRADA'
  | 'CANCELADA'
  | 'convocada'
  | 'em_andamento'
  | 'encerrada';

export interface PautaAssembleia {
  id: string | number;
  assembleiaId?: string;
  titulo: string;
  descricao?: string;
  ordem?: number;
  votosFavoraveis?: number;
  votosContrarios?: number;
}

export interface Assembleia {
  id: string | number;
  condominioId?: string;
  titulo: string;
  tipo: TipoAssembleia;
  inicioEm?: string;
  fimEm?: string;
  status: StatusAssembleia;
  linkVideochamada?: string;
  regraQuorum?: Record<string, unknown>;
  criadaPor?: string;
  criadaEm?: string;
  pautas?: PautaAssembleia[];

  // Campos de compatibilidade com UI
  dataInicio?: string;
  editalUrl?: string;
  ataUrl?: string;
}

export interface ParticipanteAssembleia {
  id: string;
  assembleiaId: string;
  pessoaId: string;
  unidadeId?: string;
  entrouEm?: string;
  saiuEm?: string;
  presente: boolean;
}

export interface ProcuracaoAssembleia {
  id: string;
  condominioId: string;
  assembleiaId: string;
  outorganteId: string;
  outorgadoId: string;
  unidadeId: string;
  chaveDocumento?: string;
  validadaPor?: string;
  status: 'PENDENTE' | 'VALIDADA' | 'REJEITADA';
  criadaEm: string;
}

export interface AtaAssembleia {
  id: string;
  condominioId: string;
  assembleiaId: string;
  textoAta: string;
  chaveDocumentoAssinado?: string;
  redigidaPor?: string;
  aprovada: boolean;
  registradaEm?: string;
  criadaEm: string;
}

export interface PastaDocumento {
  id: string;
  condominioId: string;
  pastaPaiId?: string;
  nome: string;
  visibilidade: string;
  criadaEm: string;
}

export interface Documento {
  id: string;
  condominioId: string;
  pastaId?: string;
  nome: string;
  chaveArmazenamento: string;
  tipoMime?: string;
  tamanhoBytes?: number;
  versao: number;
  criadoEm: string;
}

export interface EventoAuditoria {
  id: string | number;
  condominioId?: string;
  usuarioId?: string;
  pessoaId?: string;
  acao: string;
  entidade: string;
  entidadeId?: string;
  ocorridoEm?: string;
  enderecoIp?: string;
  agenteUsuario?: string;
  idCorrelacao?: string;

  // Campos de compatibilidade com UI
  usuarioNome?: string;
  ipOrigem?: string;
  timestamp?: string;
}

export type LogAuditoria = EventoAuditoria;
