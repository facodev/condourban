import { Routes } from '@angular/router';
import { AssembleiasComponent } from './components/assembleias/assembleias.component';
import { SegurancaAuditoriaComponent } from './components/seguranca-auditoria/seguranca-auditoria.component';

export const GOVERNANCA_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'assembleias',
    pathMatch: 'full'
  },
  {
    path: 'assembleias',
    component: AssembleiasComponent
  },
  {
    path: 'seguranca-auditoria',
    component: SegurancaAuditoriaComponent
  }
];
