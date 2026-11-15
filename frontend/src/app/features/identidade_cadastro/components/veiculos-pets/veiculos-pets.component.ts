import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { IdentidadeCadastroService, Veiculo, Pet } from '../../services/identidade-cadastro.service';
import { CondominioService, Unidade, Bloco } from '../../../condominio/services/condominio.service';
import { SessionService } from '../../../../core/services/session.service';
import { PlacaPipe } from '../../../../shared/pipes/placa.pipe';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-veiculos-pets',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RouterLinkActive, PlacaPipe, ButtonComponent, ConfirmDialogComponent],
  templateUrl: './veiculos-pets.component.html',
  styleUrls: ['./veiculos-pets.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class VeiculosPetsComponent implements OnInit {
  private readonly idService = inject(IdentidadeCadastroService);
  private readonly condService = inject(CondominioService);
  readonly sessionService = inject(SessionService);

  readonly veiculos = signal<Veiculo[]>([]);
  readonly pets = signal<Pet[]>([]);
  readonly unidades = signal<Unidade[]>([]);
  readonly blocos = signal<Bloco[]>([]);
  readonly itemParaExcluir = signal<{ tipo: 'veiculo' | 'pet'; id: string; nome: string } | null>(null);

  // Filtros e busca
  readonly busca = signal<string>('');
  readonly filtroBloco = signal<string>('TODOS');
  readonly filtroUnidade = signal<string>('TODOS');

  readonly mostrarFormVeiculo = signal<boolean>(false);
  readonly salvandoVeiculo = signal<boolean>(false);
  readonly erroVeiculo = signal<string>('');

  novaPlaca = '';
  novoModelo = '';
  novaMarca = '';
  novaCor = '';
  veiculoUnidadeId = '';

  readonly mostrarFormPet = signal<boolean>(false);
  readonly salvandoPet = signal<boolean>(false);
  readonly erroPet = signal<string>('');

  novoNomePet = '';
  especiePet = 'CACHORRO';
  racaPet = '';
  portePet = 'MEDIO';
  vacinacaoEmDia = true;
  petUnidadeId = '';

  readonly petsVacinadosCount = computed(() => {
    return this.pets().filter(p => p.vacinacao_em_dia || p.vacinado).length;
  });

  readonly unidadesDisponiveisFiltro = computed(() => {
    const bId = this.filtroBloco();
    if (!bId || bId === 'TODOS') return this.unidades();
    return this.unidades().filter(u => (u.bloco_id || u.blocoId) === bId);
  });

  aoMudarFiltroBloco(novoBlocoId: string): void {
    this.filtroBloco.set(novoBlocoId);
    const unidAtual = this.filtroUnidade();
    if (unidAtual !== 'TODOS') {
      const u = this.unidades().find(item => item.id === unidAtual);
      if (novoBlocoId !== 'TODOS' && u && (u.bloco_id || u.blocoId) !== novoBlocoId) {
        this.filtroUnidade.set('TODOS');
      }
    }
  }

  limparFiltros(): void {
    this.busca.set('');
    this.filtroBloco.set('TODOS');
    this.filtroUnidade.set('TODOS');
  }

  getBlocoNome(blocoId?: string): string {
    if (!blocoId) return 'Geral';
    const b = this.blocos().find(item => item.id === blocoId);
    return b ? (b.nome || b.name || 'Geral') : 'Geral';
  }

  getUnidadeIdentificacao(unidadeId?: string): string {
    if (!unidadeId) return 'Sem unidade';
    const u = this.unidades().find(item => item.id === unidadeId);
    return u ? (u.identificacao || u.number || 'Unidade') : 'Unidade';
  }

  getUnidadeCompleta(unidadeId?: string): string {
    if (!unidadeId) return 'Sem unidade vinculada';
    const u = this.unidades().find(item => item.id === unidadeId);
    if (!u) return 'Unidade vinculada';
    const bloco = this.getBlocoNome(u.bloco_id || u.blocoId);
    return `Unidade ${u.identificacao || u.number} (${bloco})`;
  }

  readonly veiculosFiltrados = computed(() => {
    const termo = this.busca().trim().toLowerCase();
    const blocoId = this.filtroBloco();
    const unidadeId = this.filtroUnidade();

    return this.veiculos().filter(v => {
      // Filtro por Unidade
      if (unidadeId !== 'TODOS' && v.unidade_id !== unidadeId) return false;

      // Filtro por Torre / Bloco
      if (blocoId !== 'TODOS') {
        const u = this.unidades().find(item => item.id === v.unidade_id);
        if (!u || (u.bloco_id || u.blocoId) !== blocoId) return false;
      }

      // Busca textual (placa, modelo, marca, cor, unidade)
      if (!termo) return true;
      const placa = (v.placa || '').toLowerCase();
      const modelo = (v.modelo || '').toLowerCase();
      const marca = (v.marca || '').toLowerCase();
      const unidStr = this.getUnidadeCompleta(v.unidade_id).toLowerCase();

      const termoSemHifen = termo.replace(/[^a-z0-9]/g, '');
      const placaSemHifen = placa.replace(/[^a-z0-9]/g, '');

      return placa.includes(termo) ||
             placaSemHifen.includes(termoSemHifen) ||
             modelo.includes(termo) ||
             marca.includes(termo) ||
             unidStr.includes(termo);
    });
  });

  readonly petsFiltrados = computed(() => {
    const termo = this.busca().trim().toLowerCase();
    const blocoId = this.filtroBloco();
    const unidadeId = this.filtroUnidade();

    return this.pets().filter(p => {
      // Filtro por Unidade
      if (unidadeId !== 'TODOS' && p.unidade_id !== unidadeId) return false;

      // Filtro por Torre / Bloco
      if (blocoId !== 'TODOS') {
        const u = this.unidades().find(item => item.id === p.unidade_id);
        if (!u || (u.bloco_id || u.blocoId) !== blocoId) return false;
      }

      // Busca textual (nome, espécie, raça, unidade)
      if (!termo) return true;
      const nome = (p.nome || '').toLowerCase();
      const especie = (p.especie || '').toLowerCase();
      const raca = (p.raca || '').toLowerCase();
      const unidStr = this.getUnidadeCompleta(p.unidade_id).toLowerCase();

      return nome.includes(termo) ||
             especie.includes(termo) ||
             raca.includes(termo) ||
             unidStr.includes(termo);
    });
  });

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    const cid = this.sessionService.condominioAtivoId() || undefined;

    this.idService.getVeiculos(undefined, cid).subscribe({
      next: (dados) => this.veiculos.set(dados),
      error: (e) => console.warn('Erro ao carregar veículos:', e)
    });

    this.idService.getPets(undefined, cid).subscribe({
      next: (dados) => this.pets.set(dados),
      error: (e) => console.warn('Erro ao carregar pets:', e)
    });

    this.condService.getUnits(undefined, cid).subscribe({
      next: (dados) => {
        const escopo = this.sessionService.unidadeIdsEscopo();
        if (this.sessionService.escopoSomenteUnidade() && escopo.length > 0) {
          this.unidades.set(dados.filter((u) => escopo.includes(String(u.id))));
        } else {
          this.unidades.set(dados);
        }
      },
      error: (e) => console.warn('Erro ao carregar unidades:', e)
    });

    this.condService.getBlocks(cid).subscribe({
      next: (dados) => this.blocos.set(dados),
      error: (e) => console.warn('Erro ao carregar blocos:', e)
    });
  }

  formatarPlacaInput(valor: string): void {
    this.novaPlaca = (valor || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  }

  salvarVeiculo(): void {
    if (!this.novaPlaca.trim() || !this.novoModelo.trim() || !this.veiculoUnidadeId) return;

    this.salvandoVeiculo.set(true);
    this.erroVeiculo.set('');

    const payload = {
      placa: this.novaPlaca.trim().toUpperCase(),
      modelo: this.novoModelo.trim(),
      marca: this.novaMarca.trim() || undefined,
      cor: this.novaCor.trim() || undefined,
      unidade_id: this.veiculoUnidadeId,
      condominio_id: this.sessionService.condominioAtivoId() || undefined
    };

    this.idService.createVeiculo(payload).subscribe({
      next: (novo) => {
        this.salvandoVeiculo.set(false);
        this.veiculos.update(lista => [novo, ...lista]);
        this.mostrarFormVeiculo.set(false);
        this.novaPlaca = '';
        this.novoModelo = '';
        this.novaMarca = '';
        this.novaCor = '';
      },
      error: (err) => {
        this.salvandoVeiculo.set(false);
        this.erroVeiculo.set(err?.error?.detail || 'Erro ao registrar veículo. Verifique se a placa já existe.');
      }
    });
  }

  salvarPet(): void {
    if (!this.novoNomePet.trim() || !this.petUnidadeId) return;

    this.salvandoPet.set(true);
    this.erroPet.set('');

    const payload = {
      nome: this.novoNomePet.trim(),
      especie: this.especiePet,
      raca: this.racaPet.trim() || undefined,
      porte: this.portePet,
      vacinacao_em_dia: this.vacinacaoEmDia,
      unidade_id: this.petUnidadeId,
      condominio_id: this.sessionService.condominioAtivoId() || undefined
    };

    this.idService.createPet(payload).subscribe({
      next: (novo) => {
        this.salvandoPet.set(false);
        this.pets.update(lista => [novo, ...lista]);
        this.mostrarFormPet.set(false);
        this.novoNomePet = '';
        this.racaPet = '';
      },
      error: (err) => {
        this.salvandoPet.set(false);
        this.erroPet.set(err?.error?.detail || 'Erro ao registrar animal doméstico.');
      }
    });
  }

  podeExcluirVeiculo(v: Veiculo): boolean {
    if (!v.id) return false;
    if (this.sessionService.podeGerenciarCadastros()) return true;
    return this.sessionService.escopoSomenteUnidade() &&
           this.sessionService.unidadeIdsEscopo().includes(String(v.unidade_id));
  }

  podeExcluirPet(p: Pet): boolean {
    if (!p.id) return false;
    if (this.sessionService.podeGerenciarCadastros()) return true;
    return this.sessionService.escopoSomenteUnidade() &&
           this.sessionService.unidadeIdsEscopo().includes(String(p.unidade_id));
  }

  confirmarExclusaoVeiculo(v: Veiculo): void {
    if (!v.id) return;
    this.itemParaExcluir.set({
      tipo: 'veiculo',
      id: v.id,
      nome: `o veículo ${v.modelo} (Placa ${v.placa})`
    });
  }

  confirmarExclusaoPet(p: Pet): void {
    if (!p.id) return;
    this.itemParaExcluir.set({
      tipo: 'pet',
      id: p.id,
      nome: `o animal ${p.nome}`
    });
  }

  executarExclusao(): void {
    const item = this.itemParaExcluir();
    if (!item) return;

    if (item.tipo === 'veiculo') {
      this.idService.deleteVeiculo(item.id).subscribe({
        next: () => {
          this.veiculos.update(lista => lista.filter(v => v.id !== item.id));
          this.itemParaExcluir.set(null);
        },
        error: (err) => {
          alert(err?.error?.detail || 'Erro ao excluir veículo.');
          this.itemParaExcluir.set(null);
        }
      });
    } else {
      this.idService.deletePet(item.id).subscribe({
        next: () => {
          this.pets.update(lista => lista.filter(p => p.id !== item.id));
          this.itemParaExcluir.set(null);
        },
        error: (err) => {
          alert(err?.error?.detail || 'Erro ao excluir animal.');
          this.itemParaExcluir.set(null);
        }
      });
    }
  }
}
