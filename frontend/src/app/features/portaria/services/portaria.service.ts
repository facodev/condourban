import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../../../environments/environment';
import {
  AtendimentoPortaria,
  PacoteEncomenda,
  AgendamentoMudanca,
  ItemPerdido
} from '../models/portaria.model';

export * from '../models/portaria.model';

interface EncomendaApi {
  id: string;
  condominio_id: string;
  unidade_id: string;
  destinatario_id?: string | null;
  transportadora?: string | null;
  codigo_rastreio?: string | null;
  codigo_retirada?: string | null;
  foto_url?: string | null;
  descricao?: string | null;
  status: string;
  recebida_em?: string | null;
  retirada_em?: string | null;
}

interface VisitanteApi {
  id: string;
  condominio_id: string;
  unidade_id?: string | null;
  nome_completo?: string | null;
  documento?: string | null;
  status: string;
  criado_em: string;
  observacao?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class PortariaService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/portaria`;

  getAtendimentos(condominioId?: string | null): Observable<AtendimentoPortaria[]> {
    let params = new HttpParams();
    if (condominioId) params = params.set('condominio_id', condominioId);
    return this.http.get<VisitanteApi[]>(`${this.baseUrl}/visitantes`, { params }).pipe(
      map((rows) =>
        rows.map((v) => ({
          id: v.id,
          condominioId: v.condominio_id,
          unidadeId: v.unidade_id ?? undefined,
          visitanteNome: v.nome_completo || 'Visitante',
          documento: v.documento ?? undefined,
          tipo: 'visitante',
          unidadeDestino: v.unidade_id ?? undefined,
          status: String(v.status || '').toLowerCase(),
          observacao: v.observacao ?? undefined,
          entradaEm: v.criado_em
        }))
      )
    );
  }

  getEncomendas(condominioId?: string | null): Observable<PacoteEncomenda[]> {
    let params = new HttpParams();
    if (condominioId) params = params.set('condominio_id', condominioId);
    return this.http.get<EncomendaApi[]>(`${this.baseUrl}/encomendas`, { params }).pipe(
      map((rows) => rows.map((e) => this.mapEncomenda(e)))
    );
  }

  criarEncomenda(payload: {
    unidade_id: string;
    transportadora?: string;
    codigo_rastreio?: string;
    descricao?: string;
    destinatario_id?: string;
  }): Observable<PacoteEncomenda> {
    return this.http
      .post<EncomendaApi>(`${this.baseUrl}/encomendas`, payload)
      .pipe(map((e) => this.mapEncomenda(e)));
  }

  darBaixaEncomenda(id: string, codigoRetirada: string): Observable<PacoteEncomenda> {
    return this.http
      .post<EncomendaApi>(`${this.baseUrl}/encomendas/${id}/baixa`, {
        codigo_retirada: codigoRetirada
      })
      .pipe(map((e) => this.mapEncomenda(e)));
  }

  getMudancas(): Observable<AgendamentoMudanca[]> {
    return this.http.get<AgendamentoMudanca[]>(`${this.baseUrl}/mudancas`);
  }

  getItensPerdidos(): Observable<ItemPerdido[]> {
    return this.http.get<ItemPerdido[]>(`${this.baseUrl}/achados-perdidos`);
  }

  private mapEncomenda(e: EncomendaApi): PacoteEncomenda {
    return {
      id: e.id,
      condominioId: e.condominio_id,
      unidadeId: e.unidade_id,
      unidadeDestino: e.unidade_id,
      destinatarioId: e.destinatario_id ?? undefined,
      transportadora: e.transportadora ?? undefined,
      codigoRastreio: e.codigo_rastreio ?? undefined,
      codigoRetirada: e.codigo_retirada ?? undefined,
      fotoUrl: e.foto_url ?? undefined,
      recebidoEm: e.recebida_em ?? undefined,
      retiradoEm: e.retirada_em ?? undefined,
      status: e.status
    };
  }
}
