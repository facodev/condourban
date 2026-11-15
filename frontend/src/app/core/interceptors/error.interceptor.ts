import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../../features/auth/services/auth.service';
import { NotificationService } from '../services/notification.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const notificationService = inject(NotificationService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (!navigator.onLine || error.status === 0) {
        notificationService.addNotification({
          title: 'Sem conexão',
          body: 'Você está offline. As ações serão sincronizadas quando restabelecer a rede.',
          type: 'warning'
        });
      } else if (error.status === 401) {
        authService.logout();
        router.navigate(['/auth/login']);
      } else if (error.status === 403) {
        notificationService.addNotification({
          title: 'Acesso Negado',
          body: 'Seu perfil não possui permissão para executar esta ação.',
          type: 'error'
        });
      } else if (error.status >= 500) {
        notificationService.addNotification({
          title: 'Erro no Servidor',
          body: 'Ocorreu um erro interno. Tente novamente mais tarde.',
          type: 'error'
        });
      }

      return throwError(() => error);
    })
  );
};