import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LogAuditoria } from '../../services/governanca.service';

@Component({
  selector: 'app-seguranca-auditoria',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './seguranca-auditoria.component.html',
  styleUrls: ['./seguranca-auditoria.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class SegurancaAuditoriaComponent {
  readonly logs = signal<LogAuditoria[]>([
    {
      id: 1,
      usuarioNome: 'Síndico Geral',
      acao: 'APROVACAO_ONBOARDING',
      entidade: 'Unidade 402 - Juliana Paes',
      ipOrigem: '189.120.45.12',
      timestamp: '17/10/2026 14:35:10'
    },
    {
      id: 2,
      usuarioNome: 'Porteiro Principal',
      acao: 'ENTREGA_ENCOMENDA',
      entidade: 'Pacote ML-9921',
      ipOrigem: '192.168.1.50',
      timestamp: '17/10/2026 13:20:00'
    }
  ]);
}
