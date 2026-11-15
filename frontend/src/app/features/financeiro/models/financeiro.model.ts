export type StatusCobranca =
  | 'PENDENTE'
  | 'PAGO'
  | 'VENCIDO'
  | 'CANCELADO'
  | 'EM_ACORDO'
  | 'pendente'
  | 'pago'
  | 'atrasado';

export type TipoConsumo = 'AGUA_FRIA' | 'AGUA_QUENTE' | 'GAS' | 'ENERGIA' | 'agua' | 'gas';

export interface CobrancaCondominial {
  id: string | number;
  condominioId?: string;
  unidadeId?: string;
  competencia?: string;
  vencimento: string;
  valor: number;
  valorMulta?: number;
  valorJuros?: number;
  valorDesconto?: number;
  status: StatusCobranca;
  provedorPagamento?: string;
  identificacaoExterna?: string;
  linhaDigitavel?: string;
  codigoPix?: string;
  pagoEm?: string;
  valorPago?: number;
  criadoEm?: string;

  // Visualização e compatibilidade de UI
  unidade?: string;
  mesReferencia?: string;
  codigoBarras?: string;
}

export interface TermoAcordo {
  id: string;
  condominioId: string;
  unidadeId: string;
  devedorId: string;
  valorTotalOriginal: number;
  valorTotalNegociado: number;
  numeroParcelas: number;
  diaVencimentoParcelas: number;
  status: 'ATIVO' | 'QUITADO' | 'INADIMPLIDO' | 'CANCELADO';
  observacao?: string;
  assinadoEm?: string;
  criadoEm: string;
}

export interface DespesaCondominial {
  id: string;
  condominioId: string;
  categoria: string;
  fornecedor: string;
  cnpjCpfFornecedor?: string;
  descricao: string;
  valor: number;
  dataEmissao: string;
  dataVencimento: string;
  dataPagamento?: string;
  chaveComprovante?: string;
  aprovadaConselho: boolean;
  status: 'PENDENTE' | 'PAGO' | 'CANCELADO';
  criadoEm: string;
}

export interface MedicaoIndividual {
  id: string | number;
  condominioId?: string;
  unidadeId?: string;
  tipoConsumo?: TipoConsumo;
  competencia?: string;
  leituraAnterior: number;
  leituraAtual: number;
  consumo: number;
  valorCalculado?: number;
  fotoMedidorUrl?: string;
  criadoEm?: string;

  // Visualização e compatibilidade de UI
  unidade?: string;
  tipo?: 'agua' | 'gas' | string;
  mesReferencia?: string;
}

// Aliases de retrocompatibilidade com UI existente
export type CobrancaBoleto = CobrancaCondominial;
export type MedicaoConsumo = MedicaoIndividual;
