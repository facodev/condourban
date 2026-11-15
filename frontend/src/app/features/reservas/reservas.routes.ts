import { Routes } from '@angular/router';
import { AgendamentosComponent } from './components/agendamentos/agendamentos.component';
import { VistoriasComponent } from './components/vistorias/vistorias.component';

export const RESERVAS_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'agendamentos',
    pathMatch: 'full'
  },
  {
    path: 'agendamentos',
    component: AgendamentosComponent
  },
  {
    path: 'vistorias',
    component: VistoriasComponent
  }
];
