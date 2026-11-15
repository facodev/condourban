import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'comunicacao',
        pathMatch: 'full'
    },
    {
        path: 'auth',
        loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTENTICACAO_ROUTES)
    },
    {
        path: '',
        canActivate: [authGuard],
        children: [
            {
                path: 'identidade-cadastro',
                loadChildren: () => import('./features/identidade_cadastro/identidade-cadastro.routes').then(m => m.IDENTIDADE_CADASTRO_ROUTES)
            },
            {
                path: 'condominio',
                loadChildren: () => import('./features/condominio/condominio.routes').then(m => m.CONDOMINIO_ROUTES)
            },
            {
                path: 'controle-acesso',
                loadChildren: () => import('./features/controle_acesso/controle-acesso.routes').then(m => m.CONTROLE_ACESSO_ROUTES)
            },
            {
                path: 'portaria',
                loadChildren: () => import('./features/portaria/portaria.routes').then(m => m.PORTARIA_ROUTES)
            },
            {
                path: 'reservas',
                loadChildren: () => import('./features/reservas/reservas.routes').then(m => m.RESERVAS_ROUTES)
            },
            {
                path: 'comunicacao',
                loadChildren: () => import('./features/comunicacao/comunicacao.routes').then(m => m.COMUNICACAO_ROUTES)
            },
            {
                path: 'governanca',
                loadChildren: () => import('./features/governanca/governanca.routes').then(m => m.GOVERNANCA_ROUTES)
            },
            {
                path: 'financeiro',
                loadChildren: () => import('./features/financeiro/financeiro.routes').then(m => m.FINANCEIRO_ROUTES)
            },
            {
                path: 'manutencao',
                loadChildren: () => import('./features/manutencao/manutencao.routes').then(m => m.MANUTENCAO_ROUTES)
            }
        ]
    },
    {
        path: '**',
        redirectTo: 'comunicacao'
    }
];
