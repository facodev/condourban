import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgendamentoReserva } from '../../services/reservas.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-agendamentos',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './agendamentos.component.html',
  styleUrls: ['./agendamentos.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class AgendamentosComponent {
  readonly agendamentos = signal<AgendamentoReserva[]>([
    {
      id: '1',
      areaComumNome: 'Salão de Festas Principal',
      moradorNome: 'Carlos Eduardo Silva',
      unidade: 'Apt 101',
      data: '24/10/2026',
      horarioInicio: '18:00',
      horarioFim: '23:00',
      status: 'aprovado',
      listaConvidados: ['Lucas Santos', 'Fernanda Lima', 'Rodrigo Souza']
    },
    {
      id: '2',
      areaComumNome: 'Churrasqueira 1',
      moradorNome: 'Mariana Costa Ferreira',
      unidade: 'Apt 205',
      data: '25/10/2026',
      horarioInicio: '12:00',
      horarioFim: '16:00',
      status: 'pendente'
    }
  ]);
}
