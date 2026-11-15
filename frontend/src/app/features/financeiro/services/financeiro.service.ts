import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  CobrancaCondominial,
  CobrancaBoleto,
  TermoAcordo,
  DespesaCondominial,
  MedicaoIndividual,
  MedicaoConsumo,
  StatusCobranca,
  TipoConsumo,
} from '../models/financeiro.model';

export type {
  CobrancaCondominial,
  CobrancaBoleto,
  TermoAcordo,
  DespesaCondominial,
  MedicaoIndividual,
  MedicaoConsumo,
  StatusCobranca,
  TipoConsumo,
};

@Injectable({
  providedIn: 'root'
})
export class FinanceiroService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/financeiro`;

  getCobrancas(condominioId?: string, unidadeId?: string): Observable<CobrancaBoleto[]> {
    let url = `${this.baseUrl}/cobrancas?`;
    if (condominioId) url += `condominio_id=${condominioId}&`;
    if (unidadeId) url += `unidade_id=${unidadeId}`;
    return this.http.get<CobrancaBoleto[]>(url);
  }

  getMedicoes(condominioId?: string, unidadeId?: string): Observable<MedicaoConsumo[]> {
    let url = `${this.baseUrl}/medicoes?`;
    if (condominioId) url += `condominio_id=${condominioId}&`;
    if (unidadeId) url += `unidade_id=${unidadeId}`;
    return this.http.get<MedicaoConsumo[]>(url);
  }

  getDespesas(condominioId?: string): Observable<DespesaCondominial[]> {
    const url = condominioId ? `${this.baseUrl}/despesas?condominio_id=${condominioId}` : `${this.baseUrl}/despesas`;
    return this.http.get<DespesaCondominial[]>(url);
  }

  getAcordos(condominioId?: string): Observable<TermoAcordo[]> {
    const url = condominioId ? `${this.baseUrl}/acordos?condominio_id=${condominioId}` : `${this.baseUrl}/acordos`;
    return this.http.get<TermoAcordo[]>(url);
  }
}
