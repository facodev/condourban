import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SessionService } from '../services/session.service';

export const unidadeGuard: CanActivateFn = () => {
  const sessionService = inject(SessionService);
  const router = inject(Router);

  if (sessionService.unidadeAtiva()) {
    return true;
  }

  // Redireciona para seleção de unidade / condomínio se nenhuma estiver selecionada
  return router.createUrlTree(['/condominio']);
};
