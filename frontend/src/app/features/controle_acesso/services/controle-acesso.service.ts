import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  DispositivoAcesso,
  CredencialAcesso,
  EventoAcesso,
  SincronizacaoAcesso
} from '../models/controle-acesso.model';

export * from '../models/controle-acesso.model';

@Injectable({
  providedIn: 'root'
})
export class ControleAcessoService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/controle-acesso`;

  getDispositivos(): Observable<DispositivoAcesso[]> {
    return this.http.get<DispositivoAcesso[]>(`${this.baseUrl}/dispositivos`);
  }

  getCredenciais(): Observable<CredencialAcesso[]> {
    return this.http.get<CredencialAcesso[]>(`${this.baseUrl}/credenciais`);
  }

  getEventos(): Observable<EventoAcesso[]> {
    return this.http.get<EventoAcesso[]>(`${this.baseUrl}/eventos`);
  }

  sincronizarDispositivo(id: string): Observable<void> {
    return this.http.post<void>(`${this.baseUrl}/dispositivos/${id}/sincronizar`, {});
  }
}
