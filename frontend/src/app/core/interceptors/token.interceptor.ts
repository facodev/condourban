import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../../features/auth/services/auth.service';
import { SessionService } from '../services/session.service';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const sessionService = inject(SessionService);

  const token = authService.token();
  const condominioId = sessionService.condominioAtivoId();

  const headers: Record<string, string> = {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (condominioId) {
    headers['X-Condominio-Id'] = String(condominioId);
    headers['X-Tenant-Id'] = String(condominioId);
  }

  if (Object.keys(headers).length > 0) {
    const cloned = req.clone({ setHeaders: headers });
    return next(cloned);
  }

  return next(req);
};
