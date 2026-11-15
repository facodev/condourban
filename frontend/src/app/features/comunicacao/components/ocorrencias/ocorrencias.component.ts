import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Ocorrencia } from '../../services/comunicacao.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-ocorrencias',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './ocorrencias.component.html',
  styleUrls: ['./ocorrencias.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class OcorrenciasComponent {
  readonly ocorrencias = signal<Ocorrencia[]>([
    {
      id: 1,
      titulo: 'Ruído excessivo após as 22h',
      descricao: 'Música alta e barulho persistente no bloco vizinho durante a madrugada de sexta para sábado.',
      categoria: 'Barulho / Convivência',
      unidade: 'Apt 302',
      autorNome: 'Morador Carlos',
      status: 'em_analise',
      criadoEm: '17/10/2026 08:00'
    }
  ]);
}
