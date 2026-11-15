import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  Reserva,
  AgendamentoReserva,
  VistoriaReserva,
  ConvidadoReserva,
  StatusReserva,
  TipoVistoria,
} from '../models/reservas.model';

export type {
  Reserva,
  AgendamentoReserva,
  VistoriaReserva,
  ConvidadoReserva,
  StatusReserva,
  TipoVistoria,
};

@Injectable({
  providedIn: 'root'
})
export class ReservasService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/reservas`;

  getAgendamentos(condominioId?: string): Observable<Reserva[]> {
    const url = condominioId ? `${this.baseUrl}?condominio_id=${condominioId}` : this.baseUrl;
    return this.http.get<Reserva[]>(url);
  }

  getReservas(condominioId?: string): Observable<Reserva[]> {
    return this.getAgendamentos(condominioId);
  }

  getVistorias(condominioId?: string): Observable<VistoriaReserva[]> {
    const url = condominioId ? `${this.baseUrl}/vistorias?condominio_id=${condominioId}` : `${this.baseUrl}/vistorias`;
    return this.http.get<VistoriaReserva[]>(url);
  }

  solicitarReserva(reserva: Partial<Reserva>, condominioId?: string): Observable<Reserva> {
    const url = condominioId ? `${this.baseUrl}?condominio_id=${condominioId}` : this.baseUrl;
    return this.http.post<Reserva>(url, reserva);
  }

  adicionarConvidado(reservaId: string, convidado: Partial<ConvidadoReserva>): Observable<ConvidadoReserva> {
    return this.http.post<ConvidadoReserva>(`${this.baseUrl}/${reservaId}/convidados`, convidado);
  }
}
