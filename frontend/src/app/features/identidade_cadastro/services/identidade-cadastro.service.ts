import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  Pessoa,
  PessoaUpdate,
  TelefoneItem,
  OcupacaoUnidade,
  OcupacaoUnidadeCreate,
  UsuarioPerfil,
  SolicitacaoOnboarding,
  Veiculo,
  Pet,
  VeiculoPetResponse
} from '../models/identidade-cadastro.model';

export * from '../models/identidade-cadastro.model';

@Injectable({
  providedIn: 'root'
})
export class IdentidadeCadastroService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/identidade`;

  getPessoas(condominioId?: string): Observable<Pessoa[]> {
    const url = condominioId ? `${this.baseUrl}/pessoas?condominio_id=${condominioId}` : `${this.baseUrl}/pessoas`;
    return this.http.get<Pessoa[]>(url);
  }

  getPessoa(id: string): Observable<Pessoa> {
    return this.http.get<Pessoa>(`${this.baseUrl}/pessoas/${id}`);
  }

  createPessoa(pessoa: {
    nome?: string;
    nome_completo?: string;
    email?: string;
    celular?: string;
    cpf?: string;
    telefones?: TelefoneItem[];
  }): Observable<Pessoa> {
    const payload = {
      nome_completo: pessoa.nome_completo || pessoa.nome || '',
      nome: pessoa.nome || pessoa.nome_completo || '',
      email: pessoa.email,
      celular: pessoa.celular,
      cpf: pessoa.cpf,
      telefones: pessoa.telefones ?? []
    };
    return this.http.post<Pessoa>(`${this.baseUrl}/pessoas`, payload);
  }

  updatePessoa(id: string, pessoa: PessoaUpdate): Observable<Pessoa> {
    const payload: Record<string, any> = {};
    const nome = pessoa.nome_completo || pessoa.nome;
    if (nome != null && String(nome).trim() !== '') {
      payload['nome_completo'] = String(nome).trim();
      payload['nome'] = String(nome).trim();
    }
    if (pessoa.email != null) payload['email'] = pessoa.email;
    const celular = pessoa.celular || pessoa.telefone;
    if (celular != null) payload['celular'] = celular;
    if (pessoa.telefones != null) payload['telefones'] = pessoa.telefones;
    if (pessoa.cpf != null && String(pessoa.cpf).trim() !== '') {
      payload['cpf'] = String(pessoa.cpf).trim();
    }
    return this.http.patch<Pessoa>(`${this.baseUrl}/pessoas/${id}`, payload);
  }

  deletePessoa(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/pessoas/${id}`);
  }

  // ============================================================================
  // Vínculos & Ocupações de Unidades (Posse Direta e Regime Habitacional)
  // ============================================================================

  getOcupacoes(unidadeId?: string, apenasAtivas: boolean = false, condominioId?: string): Observable<OcupacaoUnidade[]> {
    let url = `${this.baseUrl}/ocupacoes?apenas_ativas=${apenasAtivas}`;
    if (unidadeId) {
      url += `&unidade_id=${unidadeId}`;
    }
    if (condominioId) {
      url += `&condominio_id=${condominioId}`;
    }
    return this.http.get<OcupacaoUnidade[]>(url);
  }

  createOcupacao(dto: OcupacaoUnidadeCreate): Observable<OcupacaoUnidade> {
    return this.http.post<OcupacaoUnidade>(`${this.baseUrl}/ocupacoes`, dto);
  }

  updateOcupacao(id: string, dto: Partial<OcupacaoUnidadeCreate>): Observable<OcupacaoUnidade> {
    return this.http.patch<OcupacaoUnidade>(`${this.baseUrl}/ocupacoes/${id}`, dto);
  }

  inativarOcupacao(id: string, cascadeDependentes: boolean = true, novoResponsavelId?: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/ocupacoes/${id}/inativar`, {
      cascade_dependentes: cascadeDependentes,
      novo_responsavel_ocupacao_id: novoResponsavelId || null
    });
  }

  executarRotinaExpiracao(): Observable<{ ocupacoes_inativadas: number; dependentes_inativados: number }> {
    return this.http.post<{ ocupacoes_inativadas: number; dependentes_inativados: number }>(
      `${this.baseUrl}/ocupacoes/rotina-expiracao`,
      {}
    );
  }

  getUsuarios(condominioId?: string): Observable<UsuarioPerfil[]> {
    const url = condominioId ? `${this.baseUrl}/usuarios?condominio_id=${condominioId}` : `${this.baseUrl}/usuarios`;
    return this.http.get<UsuarioPerfil[]>(url);
  }

  createUsuario(dto: {
    email: string;
    senha?: string;
    nome_completo?: string;
    papel?: string;
    papel_sistema?: string;
    condominio_id?: string;
    pessoa_id?: string;
  }): Observable<UsuarioPerfil> {
    return this.http.post<UsuarioPerfil>(`${this.baseUrl}/usuarios`, dto);
  }

  updateUsuario(
    id: string,
    dto: {
      email?: string;
      senha?: string;
      nome_completo?: string;
      papel?: string;
      papel_sistema?: string;
      status?: string;
      ativo?: boolean;
      condominio_id?: string;
      pessoa_id?: string;
    }
  ): Observable<UsuarioPerfil> {
    return this.http.patch<UsuarioPerfil>(`${this.baseUrl}/usuarios/${id}`, dto);
  }

  deleteUsuario(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/usuarios/${id}`);
  }

  getSolicitacoesOnboarding(): Observable<SolicitacaoOnboarding[]> {
    return this.http.get<SolicitacaoOnboarding[]>(`${this.baseUrl}/onboarding/solicitacoes`);
  }

  aprovarOnboarding(id: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/onboarding/solicitacoes/${id}/aprovar`, {});
  }

  aprovarSolicitacao(id: string): Observable<any> {
    return this.aprovarOnboarding(id);
  }

  rejeitarOnboarding(id: string, motivo: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/onboarding/solicitacoes/${id}/rejeitar`, {
      motivo_rejeicao: motivo,
      motivo: motivo
    });
  }

  rejeitarSolicitacao(id: string, motivo: string): Observable<any> {
    return this.rejeitarOnboarding(id, motivo);
  }

  criarConvite(dto: {
    email: string;
    unidade_id: string;
    tipo_vinculo?: string;
    tipo_ocupacao?: string;
  }): Observable<any> {
    const payload = {
      email: dto.email,
      unidade_id: dto.unidade_id,
      tipo_vinculo: dto.tipo_vinculo || dto.tipo_ocupacao || 'MORADOR'
    };
    return this.http.post<any>(`${this.baseUrl}/convites`, payload);
  }

  criarConviteOnboarding(dto: {
    email: string;
    unidade_id: string;
    tipo_vinculo?: string;
    tipo_ocupacao?: string;
  }): Observable<any> {
    return this.criarConvite(dto);
  }

  getVeiculos(unidadeId?: string, condominioId?: string): Observable<Veiculo[]> {
    let url = `${this.baseUrl}/veiculos-pets/veiculos`;
    const params = new URLSearchParams();
    if (unidadeId) params.append('unidade_id', unidadeId);
    if (condominioId) params.append('condominio_id', condominioId);
    const qs = params.toString();
    if (qs) url += `?${qs}`;
    return this.http.get<Veiculo[]>(url);
  }

  createVeiculo(veiculo: {
    placa: string;
    modelo: string;
    marca?: string;
    cor?: string;
    ano?: number;
    unidade_id?: string;
    proprietario_id?: string;
    vaga_identificacao?: string;
  }): Observable<Veiculo> {
    return this.http.post<Veiculo>(`${this.baseUrl}/veiculos-pets/veiculos`, veiculo);
  }

  deleteVeiculo(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/veiculos-pets/veiculos/${id}`);
  }

  getPets(unidadeId?: string, condominioId?: string): Observable<Pet[]> {
    let url = `${this.baseUrl}/veiculos-pets/pets`;
    const params = new URLSearchParams();
    if (unidadeId) params.append('unidade_id', unidadeId);
    if (condominioId) params.append('condominio_id', condominioId);
    const qs = params.toString();
    if (qs) url += `?${qs}`;
    return this.http.get<Pet[]>(url);
  }

  createPet(pet: {
    nome: string;
    especie: string;
    raca?: string;
    porte: string;
    cor?: string;
    vacinado?: boolean;
    vacinacao_em_dia?: boolean;
    unidade_id?: string;
    tutor_id?: string;
  }): Observable<Pet> {
    const payload = {
      nome: pet.nome,
      especie: pet.especie,
      raca: pet.raca,
      porte: pet.porte,
      cor: pet.cor,
      vacinado: pet.vacinado ?? pet.vacinacao_em_dia ?? true,
      unidade_id: pet.unidade_id,
      tutor_id: pet.tutor_id
    };
    return this.http.post<Pet>(`${this.baseUrl}/veiculos-pets/pets`, payload);
  }

  deletePet(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/veiculos-pets/pets/${id}`);
  }

  getVeiculosPets(unidadeId: string): Observable<VeiculoPetResponse> {
    return this.http.get<VeiculoPetResponse>(`${this.baseUrl}/veiculos-pets?unidadeId=${unidadeId}`);
  }
}
