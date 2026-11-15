import { Routes } from '@angular/router';
import { ChamadosServicosComponent } from './components/chamados-servicos/chamados-servicos.component';
import { PlanoInventarioComponent } from './components/plano-inventario/plano-inventario.component';

export const MANUTENCAO_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'chamados-servicos',
    pathMatch: 'full'
  },
  {
    path: 'chamados-servicos',
    component: ChamadosServicosComponent
  },
  {
    path: 'plano-inventario',
    component: PlanoInventarioComponent
  }
];
