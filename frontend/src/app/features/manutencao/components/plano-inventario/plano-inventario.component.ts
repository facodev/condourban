import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ItemInventarioPMO } from '../../services/manutencao.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-plano-inventario',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './plano-inventario.component.html',
  styleUrls: ['./plano-inventario.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class PlanoInventarioComponent {
  readonly itens = signal<ItemInventarioPMO[]>([
    {
      id: 1,
      equipamento: 'Elevador Social - Bloco A',
      localizacao: 'Torre A',
      periodicidade: 'Mensal',
      proximaManutencao: '20/10/2026',
      responsavelTecnico: 'Atlas Schindler',
      status: 'em_dia'
    },
    {
      id: 2,
      equipamento: 'Bomba de Recalque 01',
      localizacao: 'Casa de Máquinas',
      periodicidade: 'Trimestral',
      proximaManutencao: '15/11/2026',
      responsavelTecnico: 'HidroBombas SP',
      status: 'em_dia'
    }
  ]);
}
