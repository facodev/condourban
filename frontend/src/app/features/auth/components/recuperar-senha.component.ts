import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-recuperar-senha',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './recuperar-senha.component.html',
  styleUrls: ['./recuperar-senha.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class RecuperarSenhaComponent {
  email = '';
  loading = signal<boolean>(false);
  emailSent = signal<boolean>(false);

  enviarInstrucoes(): void {
    if (!this.email) return;
    this.loading.set(true);

    // Simulação do envio de e-mail de recuperação
    setTimeout(() => {
      this.loading.set(false);
      this.emailSent.set(true);
    }, 1000);
  }
}
