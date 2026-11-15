import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Me {
  id: string;
  email: string;
  email_verificado: boolean;
  pessoa_id: string | null;
  nome_completo: string | null;
}

export interface CondominioResumo {
  id: string;
  nome: string;
  papel: string;
  tipo_pessoa: string;
  cidade: string | null;
  uf: string | null;
}

const ACCESS_KEY = 'cu_access';
const REFRESH_KEY = 'cu_refresh';
const CONDO_KEY = 'cu_condo';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  private readonly access = signal<string | null>(localStorage.getItem(ACCESS_KEY));
  private readonly refresh = signal<string | null>(localStorage.getItem(REFRESH_KEY));
  private readonly condo = signal<string | null>(localStorage.getItem(CONDO_KEY));
  readonly me = signal<Me | null>(null);
  readonly condominios = signal<CondominioResumo[]>([]);

  readonly accessToken = computed(() => this.access());
  readonly condominioId = computed(() => this.condo());
  readonly isAuthenticated = computed(() => !!this.access());
  readonly papelAtual = computed(() => {
    const id = this.condo();
    return this.condominios().find((c) => c.id === id)?.papel ?? null;
  });

  login(email: string, senha: string) {
    return this.http
      .post<TokenPair>(`${environment.apiBaseUrl}/auth/login`, { email, senha })
      .pipe(tap((tokens) => this.persistTokens(tokens)));
  }

  loadSession() {
    return this.http.get<Me>(`${environment.apiBaseUrl}/me`).pipe(
      tap((me) => this.me.set(me)),
    );
  }

  loadCondominios() {
    return this.http
      .get<CondominioResumo[]>(`${environment.apiBaseUrl}/me/condominios`)
      .pipe(
        tap((list) => {
          this.condominios.set(list);
          if (!this.condo() && list.length) {
            this.setCondominio(list[0].id);
          }
        }),
      );
  }

  setCondominio(id: string) {
    this.condo.set(id);
    localStorage.setItem(CONDO_KEY, id);
  }

  logout() {
    this.access.set(null);
    this.refresh.set(null);
    this.me.set(null);
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    void this.router.navigateByUrl('/login');
  }

  private persistTokens(tokens: TokenPair) {
    this.access.set(tokens.access_token);
    this.refresh.set(tokens.refresh_token);
    localStorage.setItem(ACCESS_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_KEY, tokens.refresh_token);
  }
}
