import { Component, ViewEncapsulation, input, computed } from '@angular/core';

export type StatusVariant =
  | 'pendente'
  | 'em_analise'
  | 'enviada'
  | 'aprovado'
  | 'rejeitado'
  | 'ativo'
  | 'inativo'
  | 'concluido'
  | 'cancelado'
  | 'alerta'
  | 'info'
  | 'interditado'
  | 'disponivel';

@Component({
  selector: 'app-status-badge',
  standalone: true,
  templateUrl: './status-badge.component.html',
  styleUrls: ['./status-badge.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class StatusBadgeComponent {
  readonly status = input<string>('pendente');
  readonly label = input<string>('');

  readonly normalizedStatus = computed(() => {
    const s = (this.status() || 'pendente').toLowerCase().replace('-', '_');
    return s;
  });

  readonly variantClass = computed(() => {
    return `badge-${this.normalizedStatus()}`;
  });

  readonly displayLabel = computed(() => {
    if (this.label()) return this.label();
    const s = this.normalizedStatus();
    switch (s) {
      case 'em_analise': return 'Em Análise';
      case 'ativo': return 'Ativo';
      case 'inativo': return 'Inativo';
      case 'aprovado': return 'Aprovado';
      case 'rejeitado': return 'Rejeitado';
      case 'pendente': return 'Pendente';
      case 'disponivel': return 'Disponível';
      case 'interditado': return 'Interditado';
      default: return this.status();
    }
  });
}
