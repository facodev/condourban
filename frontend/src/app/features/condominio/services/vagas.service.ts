import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { VagaGaragem } from '../models/condominio.model';

@Injectable({
  providedIn: 'root'
})
export class VagasService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/condominio`;

  getVagas(unidadeId?: string, condominioId?: string): Observable<VagaGaragem[]> {
    let url = `${this.baseUrl}/vagas`;
    const params = new URLSearchParams();
    if (unidadeId) params.append('unidade_id', unidadeId);
    if (condominioId) params.append('condominio_id', condominioId);
    const qs = params.toString();
    if (qs) url += `?${qs}`;
    return this.http.get<VagaGaragem[]>(url);
  }

  createVaga(vaga: { identificacao: string; tipo?: string; coberta?: boolean; unidade_id?: string; condominio_id?: string }): Observable<VagaGaragem> {
    const payload = {
      identificacao: vaga.identificacao.trim(),
      tipo: vaga.tipo || 'CARRO',
      coberta: !!vaga.coberta,
      unidade_id: vaga.unidade_id || null,
      condominio_id: vaga.condominio_id || null
    };
    return this.http.post<VagaGaragem>(`${this.baseUrl}/vagas`, payload);
  }

  updateVaga(id: string, dto: { identificacao?: string; tipo?: string; coberta?: boolean; unidade_id?: string | null }): Observable<VagaGaragem> {
    return this.http.patch<VagaGaragem>(`${this.baseUrl}/vagas/${id}`, dto);
  }

  deleteVaga(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/vagas/${id}`);
  }
}

