import { Component, OnInit, ViewEncapsulation, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PacoteEncomenda, PortariaService } from '../../services/portaria.service';
import { SessionService } from '../../../../core/services/session.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-encomendas',
  standalone: true,
  imports: [CommonModule, FormsModule, StatusBadgeComponent],
  templateUrl: './encomendas.component.html',
  styleUrls: ['./encomendas.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class EncomendasComponent implements OnInit {
  private readonly portariaService = inject(PortariaService);
  readonly sessionService = inject(SessionService);

  readonly pacotes = signal<PacoteEncomenda[]>([]);
  readonly loading = signal(true);
  readonly erro = signal('');
  readonly baixaEmAndamento = signal<string | null>(null);
  readonly encomendaBaixaId = signal<string | null>(null);
  pinDigitado = '';

  readonly podeBaixar = computed(() => this.sessionService.podeOperarEncomendas());
  readonly podeRegistrar = computed(() => this.sessionService.podeOperarEncomendas());

  ngOnInit(): void {
    this.carregar();
  }

  carregar(): void {
    this.loading.set(true);
    this.erro.set('');
    const condoId = this.sessionService.condominioAtivoId();
    this.portariaService.getEncomendas(condoId).subscribe({
      next: (lista) => {
        this.pacotes.set(lista);
        this.loading.set(false);
      },
      error: () => {
        this.pacotes.set([]);
        this.loading.set(false);
        this.erro.set('Não foi possível carregar as encomendas. Tente novamente.');
      }
    });
  }

  abrirBaixa(id: string): void {
    this.encomendaBaixaId.set(id);
    this.pinDigitado = '';
  }

  cancelarBaixa(): void {
    this.encomendaBaixaId.set(null);
    this.pinDigitado = '';
  }

  confirmarBaixa(): void {
    const id = this.encomendaBaixaId();
    const pin = this.pinDigitado.trim();
    if (!id || !pin) return;

    this.baixaEmAndamento.set(id);
    this.portariaService.darBaixaEncomenda(id, pin).subscribe({
      next: (atualizada) => {
        this.pacotes.update((lista) =>
          lista.map((p) => (p.id === id ? { ...p, ...atualizada } : p))
        );
        this.baixaEmAndamento.set(null);
        this.cancelarBaixa();
      },
      error: (err) => {
        this.baixaEmAndamento.set(null);
        const detail = err?.error?.detail;
        this.erro.set(
          detail === 'PIN_INVALIDO'
            ? 'PIN inválido. Confira o código com o morador.'
            : 'Falha ao registrar a retirada.'
        );
      }
    });
  }

  statusRecebida(status: string): boolean {
    const s = String(status || '').toUpperCase();
    return s === 'RECEBIDA' || s === 'PENDENTE';
  }
}
