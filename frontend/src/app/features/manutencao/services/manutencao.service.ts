import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  ChamadoManutencao,
  ChamadoServico,
  OrdemServico,
  ItemPreventivaPMO,
  ItemInventarioPMO,
  RegistroInspecaoPMO,
  PrioridadeChamado,
  StatusChamado,
  StatusOrdemServico,
} from '../models/manutencao.model';

export type {
  ChamadoManutencao,
  ChamadoServico,
  OrdemServico,
  ItemPreventivaPMO,
  ItemInventarioPMO,
  RegistroInspecaoPMO,
  PrioridadeChamado,
  StatusChamado,
  StatusOrdemServico,
};

@Injectable({
  providedIn: 'root'
})
export class ManutencaoService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/manutencao`;

  getChamados(condominioId?: string): Observable<ChamadoServico[]> {
    const url = condominioId ? `${this.baseUrl}/chamados?condominio_id=${condominioId}` : `${this.baseUrl}/chamados`;
    return this.http.get<ChamadoServico[]>(url);
  }

  getPlanoInventario(condominioId?: string): Observable<ItemInventarioPMO[]> {
    const url = condominioId ? `${this.baseUrl}/inventario?condominio_id=${condominioId}` : `${this.baseUrl}/inventario`;
    return this.http.get<ItemInventarioPMO[]>(url);
  }

  getOrdensServico(condominioId?: string): Observable<OrdemServico[]> {
    const url = condominioId ? `${this.baseUrl}/ordens-servico?condominio_id=${condominioId}` : `${this.baseUrl}/ordens-servico`;
    return this.http.get<OrdemServico[]>(url);
  }

  abrirChamado(chamado: Partial<ChamadoManutencao>, condominioId?: string): Observable<ChamadoManutencao> {
    const url = condominioId ? `${this.baseUrl}/chamados?condominio_id=${condominioId}` : `${this.baseUrl}/chamados`;
    return this.http.post<ChamadoManutencao>(url, chamado);
  }
}
