import { Routes } from '@angular/router';
import { LoginComponent } from './components/login.component';
import { SocialCallbackComponent } from './components/social-callback.component';
import { RecuperarSenhaComponent } from './components/recuperar-senha.component';

export const AUTENTICACAO_ROUTES: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'recuperar-senha',
    component: RecuperarSenhaComponent
  },
  {
    path: 'callback',
    component: SocialCallbackComponent
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  }
];

export const AUTH_ROUTES = AUTENTICACAO_ROUTES;