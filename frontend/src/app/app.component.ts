import { Component, ViewEncapsulation, inject } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { MatRipple } from '@angular/material/core';
import { PwaSyncService } from './core/services/pwa-sync.service';
import { AuthService } from './features/auth/services/auth.service';
import { SessionService } from './core/services/session.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, MatRipple],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class AppComponent {
  readonly pwaService = inject(PwaSyncService);
  readonly authService = inject(AuthService);
  readonly sessionService = inject(SessionService);

  podeAcessar(modulo: string): boolean {
    const papeis = this.sessionService.papeisAtivos().map(p => String(p).toUpperCase());
    const isGestao = papeis.some(p =>
      ['SINDICO', 'SUBSINDICO', 'ADMIN', 'ADMINISTRADOR', 'ADMINISTRADORA', 'SUPERADMIN'].includes(p)
    );
    if (isGestao) return true;

    const isPortaria = papeis.some(p => p === 'PORTARIA' || p === 'PORTEIRO' || p === 'FUNCIONARIO');
    const isEncomendas = papeis.some(p => p === 'ENCOMENDAS' || p === 'ZELADOR');
    if (isPortaria || isEncomendas) {
      // Guarita / correspondências: sem estrutura patrimonial
      return ['portaria', 'controle-acesso', 'identidade', 'comunicacao'].includes(modulo);
    }

    const isConselho = papeis.some(p => p === 'CONSELHO' || p === 'CONSELHEIRO');
    if (isConselho) {
      return ['governanca', 'financeiro', 'comunicacao'].includes(modulo);
    }

    // Morador: consulta de encomendas da unidade + módulos habituais (sem catálogo de apartamentos)
    return ['comunicacao', 'reservas', 'identidade', 'financeiro', 'portaria'].includes(modulo);
  }
}
