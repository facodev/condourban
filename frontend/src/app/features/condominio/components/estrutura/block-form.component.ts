import { Component, inject, signal, ViewEncapsulation } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CondominioService } from '../../services/condominio.service';
import { ButtonComponent } from '../../../../shared/components/button.component';

@Component({
  selector: 'app-block-form',
  standalone: true,
  imports: [FormsModule, RouterLink, ButtonComponent],
  templateUrl: './block-form.component.html',
  styleUrls: ['./block-form.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class BlockFormComponent {
  private readonly service = inject(CondominioService);
  private readonly router = inject(Router);

  nome = '';
  descricao = '';
  isLoading = signal<boolean>(false);
  errorMessage = signal<string>('');

  save(): void {
    if (!this.nome.trim()) return;

    this.isLoading.set(true);
    this.errorMessage.set('');

    this.service.createBlock({
      nome: this.nome.trim(),
      descricao: this.descricao.trim() || undefined
    }).subscribe({
      next: () => {
        this.isLoading.set(false);
        this.router.navigate(['/condominio']);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(err?.error?.detail || 'Erro ao cadastrar o bloco. Verifique os dados.');
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/condominio']);
  }
}
