import { Component, inject, OnInit, signal } from '@angular/core';
import { MatListModule } from '@angular/material/list';
import { ApiService } from '../../core/api.service';

interface Documento {
  id: string;
  nome: string;
  tipo_mime: string | null;
}

@Component({
  selector: 'cu-documentos-page',
  imports: [MatListModule],
  template: `
    <section class="cu-page">
      <h1>Documentos</h1>
      <mat-nav-list>
        @for (doc of items(); track doc.id) {
          <a mat-list-item>
            <span matListItemTitle>{{ doc.nome }}</span>
            <span matListItemLine>{{ doc.tipo_mime || 'arquivo' }}</span>
          </a>
        } @empty {
          <p class="cu-muted">Biblioteca vazia no momento.</p>
        }
      </mat-nav-list>
    </section>
  `,
})
export class DocumentosPage implements OnInit {
  private readonly api = inject(ApiService);
  readonly items = signal<Documento[]>([]);

  ngOnInit() {
    this.api.get<Documento[]>('/documentos').subscribe((rows) => this.items.set(rows));
  }
}
