import { Component, inject } from '@angular/core';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'cu-home-page',
  template: `
    <section class="cu-page">
      <h1>Olá, {{ auth.me()?.nome_completo || 'morador' }}</h1>
      <p class="cu-muted">
        Fundação CondoUrban — comunicados, documentos e ocorrências.
      </p>
    </section>
  `,
})
export class HomePage {
  readonly auth = inject(AuthService);
}
