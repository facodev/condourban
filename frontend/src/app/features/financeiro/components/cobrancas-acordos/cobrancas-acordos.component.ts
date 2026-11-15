import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CobrancaBoleto } from '../../services/financeiro.service';
import { MoedaPipe } from '../../../../shared/pipes/moeda.pipe';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-cobrancas-acordos',
  standalone: true,
  imports: [CommonModule, MoedaPipe, StatusBadgeComponent],
  templateUrl: './cobrancas-acordos.component.html',
  styleUrls: ['./cobrancas-acordos.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class CobrancasAcordosComponent {
  readonly cobrancas = signal<CobrancaBoleto[]>([
    {
      id: 1,
      unidade: 'Apt 101',
      mesReferencia: 'Outubro/2026',
      vencimento: '10/11/2026',
      valor: 485.50,
      status: 'pendente'
    },
    {
      id: 2,
      unidade: 'Apt 101',
      mesReferencia: 'Setembro/2026',
      vencimento: '10/10/2026',
      valor: 472.00,
      status: 'pago'
    }
  ]);
}
