/** Papéis alinhados ao JWT / membro_condominio.tipo_pessoa (sempre MAIÚSCULO). */
export type PapelUsuario =
  | 'SUPERADMIN'
  | 'ADMINISTRADOR'
  | 'ADMIN'
  | 'ADMINISTRADORA'
  | 'SINDICO'
  | 'SUBSINDICO'
  | 'CONSELHO'
  | 'PORTARIA'
  | 'PORTEIRO'
  | 'FUNCIONARIO'
  | 'ZELADOR'
  | 'MORADOR'
  | 'PROPRIETARIO'
  | string;

export interface UnidadeContexto {
  id: number | string;
  condominioId: number | string;
  condominioNome: string;
  bloco?: string;
  numero: string;
  papel: PapelUsuario;
}

export interface UsuarioSessao {
  id: number | string;
  email: string;
  nomeCompleto: string;
  cpf?: string;
  telefone?: string;
  fotoUrl?: string;
  papeis: PapelUsuario[];
  pessoaId?: string | null;
  unidadeIds?: string[];
  unidadeAtiva?: UnidadeContexto;
  unidadesDisponiveis: UnidadeContexto[];
}
