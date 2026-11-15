import { Routes } from '@angular/router';
import { BlocoUnidadeListComponent } from './components/blocos-unidades/bloco-unidade-list.component';
import { VagaListComponent } from './components/vagas/vaga-list.component';
import { CondominioAdminComponent } from './components/branding/condominio-admin.component';
import { AreasComunsComponent } from './components/areas-comuns/areas-comuns.component';
import { UnitFormComponent } from './components/estrutura/unit-form.component';
import { BlockFormComponent } from './components/estrutura/block-form.component';
import { papelGuard } from '../../core/guards/papel.guard';

/** Estrutura patrimonial — só síndico/administrador (valores iguais ao JWT/seed). */
const PAPEIS_GESTAO_ESTRUTURA = [
  'SINDICO',
  'SUBSINDICO',
  'ADMIN',
  'ADMINISTRADOR',
  'ADMINISTRADORA',
  'SUPERADMIN',
];

export const CONDOMINIO_ROUTES: Routes = [
  {
    path: '',
    canActivate: [papelGuard],
    data: { papeis: PAPEIS_GESTAO_ESTRUTURA },
    children: [
      {
        path: '',
        component: BlocoUnidadeListComponent
      },
      {
        path: 'estrutura',
        component: BlocoUnidadeListComponent
      },
      {
        path: 'blocos-unidades',
        component: BlocoUnidadeListComponent
      },
      {
        path: 'vagas',
        component: VagaListComponent
      },
      {
        path: 'admin',
        component: CondominioAdminComponent
      },
      {
        path: 'branding',
        component: CondominioAdminComponent
      },
      {
        path: 'areas-comuns',
        component: AreasComunsComponent
      },
      {
        path: 'novo-bloco',
        component: BlockFormComponent
      },
      {
        path: 'nova-unidade',
        component: UnitFormComponent
      }
    ]
  }
];
