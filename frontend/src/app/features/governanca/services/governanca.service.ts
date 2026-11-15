import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  Assembleia,
  PautaAssembleia,
  ProcuracaoAssembleia,
  AtaAssembleia,
  PastaDocumento,
  Documento,
  EventoAuditoria,
  LogAuditoria,
  TipoAssembleia,
  StatusAssembleia,
} from '../models/governanca.model';

export type {
  Assembleia,
  PautaAssembleia,
  ProcuracaoAssembleia,
  AtaAssembleia,
  PastaDocumento,
  Documento,
  EventoAuditoria,
  LogAuditoria,
  TipoAssembleia,
  StatusAssembleia,
};

@Injectable({
  providedIn: 'root'
})
export class GovernancaService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/governanca`;

  getAssembleias(condominioId?: string): Observable<Assembleia[]> {
    const url = condominioId ? `${this.baseUrl}/assembleias?condominio_id=${condominioId}` : `${this.baseUrl}/assembleias`;
    return this.http.get<Assembleia[]>(url);
  }

  getLogsAuditoria(condominioId?: string): Observable<LogAuditoria[]> {
    const url = condominioId ? `${this.baseUrl}/auditoria?condominio_id=${condominioId}` : `${this.baseUrl}/auditoria`;
    return this.http.get<LogAuditoria[]>(url);
  }

  getDocumentos(condominioId?: string, pastaId?: string): Observable<Documento[]> {
    let url = `${this.baseUrl}/documentos?`;
    if (condominioId) url += `condominio_id=${condominioId}&`;
    if (pastaId) url += `pasta_id=${pastaId}`;
    return this.http.get<Documento[]>(url);
  }

  criarAssembleia(assembleia: Partial<Assembleia>, condominioId?: string): Observable<Assembleia> {
    const url = condominioId ? `${this.baseUrl}/assembleias?condominio_id=${condominioId}` : `${this.baseUrl}/assembleias`;
    return this.http.post<Assembleia>(url, assembleia);
  }
}
