export interface DispositivoAcesso {
  id: string;
  condominioId?: string;
  nome: string;
  tipo: 'catraca' | 'cancela' | 'leitor_facial' | 'antena_rfid' | string;
  provedor?: string;
  identificacaoExterna?: string;
  enderecoIp?: string;
  ip?: string;
  localizacao?: string;
  sentido?: 'entrada' | 'saida' | 'bidirecional' | string;
  status?: string;
  online?: boolean;
  ultimoSync?: string;
}

export interface CredencialAcesso {
  id: string;
  condominioId?: string;
  pessoaId?: string;
  pessoaNome?: string;
  tipo: 'tag_rfid' | 'facial' | 'qr_code' | 'senha' | string;
  provedor?: string;
  referenciaExterna?: string;
  codigoIdentificador?: string;
  status: 'ativo' | 'bloqueado' | 'expirado' | string;
  criadaEm?: string;
}

export interface EventoAcesso {
  id: string;
  condominioId?: string;
  pessoaId?: string;
  pessoaNome?: string;
  dispositivoNome?: string;
  tipoEvento?: string;
  resultado?: string;
  sentido?: 'entrada' | 'saida';
  autorizado?: boolean;
  motivo?: string;
  ocorridoEm?: string;
  timestamp?: string;
}

export interface SincronizacaoAcesso {
  id: string;
  condominioId: string;
  tipoOperacao: string;
  entidade: string;
  entidadeId: string;
  status: string;
  tentativas: number;
  criadaEm: string;
}
