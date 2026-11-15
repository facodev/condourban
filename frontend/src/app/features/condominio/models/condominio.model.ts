export interface Condominio {
  id: string;
  inquilinoId?: string;
  nome: string;
  razaoSocial?: string;
  razao_social?: string;
  cnpj?: string;
  cep?: string;
  logradouro?: string;
  numero?: string;
  complemento?: string;
  bairro?: string;
  cidade?: string;
  uf?: string;
  status?: string;
}

export interface Bloco {
  id: string;
  condominio_id?: string;
  condominioId?: string;
  nome: string;
  descricao?: string;
  ordem?: number;
  status?: string;
  name?: string;
  description?: string;
}

export interface Unidade {
  id: string;
  condominio_id?: string;
  condominioId?: string;
  bloco_id?: string;
  blocoId?: string;
  identificacao: string;
  andar?: string | number;
  tipo?: string;
  descricao?: string;
  area_privativa?: number;
  status?: string;
  number?: string;
  floor?: string | number;
}

export type Block = Bloco;
export type Unit = Unidade;

export interface VagaGaragem {
  id: string;
  condominioId?: string;
  condominio_id?: string;
  unidadeId?: string;
  unidade_id?: string;
  identificacao: string;
  tipo?: string;
  coberta: boolean;
  status: string;
}

export interface AreaComum {
  id: string;
  condominioId?: string;
  condominio_id?: string;
  nome: string;
  descricao?: string;
  capacidade: number;
  valorReserva?: number;
  taxaReserva?: number;
  horarioAbertura?: string;
  horarioFechamento?: string;
  requerAprovacao?: boolean;
  regras_dias?: Record<string, any>;
  regrasDias?: Record<string, any>;
  ativo?: boolean;
  status?: string;
}
