import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MatRipple } from '@angular/material/core';
import { BlocoUnidadeService } from '../../services/bloco-unidade.service';
import { SessionService } from '../../../../core/services/session.service';
import { Bloco, Unidade } from '../../models/condominio.model';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';
import { IdentidadeCadastroService, Pessoa, OcupacaoUnidade } from '../../../identidade_cadastro/services/identidade-cadastro.service';
import { CpfPipe } from '../../../../shared/pipes/cpf.pipe';

const BLOCO_COLOR_THEMES = [
  'bloco-theme-blue',
  'bloco-theme-emerald',
  'bloco-theme-violet',
  'bloco-theme-amber',
  'bloco-theme-cyan',
  'bloco-theme-rose',
  'bloco-theme-indigo',
  'bloco-theme-teal'
] as const;

export interface PessoaVinculadaView {
  ocupacaoId: string;
  pessoaId: string;
  nome: string;
  cpf?: string;
  tipoVinculo: string;
  moraNoLocal: boolean;
  principal: boolean;
  status: string;
}

@Component({
  selector: 'app-bloco-unidade-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    MatRipple,
    ButtonComponent,
    ConfirmDialogComponent,
    StatusBadgeComponent,
    CpfPipe
  ],
  templateUrl: './bloco-unidade-list.component.html',
  styleUrls: ['./bloco-unidade-list.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class BlocoUnidadeListComponent implements OnInit {
  private readonly service = inject(BlocoUnidadeService);
  private readonly sessionService = inject(SessionService);
  private readonly idService = inject(IdentidadeCadastroService);

  readonly blocos = signal<Bloco[]>([]);
  readonly unidades = signal<Unidade[]>([]);
  readonly ocupacoes = signal<OcupacaoUnidade[]>([]);
  readonly pessoas = signal<Pessoa[]>([]);
  readonly isLoading = signal<boolean>(true);
  readonly salvando = signal<boolean>(false);

  // Filtros padronizados
  readonly filtroTexto = signal<string>('');
  readonly filtroBloco = signal<string>('TODOS');
  readonly filtroTipo = signal<string>('TODOS');
  readonly filtroStatus = signal<string>('TODOS');

  // Paginação da tabela
  readonly paginaAtual = signal<number>(1);
  readonly itensPorPagina = signal<number>(10);

  readonly toastMensagem = signal<string>('');
  readonly toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  // Modal de pessoas vinculadas à unidade
  readonly unidadePessoasModal = signal<Unidade | null>(null);

  // Modais de edição
  readonly blocoEmEdicao = signal<Bloco | null>(null);
  blocoEditForm = { nome: '', descricao: '' };

  readonly unidadeEmEdicao = signal<Unidade | null>(null);
  unidadeEditForm: {
    identificacao: string;
    bloco_id: string | null;
    andar: string | number;
    tipo: string;
    area_privativa?: number | null;
  } = {
    identificacao: '',
    bloco_id: null,
    andar: '',
    tipo: 'APARTAMENTO',
    area_privativa: null
  };

  readonly itemParaExcluir = signal<{ tipo: 'bloco' | 'unidade'; id: string; nome: string } | null>(null);

  readonly totalMetragem = computed(() => {
    const total = this.unidades().reduce((acc, u) => acc + Number(u.area_privativa || 0), 0);
    return total.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 2 });
  });

  readonly blocoSelecionadoFiltro = computed<Bloco | null>(() => {
    const id = this.filtroBloco();
    if (!id || id === 'TODOS') return null;
    return this.blocos().find(b => b.id === id) || null;
  });

  // Pessoas vinculadas à unidade em visualização modal
  readonly pessoasDaUnidadeModal = computed<PessoaVinculadaView[]>(() => {
    const u = this.unidadePessoasModal();
    if (!u) return [];

    const ocs = this.ocupacoes().filter(oc => oc.unidade_id === u.id);
    const pessoasList = this.pessoas();

    return ocs.map(oc => {
      const p = pessoasList.find(item => item.id === oc.pessoa_id);
      return {
        ocupacaoId: oc.id,
        pessoaId: oc.pessoa_id,
        nome: p ? (p.nome_completo || p.nomeCompleto || p.nome || 'Pessoa Física') : 'Pessoa Física',
        cpf: p?.cpf,
        tipoVinculo: oc.tipo_vinculo,
        moraNoLocal: Boolean(oc.mora_no_local),
        principal: Boolean(oc.principal),
        status: oc.status
      };
    });
  });

  // Unidades filtradas e ordenadas por Bloco -> Identificação
  readonly unidadesFiltradas = computed(() => {
    const termo = this.filtroTexto().toLowerCase().trim();
    const blocoId = this.filtroBloco();
    const tipo = this.filtroTipo();
    const status = this.filtroStatus();

    const filtradas = this.unidades().filter(u => {
      const uBlocoId = u.bloco_id || (u as any).blocoId || 'SEM_BLOCO';

      if (blocoId !== 'TODOS' && uBlocoId !== blocoId) {
        return false;
      }

      if (tipo !== 'TODOS' && (u.tipo || 'APARTAMENTO').toUpperCase() !== tipo) {
        return false;
      }

      const uStatus = (u.status || 'ATIVO').toUpperCase();
      if (status !== 'TODOS' && uStatus !== status) {
        return false;
      }

      if (!termo) return true;

      const ident = (u.identificacao || (u as any).number || '').toLowerCase();
      const andar = String(u.andar || (u as any).floor || '').toLowerCase();
      const tipoStr = (u.tipo || 'APARTAMENTO').toLowerCase();
      const blocoNome = this.getBlocoNome(u.bloco_id || (u as any).blocoId).toLowerCase();

      return (
        ident.includes(termo) ||
        andar.includes(termo) ||
        tipoStr.includes(termo) ||
        blocoNome.includes(termo)
      );
    });

    return filtradas.sort((a, b) => {
      const bNomeA = this.getBlocoNome(a.bloco_id || (a as any).blocoId);
      const bNomeB = this.getBlocoNome(b.bloco_id || (b as any).blocoId);
      if (bNomeA !== bNomeB) return bNomeA.localeCompare(bNomeB, 'pt-BR');

      const identA = String(a.identificacao || (a as any).number || '');
      const identB = String(b.identificacao || (b as any).number || '');
      return identA.localeCompare(identB, 'pt-BR', { numeric: true });
    });
  });

  readonly totalPaginas = computed(() => {
    return Math.max(1, Math.ceil(this.unidadesFiltradas().length / this.itensPorPagina()));
  });

  readonly unidadesPaginadas = computed(() => {
    const tam = this.itensPorPagina();
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    const inicio = (pag - 1) * tam;
    return this.unidadesFiltradas().slice(inicio, inicio + tam);
  });

  readonly indiceInicial = computed(() => {
    if (this.unidadesFiltradas().length === 0) return 0;
    return (Math.min(this.paginaAtual(), this.totalPaginas()) - 1) * this.itensPorPagina() + 1;
  });

  readonly indiceFinal = computed(() => {
    return Math.min(this.unidadesFiltradas().length, this.indiceInicial() + this.unidadesPaginadas().length - 1);
  });

  readonly paginasArray = computed(() => {
    return Array.from({ length: this.totalPaginas() }, (_, i) => i + 1);
  });

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    this.isLoading.set(true);
    const condoId = this.sessionService.condominioAtivoId() || undefined;

    this.service.getBlocos(condoId).subscribe({
      next: (b) => {
        this.blocos.set(b);
        this.service.getUnidades(undefined, condoId).subscribe({
          next: (u) => {
            this.unidades.set(u);
            this.isLoading.set(false);
          },
          error: (err) => {
            this.isLoading.set(false);
            this.mostrarToast('Erro ao carregar unidades: ' + (err?.error?.detail || err.message), 'erro');
          }
        });
      },
      error: (err) => {
        this.isLoading.set(false);
        this.mostrarToast('Erro ao carregar blocos: ' + (err?.error?.detail || err.message), 'erro');
      }
    });

    // Carregar vínculos e pessoas físicas para contadores e listagem da unidade
    this.idService.getOcupacoes(undefined, false, condoId).subscribe({
      next: (dados) => this.ocupacoes.set(dados),
      error: (e) => console.warn('Não foi possível carregar ocupações:', e)
    });

    this.idService.getPessoas(condoId).subscribe({
      next: (dados) => this.pessoas.set(dados),
      error: (e) => console.warn('Não foi possível carregar pessoas:', e)
    });
  }

  getTotalPessoasVinculadas(unidadeId: string): number {
    return this.ocupacoes().filter(oc => oc.unidade_id === unidadeId && oc.status === 'ATIVA').length;
  }

  abrirPessoasUnidade(unidade: Unidade): void {
    this.unidadePessoasModal.set(unidade);
  }

  fecharPessoasUnidade(): void {
    this.unidadePessoasModal.set(null);
  }

  getBlocoById(blocoId?: string | null): Bloco | null {
    if (!blocoId) return null;
    return this.blocos().find(item => item.id === blocoId) || null;
  }

  getBlocoNome(blocoId?: string | null): string {
    if (!blocoId) return 'Sem Bloco';
    const b = this.blocos().find(item => item.id === blocoId);
    return b ? (b.nome || b.name || 'Bloco') : 'Sem Bloco';
  }

  /**
   * Retorna uma classe de cor distinta por bloco no estilo de badge de tipologia.
   */
  getBlocoBadgeClass(blocoId?: string | null): string {
    if (!blocoId) return 'bloco-theme-neutral';
    const lista = this.blocos();
    const idx = lista.findIndex(item => item.id === blocoId);
    if (idx >= 0) {
      return BLOCO_COLOR_THEMES[idx % BLOCO_COLOR_THEMES.length];
    }
    // Fallback determinístico por hash do ID
    let hash = 0;
    for (let i = 0; i < blocoId.length; i++) {
      hash = (hash * 31 + blocoId.charCodeAt(i)) >>> 0;
    }
    return BLOCO_COLOR_THEMES[hash % BLOCO_COLOR_THEMES.length];
  }

  getTipoBadgeClass(tipo: string): string {
    switch (tipo) {
      case 'PROPRIETARIO': return 'badge-proprietario';
      case 'INQUILINO': return 'badge-inquilino';
      case 'DEPENDENTE': return 'badge-dependente';
      case 'TEMPORARIO': return 'badge-temporario';
      case 'HOSPEDE': return 'badge-hospede';
      default: return 'badge-proprietario';
    }
  }

  aoMudarBusca(valor: string): void {
    this.filtroTexto.set(valor);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroBloco(valor: string): void {
    this.filtroBloco.set(valor);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroTipo(valor: string): void {
    this.filtroTipo.set(valor);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroStatus(valor: string): void {
    this.filtroStatus.set(valor);
    this.paginaAtual.set(1);
  }

  limparFiltros(): void {
    this.filtroTexto.set('');
    this.filtroBloco.set('TODOS');
    this.filtroTipo.set('TODOS');
    this.filtroStatus.set('TODOS');
    this.paginaAtual.set(1);
  }

  mudarPagina(pagina: number): void {
    if (pagina >= 1 && pagina <= this.totalPaginas()) {
      this.paginaAtual.set(pagina);
    }
  }

  aoMudarItensPorPagina(novoTamanho: number): void {
    this.itensPorPagina.set(Number(novoTamanho));
    this.paginaAtual.set(1);
  }

  abrirEdicaoBloco(bloco: Bloco): void {
    this.blocoEmEdicao.set(bloco);
    this.blocoEditForm = {
      nome: bloco.nome || bloco.name || '',
      descricao: bloco.descricao || bloco.description || ''
    };
  }

  salvarEdicaoBloco(): void {
    const bloco = this.blocoEmEdicao();
    if (!bloco) return;

    this.salvando.set(true);
    this.service.updateBloco(bloco.id, {
      nome: this.blocoEditForm.nome.trim(),
      descricao: this.blocoEditForm.descricao.trim() || undefined
    }).subscribe({
      next: (atualizado) => {
        this.salvando.set(false);
        this.blocoEmEdicao.set(null);
        this.mostrarToast(`Bloco ${atualizado.nome} atualizado com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast('Erro ao atualizar bloco: ' + (err?.error?.detail || err.message), 'erro');
      }
    });
  }

  abrirEdicaoUnidade(unidade: Unidade): void {
    this.unidadeEmEdicao.set(unidade);
    this.unidadeEditForm = {
      identificacao: unidade.identificacao || (unidade as any).number || '',
      bloco_id: unidade.bloco_id || (unidade as any).blocoId || null,
      andar: unidade.andar || (unidade as any).floor || '',
      tipo: unidade.tipo || 'APARTAMENTO',
      area_privativa: unidade.area_privativa ?? null
    };
  }

  salvarEdicaoUnidade(): void {
    const unidade = this.unidadeEmEdicao();
    if (!unidade) return;

    this.salvando.set(true);
    this.service.updateUnidade(unidade.id, {
      identificacao: this.unidadeEditForm.identificacao.trim(),
      bloco_id: this.unidadeEditForm.bloco_id || undefined,
      andar: this.unidadeEditForm.andar,
      tipo: this.unidadeEditForm.tipo
    }).subscribe({
      next: (atualizada) => {
        this.salvando.set(false);
        this.unidadeEmEdicao.set(null);
        this.mostrarToast(`Unidade ${atualizada.identificacao} atualizada com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast('Erro ao atualizar unidade: ' + (err?.error?.detail || err.message), 'erro');
      }
    });
  }

  confirmarExclusaoBloco(bloco: Bloco): void {
    this.itemParaExcluir.set({
      tipo: 'bloco',
      id: bloco.id,
      nome: `Bloco ${bloco.nome || bloco.name}`
    });
  }

  confirmarExclusaoUnidade(unidade: Unidade): void {
    this.itemParaExcluir.set({
      tipo: 'unidade',
      id: unidade.id,
      nome: `Unidade ${unidade.identificacao || (unidade as any).number}`
    });
  }

  executarExclusao(): void {
    const item = this.itemParaExcluir();
    if (!item) return;

    this.salvando.set(true);
    if (item.tipo === 'bloco') {
      this.service.deleteBloco(item.id).subscribe({
        next: () => {
          this.salvando.set(false);
          this.itemParaExcluir.set(null);
          if (this.filtroBloco() === item.id) {
            this.filtroBloco.set('TODOS');
          }
          this.mostrarToast(`${item.nome} excluído com sucesso!`);
          this.carregarDados();
        },
        error: (err) => {
          this.salvando.set(false);
          this.itemParaExcluir.set(null);
          this.mostrarToast(err?.error?.detail || 'Erro ao excluir bloco.', 'erro');
        }
      });
    } else {
      this.service.deleteUnidade(item.id).subscribe({
        next: () => {
          this.salvando.set(false);
          this.itemParaExcluir.set(null);
          this.mostrarToast(`${item.nome} excluída com sucesso!`);
          this.carregarDados();
        },
        error: (err) => {
          this.salvando.set(false);
          this.itemParaExcluir.set(null);
          this.mostrarToast(err?.error?.detail || 'Erro ao excluir unidade.', 'erro');
        }
      });
    }
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
