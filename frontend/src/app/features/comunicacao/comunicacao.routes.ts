import { Routes } from '@angular/router';
import { MensageriaComponent } from './components/mensageria/mensageria.component';
import { OcorrenciasComponent } from './components/ocorrencias/ocorrencias.component';
import { MuralSocialComponent } from './components/mural-social/mural-social.component';

export const COMUNICACAO_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'mensageria',
    pathMatch: 'full'
  },
  {
    path: 'mensageria',
    component: MensageriaComponent
  },
  {
    path: 'ocorrencias',
    component: OcorrenciasComponent
  },
  {
    path: 'mural-social',
    component: MuralSocialComponent
  }
];
