import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { SessionService } from '../services/session.service';
import { PapelUsuario } from '../models/usuario-sessao.model';

export const papelGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const sessionService = inject(SessionService);
  const router = inject(Router);

  const papeisPermitidos = (route.data?.['papeis'] as PapelUsuario[]) || [];

  if (papeisPermitidos.length === 0) {
    return true;
  }

  if (sessionService.hasAnyRole(papeisPermitidos)) {
    return true;
  }

  // Redireciona para página inicial ou acesso não autorizado
  return router.createUrlTree(['/comunicacao']);
};
