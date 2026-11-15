import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Condominio } from '../models/condominio.model';

@Injectable({
  providedIn: 'root'
})
export class BrandingService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/condominio`;

  getInfo(condominioId?: string): Observable<Condominio> {
    const url = condominioId ? `${this.baseUrl}/info?condominio_id=${condominioId}` : `${this.baseUrl}/info`;
    return this.http.get<Condominio>(url);
  }

  updateInfo(dto: Partial<Condominio>, condominioId?: string): Observable<Condominio> {
    const url = condominioId ? `${this.baseUrl}/info?condominio_id=${condominioId}` : `${this.baseUrl}/info`;
    return this.http.put<Condominio>(url, dto);
  }

  getConfiguracoes(condominioId?: string): Observable<any> {
    const url = condominioId ? `${this.baseUrl}/configuracoes?condominio_id=${condominioId}` : `${this.baseUrl}/configuracoes`;
    return this.http.get<any>(url);
  }

  updateConfiguracoes(dto: any, condominioId?: string): Observable<any> {
    const url = condominioId ? `${this.baseUrl}/configuracoes?condominio_id=${condominioId}` : `${this.baseUrl}/configuracoes`;
    return this.http.patch<any>(url, dto);
  }

  getTodosCondominios(): Observable<Condominio[]> {
    return this.http.get<Condominio[]>(`${this.baseUrl}/todos`);
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
    return this.http.post<Condominio>(`${this.baseUrl}/novo`, condo);
  }

  deleteCondominio(id: string): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/condominios/${id}`);
  }
}

