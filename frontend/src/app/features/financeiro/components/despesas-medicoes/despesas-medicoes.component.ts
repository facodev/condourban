import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MedicaoConsumo } from '../../services/financeiro.service';

@Component({
  selector: 'app-despesas-medicoes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './despesas-medicoes.component.html',
  styleUrls: ['./despesas-medicoes.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class DespesasMedicoesComponent {
  readonly medicoes = signal<MedicaoConsumo[]>([
    {
      id: 1,
      unidade: 'Apt 101',
      tipo: 'agua',
      leituraAnterior: 142.5,
      leituraAtual: 153.2,
      consumo: 10.7,
      mesReferencia: 'Outubro/2026'
    },
    {
      id: 2,
      unidade: 'Apt 101',
      tipo: 'gas',
      leituraAnterior: 88.0,
      leituraAtual: 93.4,
      consumo: 5.4,
      mesReferencia: 'Outubro/2026'
    }
  ]);
}
