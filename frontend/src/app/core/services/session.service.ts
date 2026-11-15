import { Injectable, computed, signal } from '@angular/core';
import { PapelUsuario, UnidadeContexto, UsuarioSessao } from '../models/usuario-sessao.model';

@Injectable({
  providedIn: 'root'
})
export class SessionService {
  private readonly sessionKey = 'condourban_session';
  private readonly condoOverrideKey = 'condourban_condominio_override';
  private readonly condoOverrideNomeKey = 'condourban_condominio_override_nome';

  readonly usuario = signal<UsuarioSessao | null>(this.loadStoredSession());
  readonly unidadeAtiva = signal<UnidadeContexto | null>(this.usuario()?.unidadeAtiva ?? null);
  readonly condominioOverrideId = signal<string | null>(this.loadStoredCondoOverride());
  readonly condominioOverrideNome = signal<string | null>(this.loadStoredCondoOverrideNome());

  readonly isAuthenticated = computed(() => !!this.usuario());
  readonly condominioAtivoId = computed<string | null>(() => {
    const val = this.condominioOverrideId() ?? this.unidadeAtiva()?.condominioId ?? null;
    return val != null ? String(val) : null;
  });
  readonly condominioAtivoNome = computed(() => {
    return this.condominioOverrideNome() ?? this.unidadeAtiva()?.condominioNome ?? 'Condomínio Residencial Jardins';
  });
  readonly papeisAtivos = computed<PapelUsuario[]>(() => this.usuario()?.papeis ?? []);

  readonly isSuperAdmin = computed(() => {
    return this.papeisAtivos().some(p => {
      const pl = String(p).toLowerCase();
      return pl === 'superadmin' || pl === 'administrador' || pl === 'admin';
    });
  });

  setCondominio(condo: { id: string; nome: string } | null): void {
    if (condo) {
      this.condominioOverrideId.set(condo.id);
      this.condominioOverrideNome.set(condo.nome);
      localStorage.setItem(this.condoOverrideKey, condo.id);
      localStorage.setItem(this.condoOverrideNomeKey, condo.nome);
    } else {
      this.condominioOverrideId.set(null);
      this.condominioOverrideNome.set(null);
      localStorage.removeItem(this.condoOverrideKey);
      localStorage.removeItem(this.condoOverrideNomeKey);
    }
  }

  setCondominioId(condoId: string | null, condoNome?: string): void {
    this.condominioOverrideId.set(condoId);
    if (condoNome) {
      this.condominioOverrideNome.set(condoNome);
      localStorage.setItem(this.condoOverrideNomeKey, condoNome);
    }
    if (condoId) {
      localStorage.setItem(this.condoOverrideKey, condoId);
    } else {
      localStorage.removeItem(this.condoOverrideKey);
      localStorage.removeItem(this.condoOverrideNomeKey);
    }
  }

  private loadStoredCondoOverride(): string | null {
    try {
      return localStorage.getItem(this.condoOverrideKey);
    } catch {
      return null;
    }
  }

  private loadStoredCondoOverrideNome(): string | null {
    try {
      return localStorage.getItem(this.condoOverrideNomeKey);
    } catch {
      return null;
    }
  }

  setUsuario(usuario: UsuarioSessao | null): void {
    this.usuario.set(usuario);
    if (usuario) {
      this.unidadeAtiva.set(usuario.unidadeAtiva ?? usuario.unidadesDisponiveis[0] ?? null);
      localStorage.setItem(this.sessionKey, JSON.stringify(usuario));
    } else {
      this.unidadeAtiva.set(null);
      this.condominioOverrideId.set(null);
      this.condominioOverrideNome.set(null);
      localStorage.removeItem(this.sessionKey);
      localStorage.removeItem(this.condoOverrideKey);
      localStorage.removeItem(this.condoOverrideNomeKey);
    }
  }

  selecionarUnidade(unidade: UnidadeContexto): void {
    this.unidadeAtiva.set(unidade);
    const atual = this.usuario();
    if (atual) {
      const atualizado = { ...atual, unidadeAtiva: unidade };
      this.usuario.set(atualizado);
      localStorage.setItem(this.sessionKey, JSON.stringify(atualizado));
    }
  }

