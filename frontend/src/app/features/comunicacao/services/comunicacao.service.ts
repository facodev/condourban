import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  Comunicado,
  ComunicadoOficial,
  Ocorrencia,
  HistoricoOcorrencia,
  ItemComunidade,
  ItemMuralSocial,
  Enquete,
  MensagemFaleConosco,
  StatusOcorrencia,
  OrigemOcorrencia,
} from '../models/comunicacao.model';

export type {
  Comunicado,
  ComunicadoOficial,
  Ocorrencia,
  HistoricoOcorrencia,
  ItemComunidade,
  ItemMuralSocial,
  Enquete,
  MensagemFaleConosco,
  StatusOcorrencia,
  OrigemOcorrencia,
};

@Injectable({
  providedIn: 'root'
})
export class ComunicacaoService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/comunicacao`;

  getComunicados(condominioId?: string): Observable<ComunicadoOficial[]> {
    const url = condominioId ? `${this.baseUrl}/mensageria?condominio_id=${condominioId}` : `${this.baseUrl}/mensageria`;
    return this.http.get<ComunicadoOficial[]>(url);
  }

  getOcorrencias(condominioId?: string): Observable<Ocorrencia[]> {
    const url = condominioId ? `${this.baseUrl}/ocorrencias?condominio_id=${condominioId}` : `${this.baseUrl}/ocorrencias`;
    return this.http.get<Ocorrencia[]>(url);
  }

  getMuralSocial(condominioId?: string): Observable<ItemMuralSocial[]> {
    const url = condominioId ? `${this.baseUrl}/mural-social?condominio_id=${condominioId}` : `${this.baseUrl}/mural-social`;
    return this.http.get<ItemMuralSocial[]>(url);
  }

  criarComunicado(comunicado: Partial<Comunicado>, condominioId?: string): Observable<Comunicado> {
    const url = condominioId ? `${this.baseUrl}/mensageria?condominio_id=${condominioId}` : `${this.baseUrl}/mensageria`;
    return this.http.post<Comunicado>(url, comunicado);
  }

  registrarOcorrencia(ocorrencia: Partial<Ocorrencia>, condominioId?: string): Observable<Ocorrencia> {
    const url = condominioId ? `${this.baseUrl}/ocorrencias?condominio_id=${condominioId}` : `${this.baseUrl}/ocorrencias`;
    return this.http.post<Ocorrencia>(url, ocorrencia);
  }

  getEnquetes(condominioId?: string): Observable<Enquete[]> {
    const url = condominioId ? `${this.baseUrl}/enquetes?condominio_id=${condominioId}` : `${this.baseUrl}/enquetes`;
    return this.http.get<Enquete[]>(url);
  }
}
