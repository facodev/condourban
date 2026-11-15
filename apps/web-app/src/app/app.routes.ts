import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login.page').then((m) => m.LoginPage),
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./layouts/shell.layout').then((m) => m.ShellLayout),
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'inicio' },
      {
        path: 'inicio',
        loadComponent: () =>
          import('./features/home/home.page').then((m) => m.HomePage),
      },
      {
        path: 'comunicados',
        loadComponent: () =>
          import('./features/communication/comunicados.page').then(
            (m) => m.ComunicadosPage,
          ),
      },
      {
        path: 'documentos',
        loadComponent: () =>
          import('./features/documents/documentos.page').then(
            (m) => m.DocumentosPage,
          ),
      },
      {
        path: 'ocorrencias',
        loadComponent: () =>
          import('./features/tickets/ocorrencias.page').then(
            (m) => m.OcorrenciasPage,
          ),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
