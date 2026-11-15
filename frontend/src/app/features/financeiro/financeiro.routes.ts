import { Routes } from '@angular/router';
import { CobrancasAcordosComponent } from './components/cobrancas-acordos/cobrancas-acordos.component';
import { DespesasMedicoesComponent } from './components/despesas-medicoes/despesas-medicoes.component';

export const FINANCEIRO_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'cobrancas-acordos',
    pathMatch: 'full'
  },
  {
    path: 'cobrancas-acordos',
    component: CobrancasAcordosComponent
  },
  {
    path: 'despesas-medicoes',
    component: DespesasMedicoesComponent
  }
];
