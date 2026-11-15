import { Component, inject, signal, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { ButtonComponent } from '../../../shared/components/button.component';
import { CardComponent } from '../../../shared/components/card.component';

@Component({
  selector: 'app-login',
  imports: [FormsModule, ButtonComponent, CardComponent],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  email = '';
  password = '';
  isLoading = signal<boolean>(false);
  errorMessage = signal<string>('');

  onSubmit(): void {
    if (!this.email || !this.password) return;
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.authService.login({ email: this.email, password: this.password }).subscribe({
      next: () => {
        this.isLoading.set(false);
        this.router.navigate(['/condominio']);
      },
      error: () => {
        this.isLoading.set(false);
        this.errorMessage.set('Falha na autenticação. Verifique suas credenciais.');
      }
    });
  }

  loginGoogle(): void {
    console.log('Iniciar OAuth Google');
  }

  loginInstagram(): void {
    console.log('Iniciar OAuth Instagram');
  }
}