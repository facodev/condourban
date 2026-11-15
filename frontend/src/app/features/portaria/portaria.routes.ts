import { Routes } from '@angular/router';
import { AtendimentoComponent } from './components/atendimento/atendimento.component';
import { EncomendasComponent } from './components/encomendas/encomendas.component';

export const PORTARIA_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'encomendas',
    pathMatch: 'full'
  },
  {
    path: 'atendimento',
    component: AtendimentoComponent
  },
  {
    path: 'encomendas',
    component: EncomendasComponent
  }
];
