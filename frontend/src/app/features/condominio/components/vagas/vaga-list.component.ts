import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';
import { VagasService } from '../../services/vagas.service';
import { BlocoUnidadeService } from '../../services/bloco-unidade.service';
import { SessionService } from '../../../../core/services/session.service';
import { VagaGaragem, Unidade, Bloco } from '../../models/condominio.model';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-vaga-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, MatRippleModule, ButtonComponent, ConfirmDialogComponent, StatusBadgeComponent],
  templateUrl: './vaga-list.component.html',
  styleUrls: ['./vaga-list.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class VagaListComponent implements OnInit {
  private readonly service = inject(VagasService);
  private readonly blocoUnidadeService = inject(BlocoUnidadeService);
  readonly sessionService = inject(SessionService);

  vagas = signal<VagaGaragem[]>([]);
  unidades = signal<Unidade[]>([]);
  blocos = signal<Bloco[]>([]);
  isLoading = signal<boolean>(true);
  salvando = signal<boolean>(false);

  filtroTexto = signal<string>('');
  filtroTipo = signal<string>('TODOS');
  filtroCobertura = signal<string>('TODOS');

  // Paginação
  paginaAtual = signal<number>(1);
  itensPorPagina = signal<number>(10);

  mostrarFormNovaVaga = signal<boolean>(false);
  novaVagaForm: { identificacao: string; tipo: string; coberta: boolean; unidade_id: string | null } = {
    identificacao: '',
    tipo: 'CARRO',
    coberta: false,
    unidade_id: null
  };

  vagaEmEdicao = signal<VagaGaragem | null>(null);
  vagaEditForm: { identificacao: string; tipo: string; coberta: boolean; unidade_id: string | null } = {
    identificacao: '',
    tipo: 'CARRO',
    coberta: false,
    unidade_id: null
  };

  vagaParaExcluir = signal<VagaGaragem | null>(null);

  toastMensagem = signal<string>('');
  toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  totalCobertas = computed(() => this.vagas().filter(v => v.coberta).length);
  totalVinculadas = computed(() => this.vagas().filter(v => v.unidade_id || v.unidadeId).length);

  vagasFiltradas = computed(() => {
    const termo = this.filtroTexto().toLowerCase().trim();
    const tipo = this.filtroTipo();
    const cobertura = this.filtroCobertura();
    let lista = this.vagas();

    if (cobertura === 'COBERTAS') {
      lista = lista.filter(v => v.coberta);
    } else if (cobertura === 'DESCOBERTAS') {
      lista = lista.filter(v => !v.coberta);
    }

    if (tipo !== 'TODOS') {
      lista = lista.filter(v => (v.tipo || 'CARRO').toUpperCase() === tipo);
    }

    if (!termo) return lista;

    return lista.filter(v => {
      const identMatch = v.identificacao.toLowerCase().includes(termo);
      const unidadeBlocoDesc = this.getUnidadeBlocoDesc(v.unidade_id || v.unidadeId).toLowerCase();
      const unidadeMatch = unidadeBlocoDesc.includes(termo);
      return identMatch || unidadeMatch;
    });
  });

  totalPaginas = computed(() => {
    const total = this.vagasFiltradas().length;
    return Math.max(1, Math.ceil(total / this.itensPorPagina()));
  });

  paginasVisiveis = computed(() => {
    const total = this.totalPaginas();
    const atual = Math.min(this.paginaAtual(), total);
    const paginas: number[] = [];
    const inicio = Math.max(1, atual - 2);
    const fim = Math.min(total, inicio + 4);
    for (let i = Math.max(1, fim - 4); i <= fim; i++) {
      paginas.push(i);
    }
    return paginas;
  });

  vagasPaginadas = computed(() => {
    const lista = this.vagasFiltradas();
    const total = Math.max(1, Math.ceil(lista.length / this.itensPorPagina()));
    const pag = Math.min(this.paginaAtual(), total);
    const start = (pag - 1) * this.itensPorPagina();
    return lista.slice(start, start + this.itensPorPagina());
  });

  rangeInicio = computed(() => {
    const total = this.vagasFiltradas().length;
    if (total === 0) return 0;
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    return (pag - 1) * this.itensPorPagina() + 1;
  });

  rangeFim = computed(() => {
    const total = this.vagasFiltradas().length;
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    return Math.min(pag * this.itensPorPagina(), total);
  });

  ngOnInit(): void {
    this.carregarDados();
  }

  irParaPagina(p: number): void {
    if (p >= 1 && p <= this.totalPaginas()) {
      this.paginaAtual.set(p);
    }
  }

  alterarItensPorPagina(size: number): void {
    this.itensPorPagina.set(Number(size));
    this.paginaAtual.set(1);
  }

  limparFiltros(): void {
    this.filtroTexto.set('');
    this.filtroTipo.set('TODOS');
    this.filtroCobertura.set('TODOS');
    this.paginaAtual.set(1);
  }

  carregarDados(): void {
    this.isLoading.set(true);
    const cid = this.sessionService.condominioAtivoId() || undefined;

    this.blocoUnidadeService.getBlocos(cid).subscribe({
      next: (b) => this.blocos.set(b),
      error: (e) => console.warn('Erro ao carregar blocos em vagas:', e)
    });

    this.service.getVagas(undefined, cid).subscribe({
      next: (v) => {
        this.vagas.set(v);
        this.blocoUnidadeService.getUnidades(undefined, cid).subscribe({
          next: (u) => {
            this.unidades.set(u);
            this.isLoading.set(false);
          },
          error: () => this.isLoading.set(false)
        });
      },
      error: (err) => {
        this.isLoading.set(false);
        this.mostrarToast('Erro ao carregar vagas: ' + (err?.error?.detail || err.message), 'erro');
      }
    });
  }

  getUnidade(unidadeId?: string): Unidade | null {
    if (!unidadeId) return null;
    return this.unidades().find(item => item.id === unidadeId) || null;
  }

  getBlocoNome(blocoId?: string | null): string {
    if (!blocoId) return '';
    const b = this.blocos().find(item => item.id === blocoId);
    return b ? (b.nome || b.name || '') : '';
  }

  getUnidadeNome(unidadeId?: string): string {
    const u = this.getUnidade(unidadeId);
    return u ? (u.identificacao || (u as any).number) : '';
  }

  getUnidadeBlocoDesc(unidadeId?: string): string {
    const u = this.getUnidade(unidadeId);
    if (!u) return '';
    const ident = u.identificacao || (u as any).number || '';
    const bloco = this.getBlocoNome(u.bloco_id || (u as any).blocoId);
    return bloco ? `${ident} / ${bloco}` : ident;
  }

  salvarNovaVaga(): void {
    if (!this.novaVagaForm.identificacao.trim()) return;

    this.salvando.set(true);
    this.service.createVaga({
      identificacao: this.novaVagaForm.identificacao.trim(),
      tipo: this.novaVagaForm.tipo,
      coberta: this.novaVagaForm.coberta,
      unidade_id: this.novaVagaForm.unidade_id || undefined,
      condominio_id: this.sessionService.condominioAtivoId() || undefined
    }).subscribe({
      next: (criada) => {
        this.salvando.set(false);
        this.mostrarFormNovaVaga.set(false);
        this.novaVagaForm = { identificacao: '', tipo: 'CARRO', coberta: false, unidade_id: null };
        this.mostrarToast(`Vaga ${criada.identificacao} cadastrada com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao cadastrar vaga.', 'erro');
      }
    });
  }

  abrirEdicao(vaga: VagaGaragem): void {
    this.vagaEmEdicao.set(vaga);
    this.vagaEditForm = {
      identificacao: vaga.identificacao || '',
      tipo: vaga.tipo || 'CARRO',
      coberta: vaga.coberta,
      unidade_id: vaga.unidade_id || vaga.unidadeId || null
    };
  }

  salvarEdicao(): void {
    const vaga = this.vagaEmEdicao();
    if (!vaga) return;
    if (!this.vagaEditForm.identificacao.trim()) {
      this.mostrarToast('A identificação da vaga é obrigatória.', 'erro');
      return;
    }

    this.salvando.set(true);
    this.service.updateVaga(vaga.id, {
      identificacao: this.vagaEditForm.identificacao.trim(),
      tipo: this.vagaEditForm.tipo,
      coberta: this.vagaEditForm.coberta,
      unidade_id: this.vagaEditForm.unidade_id
    }).subscribe({
      next: (atualizada) => {
        this.salvando.set(false);
        this.vagaEmEdicao.set(null);
        this.mostrarToast(`Vaga ${atualizada.identificacao} atualizada com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao atualizar vaga.', 'erro');
      }
    });
  }

  confirmarExclusao(vaga: VagaGaragem): void {
    this.vagaParaExcluir.set(vaga);
  }

  executarExclusao(): void {
    const vaga = this.vagaParaExcluir();
    if (!vaga) return;

    this.salvando.set(true);
    this.service.deleteVaga(vaga.id).subscribe({
      next: () => {
        this.salvando.set(false);
        this.vagaParaExcluir.set(null);
        this.mostrarToast(`Vaga ${vaga.identificacao} excluída com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao excluir vaga.', 'erro');
      }
    });
  }

  mostrarToast(msg: string, tipo: 'sucesso' | 'erro' = 'sucesso'): void {
    this.toastMensagem.set(msg);
    this.toastTipo.set(tipo);
    setTimeout(() => {
      if (this.toastMensagem() === msg) {
        this.toastMensagem.set('');
      }
    }, 5000);
  }
}
