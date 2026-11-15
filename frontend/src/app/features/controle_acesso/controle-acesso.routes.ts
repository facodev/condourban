import { Routes } from '@angular/router';
import { DispositivosComponent } from './components/dispositivos/dispositivos.component';
import { CredenciaisComponent } from './components/credenciais/credenciais.component';
import { EventosComponent } from './components/eventos/eventos.component';

export const CONTROLE_ACESSO_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'dispositivos',
    pathMatch: 'full'
  },
  {
    path: 'dispositivos',
    component: DispositivosComponent
  },
  {
    path: 'credenciais',
    component: CredenciaisComponent
  },
  {
    path: 'eventos',
    component: EventosComponent
  }
];
