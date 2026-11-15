import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../../../environments/environment';
import { Observable, tap } from 'rxjs';
import { SessionService } from '../../../core/services/session.service';
import { UsuarioSessao, PapelUsuario } from '../../../core/models/usuario-sessao.model';

export interface CondominioVinculado {
  id: string;
  nome: string;
  papel: string;
}

export interface TokenResponse {
  access_token: string;
  token_tipo?: string;
  condominios?: CondominioVinculado[];
  condominio_ativo?: string | null;
  pessoa_id?: string | null;
  unidade_ids?: string[];
}

export interface User {
  id: number | string;
  email: string;
  full_name: string;
  role: string;
}

function parseJwt(token: string): any {
  try {
    const base64Url = token.split('.')[1];
    if (!base64Url) return null;
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly sessionService = inject(SessionService);
  private readonly tokenKey = 'condourban_token';

  readonly token = signal<string | null>(localStorage.getItem(this.tokenKey));
  readonly currentUser = signal<User | null>(null);

  readonly isAuthenticated = computed(() => !!this.token());

  constructor() {
    this.restoreUserFromToken();
  }

  login(credentials: { email: string; password?: string; senha?: string }): Observable<TokenResponse> {
    const payload = {
      email: credentials.email,
      senha: credentials.senha || credentials.password || ''
    };

    return this.http.post<TokenResponse>(
      `${environment.apiUrl}/auth/login`,
      payload
    ).pipe(
      tap((res) => {
        this.token.set(res.access_token);
        localStorage.setItem(this.tokenKey, res.access_token);
        this.syncSessionWithToken(res.access_token, res);
      })
    );
  }

  logout(): void {
    this.token.set(null);
    this.currentUser.set(null);
    localStorage.removeItem(this.tokenKey);
    this.sessionService.clearSession();
    this.router.navigate(['/auth/login']);
  }

  hasRole(role: string): boolean {
    return this.currentUser()?.role === role || this.sessionService.hasRole(role as PapelUsuario);
  }

  private restoreUserFromToken(): void {
    const currentToken = this.token();
    if (currentToken) {
      this.syncSessionWithToken(currentToken);
    }
  }

  private syncSessionWithToken(token: string, tokenResponse?: TokenResponse): void {
    const payload = parseJwt(token);
    if (!payload) return;

    const papeis: PapelUsuario[] = (payload.papeis || []).map((p: string) => p as PapelUsuario);
    const role = papeis[0] || 'morador';

    const user: User = {
      id: payload.sub,
      email: payload.email || '',
      full_name: payload.email ? payload.email.split('@')[0] : 'Usuário',
      role: String(role)
    };
    this.currentUser.set(user);

    const condoId = tokenResponse?.condominio_ativo || payload.condominio_id || tokenResponse?.condominios?.[0]?.id;
    const condoNome = tokenResponse?.condominios?.[0]?.nome || 'Condomínio Residencial Jardins';

    const unidadeIds: string[] = (
      tokenResponse?.unidade_ids ||
      payload.unidade_ids ||
      []
    ).map((u: string) => String(u));
    const pessoaId =
      tokenResponse?.pessoa_id || payload.pessoa_id || null;
    const unidadePrincipalId = unidadeIds[0] || condoId;

    const usuarioSessao: UsuarioSessao = {
      id: payload.sub,
      email: payload.email || '',
      nomeCompleto: user.full_name,
      papeis: papeis.length > 0 ? papeis : [role],
      pessoaId: pessoaId != null ? String(pessoaId) : null,
      unidadeIds,
      unidadeAtiva: unidadePrincipalId ? {
        id: unidadePrincipalId,
        condominioId: condoId || unidadePrincipalId,
        condominioNome: condoNome,
        numero: '—',
        papel: role,
      } : undefined,
      unidadesDisponiveis: unidadeIds.length
        ? unidadeIds.map((uid) => ({
            id: uid,
            condominioId: condoId || uid,
            condominioNome: condoNome,
            numero: '—',
            papel: role,
          }))
        : (tokenResponse?.condominios || []).map((c) => ({
            id: c.id,
            condominioId: c.id,
            condominioNome: c.nome,
            numero: '—',
            papel: (c.papel as PapelUsuario) || role,
          })),
    };

    this.sessionService.setUsuario(usuarioSessao);
  }
}
