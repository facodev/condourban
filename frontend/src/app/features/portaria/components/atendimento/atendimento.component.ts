import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AtendimentoPortaria } from '../../services/portaria.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-atendimento',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './atendimento.component.html',
  styleUrls: ['./atendimento.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class AtendimentoComponent {
  readonly atendimentos = signal<AtendimentoPortaria[]>([
    {
      id: '1',
      visitanteNome: 'Marcos Vinicius (Técnico Internet)',
      documento: 'RG 45.123.890-X',
      tipo: 'prestador',
      unidadeDestino: 'Bloco A - Apt 101',
      status: 'aguardando'
    },
    {
      id: '2',
      visitanteNome: 'Ana Paula Rocha',
      documento: 'CPF 333.444.555-66',
      tipo: 'visitante',
      unidadeDestino: 'Bloco B - Apt 304',
      status: 'entrou',
      entradaEm: '17/10/2026 15:40'
    }
  ]);

  autorizar(id: string): void {
    this.atendimentos.update(list =>
      list.map(a => (a.id === id ? { ...a, status: 'autorizado' } : a))
    );
  }

  registrarEntrada(id: string): void {
    this.atendimentos.update(list =>
      list.map(a => (a.id === id ? { ...a, status: 'entrou', entradaEm: 'Agora' } : a))
    );
  }

  registrarSaida(id: string): void {
    this.atendimentos.update(list =>
      list.map(a => (a.id === id ? { ...a, status: 'saiu', saidaEm: 'Agora' } : a))
    );
  }
}
