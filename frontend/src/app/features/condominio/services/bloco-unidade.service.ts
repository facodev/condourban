import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Bloco, Unidade } from '../models/condominio.model';

@Injectable({
  providedIn: 'root'
})
export class BlocoUnidadeService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/condominio`;

  getBlocos(condominioId?: string): Observable<Bloco[]> {
    const url = condominioId ? `${this.baseUrl}/blocos?condominio_id=${condominioId}` : `${this.baseUrl}/blocos`;
    return this.http.get<Bloco[]>(url);
  }

  createBloco(bloco: { nome?: string; name?: string; descricao?: string; description?: string; ordem?: number }): Observable<Bloco> {
    const payload = {
      nome: bloco.nome || bloco.name || '',
      descricao: bloco.descricao || bloco.description || null,
      ordem: bloco.ordem ?? null
    };
    return this.http.post<Bloco>(`${this.baseUrl}/blocos`, payload);
  }

  updateBloco(id: string, dto: { nome?: string; descricao?: string; status?: string; ordem?: number }): Observable<Bloco> {
    return this.http.patch<Bloco>(`${this.baseUrl}/blocos/${id}`, dto);
  }

  deleteBloco(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/blocos/${id}`);
  }

  getUnidades(blocoId?: string, condominioId?: string): Observable<Unidade[]> {
    let url = `${this.baseUrl}/unidades`;
    const params = new URLSearchParams();
    if (blocoId) params.append('bloco_id', blocoId);
    if (condominioId) params.append('condominio_id', condominioId);
    const queryString = params.toString();
    if (queryString) url += `?${queryString}`;
    return this.http.get<Unidade[]>(url);
  }

  createUnidade(unidade: Partial<Unidade>): Observable<Unidade> {
    const payload = {
      identificacao: unidade.identificacao || (unidade as any).number || '',
      andar: unidade.andar || (unidade as any).floor || null,
      bloco_id: unidade.bloco_id || (unidade as any).blocoId || null,
      tipo: unidade.tipo || 'APARTAMENTO',
      descricao: unidade.descricao || null,
      area_privativa: unidade.area_privativa || null
    };
    return this.http.post<Unidade>(`${this.baseUrl}/unidades`, payload);
  }

  updateUnidade(id: string, dto: Partial<Unidade>): Observable<Unidade> {
    const payload = {
      identificacao: dto.identificacao || (dto as any).number,
      andar: dto.andar || (dto as any).floor,
      bloco_id: dto.bloco_id || (dto as any).blocoId,
      tipo: dto.tipo,
      descricao: dto.descricao,
      area_privativa: dto.area_privativa,
      status: dto.status
    };
    return this.http.patch<Unidade>(`${this.baseUrl}/unidades/${id}`, payload);
  }

  deleteUnidade(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/unidades/${id}`);
  }

  importarUnidadesCsv(conteudoCsv: string, condominioId?: string): Observable<any> {
    const url = condominioId ? `${this.baseUrl}/unidades/importar?condominio_id=${condominioId}` : `${this.baseUrl}/unidades/importar`;
    return this.http.post<any>(url, { arquivo_csv: conteudoCsv });
  }
}

