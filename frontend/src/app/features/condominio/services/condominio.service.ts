import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  Condominio,
  Bloco,
  Unidade,
  AreaComum,
  Block,
  Unit,
  VagaGaragem
} from '../models/condominio.model';
import { BlocoUnidadeService } from './bloco-unidade.service';
import { VagasService } from './vagas.service';
import { BrandingService } from './branding.service';

export * from '../models/condominio.model';
export { BlocoUnidadeService } from './bloco-unidade.service';
export { VagasService } from './vagas.service';
export { BrandingService } from './branding.service';

@Injectable({
  providedIn: 'root'
})
export class CondominioService {
  private readonly http = inject(HttpClient);
  private readonly blocoUnidadeService = inject(BlocoUnidadeService);
  private readonly vagasService = inject(VagasService);
  private readonly brandingService = inject(BrandingService);
  private readonly baseUrl = `${environment.apiUrl}/condominio`;

  // Blocos
  getBlocos(condominioId?: string): Observable<Bloco[]> {
    return this.blocoUnidadeService.getBlocos(condominioId);
  }

  getBlocks(condominioId?: string): Observable<Bloco[]> {
    return this.getBlocos(condominioId);
  }

  createBloco(bloco: { nome?: string; name?: string; descricao?: string; description?: string; ordem?: number }): Observable<Bloco> {
    return this.blocoUnidadeService.createBloco(bloco);
  }

  createBlock(bloco: { nome?: string; name?: string; descricao?: string; description?: string; ordem?: number }): Observable<Bloco> {
    return this.createBloco(bloco);
  }

  updateBloco(id: string, dto: { nome?: string; descricao?: string; status?: string; ordem?: number }): Observable<Bloco> {
    return this.blocoUnidadeService.updateBloco(id, dto);
  }

  updateBlock(id: string, dto: { nome?: string; descricao?: string; status?: string; ordem?: number }): Observable<Bloco> {
    return this.updateBloco(id, dto);
  }

  deleteBloco(id: string): Observable<any> {
    return this.blocoUnidadeService.deleteBloco(id);
  }

  deleteBlock(id: string): Observable<any> {
    return this.deleteBloco(id);
  }

  // Unidades
  getUnidades(blocoId?: string, condominioId?: string): Observable<Unidade[]> {
    return this.blocoUnidadeService.getUnidades(blocoId, condominioId);
  }

  getUnits(blocoId?: string, condominioId?: string): Observable<Unidade[]> {
    return this.getUnidades(blocoId, condominioId);
  }

  createUnidade(unidade: Partial<Unidade>): Observable<Unidade> {
    return this.blocoUnidadeService.createUnidade(unidade);
  }

  createUnit(unidade: Partial<Unidade>): Observable<Unidade> {
    return this.createUnidade(unidade);
  }

  updateUnidade(id: string, dto: Partial<Unidade>): Observable<Unidade> {
    return this.blocoUnidadeService.updateUnidade(id, dto);
  }

  updateUnit(id: string, dto: Partial<Unidade>): Observable<Unidade> {
    return this.updateUnidade(id, dto);
  }

  deleteUnidade(id: string): Observable<any> {
    return this.blocoUnidadeService.deleteUnidade(id);
  }

  deleteUnit(id: string): Observable<any> {
    return this.deleteUnidade(id);
  }

  importarUnidadesCsv(conteudoCsv: string, condominioId?: string): Observable<any> {
    return this.blocoUnidadeService.importarUnidadesCsv(conteudoCsv, condominioId);
  }

  // Vagas
  getVagas(unidadeId?: string, condominioId?: string): Observable<VagaGaragem[]> {
    return this.vagasService.getVagas(unidadeId, condominioId);
  }

  createVaga(vaga: { identificacao: string; tipo?: string; coberta?: boolean; unidade_id?: string; condominio_id?: string }): Observable<VagaGaragem> {
    return this.vagasService.createVaga(vaga);
  }

  updateVaga(id: string, dto: { identificacao?: string; tipo?: string; coberta?: boolean; unidade_id?: string | null }): Observable<VagaGaragem> {
    return this.vagasService.updateVaga(id, dto);
  }

  deleteVaga(id: string): Observable<any> {
    return this.vagasService.deleteVaga(id);
  }

  // Áreas Comuns
  getAreasComuns(condominioId?: string): Observable<AreaComum[]> {
    const url = condominioId ? `${this.baseUrl}/areas-comuns?condominio_id=${condominioId}` : `${this.baseUrl}/areas-comuns`;
    return this.http.get<AreaComum[]>(url);
  }

  createAreaComum(area: {
    nome: string;
    capacidade: number;
    taxa_reserva?: number;
    valor_caucao?: number;
    horario_abertura?: string;
    horario_fechamento?: string;
    requer_aprovacao?: boolean;
    descricao?: string;
    regras_dias?: Record<string, any>;
    condominio_id?: string;
  }): Observable<AreaComum> {
    return this.http.post<AreaComum>(`${this.baseUrl}/areas-comuns`, area);
  }

  updateAreaComum(id: string, dto: Partial<AreaComum>): Observable<AreaComum> {
    return this.http.patch<AreaComum>(`${this.baseUrl}/areas-comuns/${id}`, dto);
  }

  atualizarAreaComum(id: string, dto: Partial<AreaComum>): Observable<AreaComum> {
    return this.updateAreaComum(id, dto);
  }

  updateAreaStatus(id: string, ativo: boolean): Observable<AreaComum> {
    return this.atualizarAreaComum(id, { ativo });
  }

  deleteAreaComum(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/areas-comuns/${id}`);
  }

  // Multi-Condomínio & Branding
  getTodosCondominios(): Observable<Condominio[]> {
    return this.brandingService.getTodosCondominios();
  }

  createCondominio(condo: {
    nome: string;
    razao_social?: string;
    cnpj?: string;
    cep?: string;
    logradouro?: string;
    numero?: string;
    complemento?: string;
    bairro?: string;
    cidade?: string;
    uf?: string;
  }): Observable<Condominio> {
    return this.brandingService.createCondominio(condo);
  }

  deleteCondominio(id: string): Observable<any> {
    return this.brandingService.deleteCondominio(id);
  }

  getCondominioInfo(condominioId?: string): Observable<Condominio> {
    return this.brandingService.getInfo(condominioId);
  }

  updateCondominioInfo(dto: Partial<Condominio>, condominioId?: string): Observable<Condominio> {
    return this.brandingService.updateInfo(dto, condominioId);
  }
}
