import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ComunicadoOficial } from '../../services/comunicacao.service';

@Component({
  selector: 'app-mensageria',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mensageria.component.html',
  styleUrls: ['./mensageria.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class MensageriaComponent {
  readonly comunicados = signal<ComunicadoOficial[]>([
    {
      id: 1,
      titulo: 'Manutenção Preventiva dos Elevadores',
      conteudo: 'Informamos que na próxima terça-feira (20/10) os elevadores do Bloco A passarão por manutenção entre 09:00 e 12:00.',
      autorNome: 'Administração Predial',
      urgente: true,
      publicadoEm: '16/10/2026'
    },
    {
      id: 2,
      titulo: 'Assembleia Geral Ordinária Convocada',
      conteudo: 'Acesse o módulo de governança para visualizar o edital e a pauta da próxima reunião virtual.',
      autorNome: 'Síndico Geral',
      urgente: false,
      publicadoEm: '15/10/2026'
    }
  ]);
}
