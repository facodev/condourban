import { Component, OnInit, inject, signal, ViewEncapsulation } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CondominioService, Bloco } from '../../services/condominio.service';
import { ButtonComponent } from '../../../../shared/components/button.component';

@Component({
  selector: 'app-unit-form',
  standalone: true,
  imports: [FormsModule, RouterLink, ButtonComponent],
  templateUrl: './unit-form.component.html',
  styleUrls: ['./unit-form.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class UnitFormComponent implements OnInit {
  private readonly service = inject(CondominioService);
  private readonly router = inject(Router);

  readonly blocos = signal<Bloco[]>([]);

  identificacao = '';
  blocoId = '';
  andar = '';
  tipo = 'APARTAMENTO';

  isLoading = signal<boolean>(false);
  errorMessage = signal<string>('');

  ngOnInit(): void {
    this.service.getBlocks().subscribe({
      next: (dados) => this.blocos.set(dados),
      error: (e) => console.warn('Erro ao carregar blocos:', e)
    });
  }

  save(): void {
    if (!this.identificacao.trim()) return;

    this.isLoading.set(true);
    this.errorMessage.set('');

    const payload = {
      identificacao: this.identificacao.trim(),
      bloco_id: this.blocoId || undefined,
      andar: this.andar.trim() || undefined,
      tipo: this.tipo
    };

    this.service.createUnit(payload).subscribe({
      next: () => {
        this.isLoading.set(false);
        this.router.navigate(['/condominio']);
      },
      error: (err) => {
        this.isLoading.set(false);
        const detail = err?.error?.detail;
        if (detail === 'UNIDADE_DUPLICADA' || err?.status === 400) {
          this.errorMessage.set('Já existe uma unidade com este número/identificador neste bloco.');
        } else {
          this.errorMessage.set(detail || 'Erro ao cadastrar unidade. Verifique os dados fornecidos.');
        }
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/condominio']);
  }
}
