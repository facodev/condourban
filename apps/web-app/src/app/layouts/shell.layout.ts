import { Component, computed, inject, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'cu-shell-layout',
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
  ],
  styles: `
    .shell {
      min-height: 100vh;
      background:
        radial-gradient(ellipse at top left, color-mix(in srgb, var(--color-brand-soft) 80%, transparent), transparent 55%),
        linear-gradient(180deg, #eef3f1 0%, var(--color-surface) 40%);
    }
    mat-toolbar {
      background: var(--color-drawer);
      color: var(--color-drawer-ink);
    }
    .brand {
      font-weight: 700;
      letter-spacing: 0.02em;
      margin-right: 1rem;
    }
    .spacer {
      flex: 1;
    }
    .content {
      padding: 1rem;
    }
    a.active {
      color: var(--color-brand);
      font-weight: 600;
    }
    .meta {
      font-size: var(--text-sm);
      opacity: 0.85;
    }
  `,
  template: `
    <div class="shell">
      <mat-toolbar>
        <span class="brand">CondoUrban</span>
        <span class="meta">{{ condoLabel() }}</span>
        <span class="spacer"></span>
        <span class="meta">{{ auth.me()?.nome_completo || auth.me()?.email }}</span>
        <button mat-button type="button" (click)="auth.logout()">Sair</button>
      </mat-toolbar>

      <mat-sidenav-container>
        <mat-sidenav mode="side" opened>
          <mat-nav-list>
            <a mat-list-item routerLink="/inicio" routerLinkActive="active">Início</a>
            <a mat-list-item routerLink="/comunicados" routerLinkActive="active">Comunicados</a>
            <a mat-list-item routerLink="/documentos" routerLinkActive="active">Documentos</a>
            <a mat-list-item routerLink="/ocorrencias" routerLinkActive="active">Ocorrências</a>
          </mat-nav-list>
        </mat-sidenav>
        <mat-sidenav-content>
          <div class="content">
            <router-outlet />
          </div>
        </mat-sidenav-content>
      </mat-sidenav-container>
    </div>
  `,
})
export class ShellLayout implements OnInit {
  readonly auth = inject(AuthService);

  readonly condoLabel = computed(() => {
    const id = this.auth.condominioId();
    const found = this.auth.condominios().find((c) => c.id === id);
    if (!found) {
      return 'Sem condomínio';
    }
    return `${found.nome} · ${found.papel}`;
  });

  ngOnInit() {
    if (!this.auth.me()) {
      this.auth.loadSession().subscribe();
    }
    if (!this.auth.condominios().length) {
      this.auth.loadCondominios().subscribe();
    }
  }
}
