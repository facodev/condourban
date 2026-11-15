import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VistoriaReserva } from '../../services/reservas.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-vistorias',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './vistorias.component.html',
  styleUrls: ['./vistorias.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class VistoriasComponent {
  readonly vistorias = signal<VistoriaReserva[]>([
    {
      id: 1,
      reservaId: 101,
      areaComumNome: 'Salão de Festas Principal',
      tipo: 'pos_uso',
      responsavelNome: 'Zelador Marcos',
      statusCaucao: 'devolvido',
      observacoes: 'Espaço entregue limpo, equipamentos e freezer em perfeito estado.',
      fotosUrls: [],
      realizadoEm: '17/10/2026 08:30'
    }
  ]);
}
