import { DatePipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { ApiService } from '../../core/api.service';

interface Comunicado {
  id: string;
  titulo: string;
  conteudo: string;
  status: string;
  publicado_em: string | null;
  lido: boolean;
}

@Component({
  selector: 'cu-comunicados-page',
  imports: [MatListModule, MatButtonModule, DatePipe],
  template: `
    <section class="cu-page">
      <h1>Comunicados</h1>
      <mat-nav-list>
        @for (item of items(); track item.id) {
          <a mat-list-item>
            <span matListItemTitle>{{ item.titulo }}</span>
            <span matListItemLine>{{ item.conteudo }}</span>
            <span matListItemMeta>
              {{ item.publicado_em | date: 'short' }}
              @if (!item.lido) {
                <button mat-button type="button" (click)="marcarLido(item.id); $event.stopPropagation()">
                  Confirmar leitura
                </button>
              } @else {
                Lido
              }
            </span>
          </a>
        } @empty {
          <p class="cu-muted">Nenhum comunicado publicado.</p>
        }
      </mat-nav-list>
    </section>
  `,
})
export class ComunicadosPage implements OnInit {
  private readonly api = inject(ApiService);
  readonly items = signal<Comunicado[]>([]);

  ngOnInit() {
    this.reload();
  }

  marcarLido(id: string) {
    this.api.post(`/comunicados/${id}/leitura`, {}).subscribe({
      next: () => this.reload(),
    });
  }

  private reload() {
    this.api.get<Comunicado[]>('/comunicados').subscribe((rows) => this.items.set(rows));
  }
}
