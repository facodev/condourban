import { Routes } from '@angular/router';
import { PessoasComponent } from './components/pessoas/pessoas.component';
import { OcupacoesComponent } from './components/ocupacoes/ocupacoes.component';
import { UsuariosComponent } from './components/usuarios/usuarios.component';
import { OnboardingComponent } from './components/onboarding/onboarding.component';
import { VeiculosPetsComponent } from './components/veiculos-pets/veiculos-pets.component';
import { papelGuard } from '../../core/guards/papel.guard';

export const IDENTIDADE_CADASTRO_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'pessoas',
    pathMatch: 'full'
  },
  {
    path: 'pessoas',
    component: PessoasComponent
  },
  {
    path: 'ocupacoes',
    component: OcupacoesComponent
  },
  {
    path: 'usuarios',
    component: UsuariosComponent,
    canActivate: [papelGuard],
    data: {
      papeis: [
        'SINDICO',
        'SUBSINDICO',
        'ADMIN',
        'ADMINISTRADOR',
        'ADMINISTRADORA',
        'SUPERADMIN',
      ],
    },
  },
  {
    path: 'onboarding',
    component: OnboardingComponent,
    canActivate: [papelGuard],
    data: {
      papeis: [
        'SINDICO',
        'SUBSINDICO',
        'ADMIN',
        'ADMINISTRADOR',
        'ADMINISTRADORA',
        'SUPERADMIN',
      ],
    },
  },
  {
    path: 'veiculos-pets',
    component: VeiculosPetsComponent
  }
];
