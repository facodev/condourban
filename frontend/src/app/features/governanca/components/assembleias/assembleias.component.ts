import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Assembleia } from '../../services/governanca.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-assembleias',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './assembleias.component.html',
  styleUrls: ['./assembleias.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class AssembleiasComponent {
  readonly assembleias = signal<Assembleia[]>([
    {
      id: 1,
      titulo: 'Assembleia Geral Ordinária 2026',
      tipo: 'ordinaria',
      dataInicio: '28/10/2026 às 19:30',
      status: 'convocada',
      pautas: [
        { id: 1, titulo: 'Aprovação das contas do exercício anterior', votosFavoraveis: 18, votosContrarios: 2 },
        { id: 2, titulo: 'Previsão orçamentária e taxa condominial', votosFavoraveis: 14, votosContrarios: 6 }
      ]
    }
  ]);
}