  hasRole(role: PapelUsuario): boolean {
    const roleLower = String(role).toLowerCase();
    const matches = (p: string) => {
      const pl = String(p).toLowerCase();
      if (pl === roleLower) return true;
      if ((roleLower === 'admin' || roleLower === 'sindico') && (pl === 'administrador' || pl === 'admin' || pl === 'sindico')) return true;
      if (roleLower === 'porteiro' && (pl === 'funcionario' || pl === 'porteiro')) return true;
      return false;
    };
    return this.papeisAtivos().some(matches) || (this.unidadeAtiva()?.papel ? matches(this.unidadeAtiva()!.papel) : false);
  }

  hasAnyRole(roles: PapelUsuario[]): boolean {
    return roles.some(r => this.hasRole(r));
  }

  /** Gestão de contas/RBAC: síndico, admin e administradora — não morador/portaria. */
  podeGerenciarUsuarios(): boolean {
    const papeis = this.papeisAtivos().map((p) => String(p).toUpperCase());
    return papeis.some((p) =>
      [
        'SINDICO',
        'SUBSINDICO',
        'ADMIN',
        'ADMINISTRADOR',
        'ADMINISTRADORA',
        'SUPERADMIN',
      ].includes(p)
    );
  }

  /** Consulta ampla (inclui portaria/encomendas/conselho) — ver todos os cadastros. */
  podeVerTodosCadastros(): boolean {
    const papeis = this.papeisAtivos().map((p) => String(p).toUpperCase());
    return papeis.some((p) =>
      [
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
        'CONSELHO',
        'PORTARIA',
        'PORTEIRO',
        'ENCOMENDAS',
        'FUNCIONARIO',
        'ZELADOR',
      ].includes(p)
    );
  }

  /** Recebimento e baixa de correspondências (não libera visitantes). */
  podeOperarEncomendas(): boolean {
    const papeis = this.papeisAtivos().map((p) => String(p).toUpperCase());
    return papeis.some((p) =>
      [
        'ENCOMENDAS',
        'ZELADOR',
        'SINDICO',
        'SUBSINDICO',
        'ADMIN',
        'ADMINISTRADOR',
        'ADMINISTRADORA',
        'SUPERADMIN',
      ].includes(p)
    );
  }

  /** Liberação de entrada / visitantes (não opera pacotes). */
  podeOperarVisitantes(): boolean {
    const papeis = this.papeisAtivos().map((p) => String(p).toUpperCase());
    return papeis.some((p) =>
      [
        'PORTARIA',
        'PORTEIRO',
        'SINDICO',
        'SUBSINDICO',
        'ADMIN',
        'ADMINISTRADOR',
        'ADMINISTRADORA',
        'SUPERADMIN',
      ].includes(p)
    );
  }

  /** Morador: só dados da própria unidade. */
  escopoSomenteUnidade(): boolean {
    return !this.podeVerTodosCadastros();
  }

  /**
   * Mutações sensíveis (criar/excluir pessoa, vínculo, estrutura, CPF/nome civil).
   * Só síndico e administrador — portaria NÃO edita.
   */
  podeGerenciarCadastros(): boolean {
    const papeis = this.papeisAtivos().map((p) => String(p).toUpperCase());
    return papeis.some((p) =>
      [
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
      ].includes(p)
    );
  }

  /** Nome civil, CPF e status — idêntico à gestão plena. */
  podeEditarDadosCivis(): boolean {
    return this.podeGerenciarCadastros();
  }

  unidadeIdsEscopo(): string[] {
    return (this.usuario()?.unidadeIds ?? []).map(String);
  }

  pessoaIdSessao(): string | null {
    const id = this.usuario()?.pessoaId;
    return id != null ? String(id) : null;
  }

  clearSession(): void {
    this.setUsuario(null);
  }

  private loadStoredSession(): UsuarioSessao | null {
    try {
      const item = localStorage.getItem(this.sessionKey);
      return item ? JSON.parse(item) : null;
    } catch {
      return null;
    }
  }
}
