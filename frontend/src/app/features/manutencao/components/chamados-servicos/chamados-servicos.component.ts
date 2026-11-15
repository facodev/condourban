import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChamadoServico } from '../../services/manutencao.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-chamados-servicos',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './chamados-servicos.component.html',
  styleUrls: ['./chamados-servicos.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ChamadosServicosComponent {
  readonly chamados = signal<ChamadoServico[]>([
    {
      id: 1,
      titulo: 'Vazamento na torneira do jardim',
      descricao: 'Vazamento contínuo na torneira de irrigação próxima ao Bloco A.',
      local: 'Jardim Externo - Bloco A',
      prioridade: 'media',
      status: 'aberto',
      abertoPor: 'Zelador Marcos',
      abertoEm: '17/10/2026 09:15'
    }
  ]);
}
