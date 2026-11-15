import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EventoAcesso } from '../../services/controle-acesso.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-eventos',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './eventos.component.html',
  styleUrls: ['./eventos.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class EventosComponent {
  readonly eventos = signal<EventoAcesso[]>([
    {
      id: '1',
      dispositivoNome: 'Facial Portaria Social',
      pessoaNome: 'Carlos Eduardo Silva',
      sentido: 'entrada',
      autorizado: true,
      timestamp: '17/10/2026 16:42:10'
    },
    {
      id: '2',
      dispositivoNome: 'Cancela Veicular Entrada',
      pessoaNome: 'Veículo Placa ABC1D23',
      sentido: 'entrada',
      autorizado: true,
      timestamp: '17/10/2026 16:38:05'
    },
    {
      id: '3',
      dispositivoNome: 'Facial Portaria Social',
      pessoaNome: 'Desconhecido',
      sentido: 'entrada',
      autorizado: false,
      motivo: 'Rosto não cadastrado na base',
      timestamp: '17/10/2026 16:30:12'
    }
  ]);
}
