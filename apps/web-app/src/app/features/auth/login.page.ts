import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { switchMap } from 'rxjs';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'cu-login-page',
  imports: [
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  styles: `
    .wrap {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 1rem;
      background:
        linear-gradient(135deg, var(--color-brand-strong), var(--color-brand) 45%, #1e2a28);
    }
    mat-card {
      width: min(420px, 100%);
      padding: 1.5rem;
    }
    h1 {
      margin: 0 0 0.25rem;
      font-size: 1.75rem;
      color: var(--color-brand-strong);
    }
    p {
      margin: 0 0 1.25rem;
      color: var(--color-ink-muted);
    }
    form {
      display: grid;
      gap: 0.75rem;
    }
    .error {
      color: var(--color-danger);
      font-size: var(--text-sm);
    }
  `,
  template: `
    <div class="wrap">
      <mat-card>
        <h1>CondoUrban</h1>
        <p>Entre para acessar o condomínio.</p>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field appearance="outline">
            <mat-label>E-mail</mat-label>
            <input matInput type="email" formControlName="email" autocomplete="username" />
          </mat-form-field>
          <mat-form-field appearance="outline">
            <mat-label>Senha</mat-label>
            <input
              matInput
              type="password"
              formControlName="senha"
              autocomplete="current-password"
            />
          </mat-form-field>
          @if (error()) {
            <div class="error" role="alert">{{ error() }}</div>
          }
          <button mat-flat-button color="primary" type="submit" [disabled]="form.invalid || loading()">
            Entrar
          </button>
        </form>
      </mat-card>
    </div>
  `,
})
export class LoginPage {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  readonly form = this.fb.nonNullable.group({
    email: ['morador@example.com', [Validators.required, Validators.email]],
    senha: ['Demo@1234', [Validators.required, Validators.minLength(8)]],
  });

  submit() {
    if (this.form.invalid) {
      return;
    }
    this.loading.set(true);
    this.error.set(null);
    const { email, senha } = this.form.getRawValue();
    this.auth
      .login(email, senha)
      .pipe(
        switchMap(() => this.auth.loadSession()),
        switchMap(() => this.auth.loadCondominios()),
      )
      .subscribe({
        next: () => {
          this.loading.set(false);
          void this.router.navigateByUrl('/inicio');
        },
        error: () => {
          this.loading.set(false);
          this.error.set('Não foi possível entrar. Verifique e-mail e senha.');
        },
      });
  }
}
