import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { ApiService } from '../../core/api.service';

interface Ocorrencia {
  id: string;
  titulo: string;
  descricao: string;
  status: string;
  prioridade: string;
}

@Component({
  selector: 'cu-ocorrencias-page',
  imports: [
    ReactiveFormsModule,
    MatListModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  styles: `
    form {
      display: grid;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
  `,
  template: `
    <section class="cu-page">
      <h1>Ocorrências</h1>
      <form [formGroup]="form" (ngSubmit)="criar()">
        <mat-form-field appearance="outline">
          <mat-label>Título</mat-label>
          <input matInput formControlName="titulo" />
        </mat-form-field>
        <mat-form-field appearance="outline">
          <mat-label>Descrição</mat-label>
          <textarea matInput rows="3" formControlName="descricao"></textarea>
        </mat-form-field>
        <button mat-flat-button color="primary" type="submit" [disabled]="form.invalid">
          Abrir ocorrência
        </button>
      </form>

      <mat-nav-list>
        @for (item of items(); track item.id) {
          <a mat-list-item>
            <span matListItemTitle>{{ item.titulo }}</span>
            <span matListItemLine>{{ item.descricao }}</span>
            <span matListItemMeta>{{ item.status }} · {{ item.prioridade }}</span>
          </a>
        } @empty {
          <p class="cu-muted">Nenhuma ocorrência ainda.</p>
        }
      </mat-nav-list>
    </section>
  `,
})
export class OcorrenciasPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);
  readonly items = signal<Ocorrencia[]>([]);

  readonly form = this.fb.nonNullable.group({
    titulo: ['', Validators.required],
    descricao: ['', Validators.required],
  });

  ngOnInit() {
    this.reload();
  }

  criar() {
    if (this.form.invalid) {
      return;
    }
    this.api.post<Ocorrencia>('/ocorrencias', this.form.getRawValue()).subscribe({
      next: () => {
        this.form.reset();
        this.reload();
      },
    });
  }

  private reload() {
    this.api.get<Ocorrencia[]>('/ocorrencias').subscribe((rows) => this.items.set(rows));
  }
}
