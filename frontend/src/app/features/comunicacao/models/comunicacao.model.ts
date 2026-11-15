export type OrigemOcorrencia = 'MORADOR' | 'PORTARIA' | 'GESTAO';
export type StatusOcorrencia =
  | 'ABERTA'
  | 'EM_ANDAMENTO'
  | 'RESOLVIDA'
  | 'CANCELADA'
  | 'pendente'
  | 'em_analise'
  | 'resolvido'
  | 'cancelado';

export interface Comunicado {
  id: string | number;
  condominioId?: string;
  titulo: string;
  conteudo: string;
  autorId?: string;
  urgente: boolean;
  fixado?: boolean;
  publicadoEm?: string;
  expiraEm?: string;
  status?: string;
  criadoEm?: string;

  // Visualização amigável
  autorNome?: string;
}

export interface LeituraComunicado {
  id: string;
  condominioId: string;
  comunicadoId: string;
  pessoaId: string;
  lidoEm: string;
}

export interface MensagemFaleConosco {
  id: string;
  condominioId: string;
  remetenteId: string;
  destinatarioId?: string;
  assunto: string;
  mensagem: string;
  lidaEm?: string;
  enviadaEm: string;
}

export interface HistoricoOcorrencia {
  id: string;
  ocorrenciaId: string;
  autorId: string;
  mensagem: string;
  tipo: 'COMENTARIO' | 'MUDANCA_STATUS' | 'PARECER';
  criadoEm: string;
  autorNome?: string;
}

export interface Ocorrencia {
  id: string | number;
  condominioId?: string;
  unidadeId?: string;
  registradaPor?: string;
  origem?: OrigemOcorrencia;
  categoria?: string;
  titulo: string;
  descricao: string;
  prioridade?: string;
  status: StatusOcorrencia;
  sigilosa?: boolean;
  responsavelId?: string;
  criadaEm?: string;
  resolvidaEm?: string;
  historico?: HistoricoOcorrencia[];

  // Visualização amigável
  unidade?: string;
  autorNome?: string;
  criadoEm?: string;
}

export interface OpcaoEnquete {
  id: string;
  enqueteId?: string;
  descricao: string;
  ordem: number;
  totalVotos?: number;
}

export interface Enquete {
  id: string;
  condominioId: string;
  titulo: string;
  descricao?: string;
  inicioEm: string;
  fimEm: string;
  anonima: boolean;
  status: string;
  criadaPor?: string;
  criadaEm: string;
  opcoes?: OpcaoEnquete[];
}

export interface ItemComunidade {
  id: string | number;
  condominioId?: string;
  autorId?: string;
  tipo: 'CLASSIFICADO' | 'AVISO' | 'RECOMENDACAO' | 'enquete' | 'achado_perdido' | 'classificado';
  titulo: string;
  descricao: string;
  preco?: number;
  contato?: string;
  fotoUrl?: string;
  status?: string;
  criadoEm?: string;
  expiraEm?: string;

  // Visualização amigável
  autorNome?: string;
  publicadoEm?: string;
  detalhes?: Record<string, unknown>;
}

// Aliases de retrocompatibilidade com UI existente
export type ComunicadoOficial = Comunicado;
export type ItemMuralSocial = ItemComunidade;
