export interface TelefoneItem {
  numero: string;
  tipo: 'celular' | 'residencial' | 'comercial';
  principal: boolean;
  whatsapp: boolean;
}

export interface Pessoa {
  id: string;
  nome?: string;
  nomeCompleto?: string;
  nome_completo?: string;
  email?: string;
  telefone?: string;
  celular?: string;
  telefones?: TelefoneItem[];
  cpf?: string;
  tipoVinculo?: string;
  unidadeId?: string;
  criadoEm?: string;
  criado_em?: string;
}

export interface PessoaUpdate {
  nome?: string;
  nome_completo?: string;
  email?: string;
  celular?: string;
  telefone?: string;
  telefones?: TelefoneItem[];
  cpf?: string;
}

export interface OcupacaoUnidade {
  id: string;
  condominio_id?: string;
  unidade_id: string;
  pessoa_id: string;
  tipo_vinculo: 'PROPRIETARIO' | 'INQUILINO' | 'DEPENDENTE' | 'TEMPORARIO' | 'HOSPEDE' | string;
  mora_no_local: boolean;
  principal?: boolean;
  responsavel_ocupacao_id?: string | null;
  inicio_em?: string;
  fim_em?: string | null;
  status: 'ATIVA' | 'INATIVA' | 'EXPIRADA' | string;
  criado_em?: string;
  // Campos enriquecidos para exibição em tela
  pessoa_nome?: string;
  pessoa_email?: string;
  pessoa_cpf?: string;
  unidade_identificacao?: string;
  bloco_nome?: string;
}

export interface OcupacaoUnidadeCreate {
  condominio_id?: string;
  unidade_id: string;
  pessoa_id: string;
  tipo_vinculo: string;
  mora_no_local: boolean;
  principal?: boolean;
  responsavel_ocupacao_id?: string | null;
  inicio_em?: string;
  fim_em?: string | null;
  data_inicio?: string;
  data_fim?: string;
}

export interface UsuarioPerfil {
  id: string;
  email: string;
  nome?: string;
  nomeCompleto?: string;
  nome_completo?: string;
  ativo?: boolean;
  papeis?: string[];
  roles?: string[];
  ultimoAcessoEm?: string;
  condominioId?: string;
}

export interface SolicitacaoOnboarding {
  id: string;
  condominioId?: string;
  unidadeId?: string;
  nome: string;
  email: string;
  telefone?: string;
  unidadeIdentificador?: string;
  tipoVinculo?: string;
  tipoOcupacao?: string;
  etapaAtual?: string;
  status: 'pendente' | 'aprovado' | 'rejeitado' | 'RASCUNHO' | 'ENVIADA' | 'EM_ANALISE' | 'PENDENTE_CORRECAO' | 'APROVADA' | 'REJEITADA' | string;
  criadaEm?: string;
  criadoEm?: string;
}

export interface Veiculo {
  id?: string;
  condominio_id?: string;
  unidade_id?: string;
  placa: string;
  modelo: string;
  marca?: string;
  cor?: string;
  ano?: number;
  proprietario_id?: string;
  vaga_identificacao?: string;
}

export interface Pet {
  id?: string;
  condominio_id?: string;
  unidade_id?: string;
  nome: string;
  especie: string;
  raca?: string;
  porte: string;
  cor?: string;
  vacinado?: boolean;
  vacinacao_em_dia?: boolean;
  tutor_id?: string;
}

export interface VeiculoPetResponse {
  veiculos: Veiculo[];
  pets: Pet[];
}
