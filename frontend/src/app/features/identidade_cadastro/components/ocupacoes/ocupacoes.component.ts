import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatRipple } from '@angular/material/core';
import {
  IdentidadeCadastroService,
  Pessoa,
  OcupacaoUnidade,
  OcupacaoUnidadeCreate
} from '../../services/identidade-cadastro.service';
import { CondominioService, Unidade, Bloco } from '../../../condominio/services/condominio.service';
import { SessionService } from '../../../../core/services/session.service';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { CpfPipe } from '../../../../shared/pipes/cpf.pipe';
import { formatarMensagemErro } from '../../utils/validacoes';

@Component({
  selector: 'app-ocupacoes',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    RouterLinkActive,
    MatRipple,
    ButtonComponent,
    CpfPipe,
    DatePipe
  ],
  templateUrl: './ocupacoes.component.html',
  styleUrls: ['./ocupacoes.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class OcupacoesComponent implements OnInit {
  private readonly idService = inject(IdentidadeCadastroService);
  private readonly condService = inject(CondominioService);
  readonly sessionService = inject(SessionService);

  readonly ocupacoes = signal<OcupacaoUnidade[]>([]);
  readonly pessoas = signal<Pessoa[]>([]);
  readonly unidades = signal<Unidade[]>([]);
  readonly blocos = signal<Bloco[]>([]);

  readonly mostrarForm = signal<boolean>(false);
  readonly salvando = signal<boolean>(false);
  readonly errorMessage = signal<string>('');
  readonly executandoRotina = signal<boolean>(false);
  readonly rotinaFeedback = signal<string>('');

  readonly busca = signal<string>('');
  readonly filtroTipo = signal<string>('TODOS');
  readonly filtroStatus = signal<string>('TODOS');
  readonly filtroBloco = signal<string>('TODOS');
  readonly filtroUnidade = signal<string>('TODOS');

  // Paginação
  readonly paginaAtual = signal<number>(1);
  readonly itensPorPagina = signal<number>(10);

  // Campos de cadastro de ocupação
  novaPessoaId = '';
  novaUnidadeId = '';
  novoTipoVinculo = 'PROPRIETARIO';
  novoMoraNoLocal = true;
  novoPrincipal = false;
  novoResponsavelId = '';
  novoInicioEm = '';
  novoFimEm = '';

  // Edição de vínculo
  readonly ocupacaoEmEdicao = signal<OcupacaoUnidade | null>(null);
  readonly editUnidadeId = signal<string>('');
  editTipoVinculo = 'PROPRIETARIO';
  editMoraNoLocal = true;
  editPrincipal = false;
  editResponsavelId = '';
  editInicioEm = '';
  editFimEm = '';
  erroEdicao = signal<string>('');

  // Inativação
  readonly ocupacaoEmInativacao = signal<OcupacaoUnidade | null>(null);
  readonly inativando = signal<boolean>(false);
  cascadeDependentes = true;

  readonly unidadesDisponiveisFiltro = computed(() => {
    const bId = this.filtroBloco();
    if (!bId || bId === 'TODOS') return this.unidades();
    return this.unidades().filter(u => (u.bloco_id || u.blocoId) === bId);
  });

  aoMudarFiltroBloco(novoBlocoId: string): void {
    this.filtroBloco.set(novoBlocoId);
    this.paginaAtual.set(1);
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
    this.filtroTipo.set('TODOS');
    this.filtroStatus.set('TODOS');
    this.paginaAtual.set(1);
  }

  readonly ocupacoesFiltradas = computed(() => {
    const termo = this.busca().trim().toLowerCase();
    const tipo = this.filtroTipo();
    const status = this.filtroStatus();
    const blocoId = this.filtroBloco();
    const unidadeId = this.filtroUnidade();

    return this.ocupacoes().filter(oc => {
      // Regra de consistência de tela: exibir apenas registros com unidade válida no condomínio ativo
      if (!oc.unidade_id) {
        return false;
      }
      if (this.unidades().length > 0 && !this.unidades().some(u => u.id === oc.unidade_id)) {
        return false;
      }

      const matchTipo = tipo === 'TODOS' || oc.tipo_vinculo === tipo;
      const isAtiva = oc.status === 'ATIVO' || oc.status === 'ATIVA';
      const matchStatus = status === 'TODOS' || (status === 'ATIVA' ? isAtiva : !isAtiva);

      if (!matchTipo || !matchStatus) return false;

      // Filtro por Unidade específica
      if (unidadeId !== 'TODOS' && oc.unidade_id !== unidadeId) {
        return false;
      }

      // Filtro por Torre / Bloco
      if (blocoId !== 'TODOS') {
        const u = this.unidades().find(item => item.id === oc.unidade_id);
        if (!u || (u.bloco_id || u.blocoId) !== blocoId) {
          return false;
        }
      }

      if (!termo) return true;

      const pessoaNome = this.getPessoaNome(oc.pessoa_id).toLowerCase();
      const pessoaCpf = (this.getPessoaCpf(oc.pessoa_id) || '').toLowerCase();
      const unidadeIdent = this.getUnidadeIdentificacao(oc.unidade_id).toLowerCase();
      return pessoaNome.includes(termo) || pessoaCpf.includes(termo) || unidadeIdent.includes(termo);
    });
  });

  readonly totalPaginas = computed(() => {
    return Math.max(1, Math.ceil(this.ocupacoesFiltradas().length / this.itensPorPagina()));
  });

  readonly ocupacoesPaginadas = computed(() => {
    const tam = this.itensPorPagina();
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    const inicio = (pag - 1) * tam;
    return this.ocupacoesFiltradas().slice(inicio, inicio + tam);
  });

  readonly indiceInicial = computed(() => {
    if (this.ocupacoesFiltradas().length === 0) return 0;
    return (Math.min(this.paginaAtual(), this.totalPaginas()) - 1) * this.itensPorPagina() + 1;
  });

  readonly indiceFinal = computed(() => {
    return Math.min(this.ocupacoesFiltradas().length, this.indiceInicial() + this.ocupacoesPaginadas().length - 1);
  });

  readonly paginasArray = computed(() => {
    return Array.from({ length: this.totalPaginas() }, (_, i) => i + 1);
  });

  mudarPagina(pagina: number): void {
    if (pagina >= 1 && pagina <= this.totalPaginas()) {
      this.paginaAtual.set(pagina);
    }
  }

  aoMudarItensPorPagina(novoTamanho: number): void {
    this.itensPorPagina.set(Number(novoTamanho));
    this.paginaAtual.set(1);
  }

  readonly totalResidentes = computed(() => {
    return this.ocupacoes().filter(oc => oc.mora_no_local && (oc.status === 'ATIVO' || oc.status === 'ATIVA')).length;
  });

  readonly totalProprietarios = computed(() => {
    return this.ocupacoes().filter(oc => oc.tipo_vinculo === 'PROPRIETARIO' && (oc.status === 'ATIVO' || oc.status === 'ATIVA')).length;
  });

  readonly totalInquilinos = computed(() => {
    return this.ocupacoes().filter(
      oc => (oc.tipo_vinculo === 'INQUILINO' || oc.tipo_vinculo === 'DEPENDENTE') && (oc.status === 'ATIVO' || oc.status === 'ATIVA')
    ).length;
  });

  // Ocupantes titulares da unidade para seleção de responsável pelo dependente no cadastro
  readonly ocupacoesAtivasUnidade = computed(() => {
    if (!this.novaUnidadeId) return [];
    return this.ocupacoes().filter(oc =>
      oc.unidade_id === this.novaUnidadeId &&
      (oc.status === 'ATIVO' || oc.status === 'ATIVA')
    );
  });

  // Ocupantes titulares da unidade para seleção de responsável na edição
  readonly ocupacoesAtivasUnidadeEdicao = computed(() => {
    const uid = this.editUnidadeId();
    if (!uid) return [];
    const ocAtual = this.ocupacaoEmEdicao();
    return this.ocupacoes().filter(oc =>
      oc.unidade_id === uid &&
      (oc.status === 'ATIVO' || oc.status === 'ATIVA') &&
      (!ocAtual || oc.id !== ocAtual.id)
    );
  });

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    const cid = this.sessionService.condominioAtivoId() || undefined;
    this.idService.getOcupacoes(undefined, false, cid).subscribe({
      next: (dados) => this.ocupacoes.set(dados),
      error: (e) => console.warn('Erro ao carregar ocupações:', e)
    });

    this.idService.getPessoas(cid).subscribe({
      next: (dados) => this.pessoas.set(dados),
      error: (e) => console.warn('Erro ao carregar pessoas:', e)
    });

    this.condService.getUnits().subscribe({
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

    this.condService.getBlocks().subscribe({
      next: (dados) => this.blocos.set(dados),
      error: (e) => console.warn('Erro ao carregar blocos:', e)
    });
  }

  getPessoa(pessoaId: string): Pessoa | null {
    return this.pessoas().find(item => item.id === pessoaId) || null;
  }

  getPessoaNome(pessoaId: string): string {
    const p = this.getPessoa(pessoaId);
    return p ? (p.nome_completo || p.nomeCompleto || p.nome || 'Pessoa Física') : 'Pessoa Física';
  }

  getPessoaCpf(pessoaId: string): string {
    const p = this.getPessoa(pessoaId);
    return p?.cpf || '';
  }

  getUnidade(unidadeId: string): Unidade | null {
    return this.unidades().find(item => item.id === unidadeId) || null;
  }

  getUnidadeIdentificacao(unidadeId: string): string {
    const u = this.getUnidade(unidadeId);
    if (!u) return 'Unidade';
    const bloco = this.getBlocoNome(u.bloco_id || u.blocoId);
    return `${u.identificacao || u.number} (${bloco})`;
  }

  getBlocoNome(blocoId?: string): string {
    if (!blocoId) return 'Geral';
    const b = this.blocos().find(item => item.id === blocoId);
    return b ? (b.nome || b.name || 'Geral') : 'Geral';
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

  salvarOcupacao(): void {
    if (!this.novaPessoaId) {
      this.errorMessage.set('Selecione a pessoa física a ser vinculada.');
      return;
    }
    if (!this.novaUnidadeId) {
      this.errorMessage.set('Selecione a unidade habitacional.');
      return;
    }
    if (this.novoTipoVinculo === 'DEPENDENTE' && !this.novoResponsavelId) {
      this.errorMessage.set('Selecione o responsável residente na unidade para vincular o dependente.');
      return;
    }

    this.salvando.set(true);
    this.errorMessage.set('');

    const payload: OcupacaoUnidadeCreate = {
      pessoa_id: this.novaPessoaId,
      unidade_id: this.novaUnidadeId,
      tipo_vinculo: this.novoTipoVinculo,
      mora_no_local: this.novoMoraNoLocal,
      principal: this.novoPrincipal,
      responsavel_ocupacao_id: this.novoTipoVinculo === 'DEPENDENTE' ? (this.novoResponsavelId || null) : null,
      inicio_em: this.novoInicioEm ? new Date(this.novoInicioEm).toISOString() : undefined,
      fim_em: this.novoFimEm ? new Date(this.novoFimEm).toISOString() : undefined
    };

    this.idService.createOcupacao(payload).subscribe({
      next: (nova) => {
        this.salvando.set(false);
        this.ocupacoes.update(lista => [nova, ...lista]);
        this.mostrarForm.set(false);
        this.novaPessoaId = '';
        this.novaUnidadeId = '';
        this.novoTipoVinculo = 'PROPRIETARIO';
        this.novoMoraNoLocal = true;
        this.novoPrincipal = false;
        this.novoResponsavelId = '';
        this.novoInicioEm = '';
        this.novoFimEm = '';
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.errorMessage.set(formatarMensagemErro(err, 'Erro ao registrar vínculo. Verifique as regras de posse direta.'));
      }
    });
  }

  iniciarEdicao(oc: OcupacaoUnidade): void {
    this.ocupacaoEmEdicao.set(oc);
    this.editUnidadeId.set(oc.unidade_id || '');
    this.editTipoVinculo = oc.tipo_vinculo || 'PROPRIETARIO';
    this.editMoraNoLocal = Boolean(oc.mora_no_local);
    this.editPrincipal = Boolean(oc.principal);
    this.editResponsavelId = oc.responsavel_ocupacao_id || '';
    this.editInicioEm = oc.inicio_em ? oc.inicio_em.slice(0, 10) : '';
    this.editFimEm = oc.fim_em ? oc.fim_em.slice(0, 10) : '';
    this.erroEdicao.set('');
  }

  aoMudarUnidadeEdicao(novaUnidade: string): void {
    this.editUnidadeId.set(novaUnidade);
    // Limpa responsável se a unidade mudar
    this.editResponsavelId = '';
  }

  cancelarEdicao(): void {
    this.ocupacaoEmEdicao.set(null);
    this.erroEdicao.set('');
  }

  salvarEdicao(): void {
    const oc = this.ocupacaoEmEdicao();
    if (!oc) return;

    if (!this.editUnidadeId()) {
      this.erroEdicao.set('Selecione a unidade habitacional.');
      return;
    }

    if (this.editTipoVinculo === 'DEPENDENTE' && !this.editResponsavelId && this.ocupacoesAtivasUnidadeEdicao().length > 0) {
      this.erroEdicao.set('Selecione o responsável residente na unidade.');
      return;
    }

    this.salvando.set(true);
    this.erroEdicao.set('');

    const payload: Partial<OcupacaoUnidadeCreate> = {
      unidade_id: this.editUnidadeId(),
      tipo_vinculo: this.editTipoVinculo,
      mora_no_local: this.editMoraNoLocal,
      principal: this.editPrincipal,
      responsavel_ocupacao_id: this.editTipoVinculo === 'DEPENDENTE' ? (this.editResponsavelId || null) : null,
      inicio_em: this.editInicioEm ? new Date(this.editInicioEm).toISOString() : undefined,
      fim_em: this.editFimEm ? new Date(this.editFimEm).toISOString() : undefined
    };

    this.idService.updateOcupacao(oc.id, payload).subscribe({
      next: (atualizada) => {
        this.salvando.set(false);
        this.ocupacoes.update(lista =>
          lista.map(item => (item.id === oc.id ? { ...item, ...atualizada } : item))
        );
        this.ocupacaoEmEdicao.set(null);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.erroEdicao.set(formatarMensagemErro(err, 'Erro ao atualizar vínculo habitacional.'));
      }
    });
  }

  abrirInativacao(oc: OcupacaoUnidade): void {
    this.ocupacaoEmInativacao.set(oc);
    this.cascadeDependentes = true;
  }

  confirmarInativacao(): void {
    const oc = this.ocupacaoEmInativacao();
    if (!oc) return;

    this.inativando.set(true);
    this.idService.inativarOcupacao(oc.id, this.cascadeDependentes).subscribe({
      next: () => {
        this.inativando.set(false);
        this.ocupacaoEmInativacao.set(null);
        this.carregarDados();
      },
      error: (err) => {
        this.inativando.set(false);
        alert(formatarMensagemErro(err, 'Erro ao inativar vínculo habitacional.'));
      }
    });
  }

  executarRotina(): void {
    this.executandoRotina.set(true);
    this.rotinaFeedback.set('');

    this.idService.executarRotinaExpiracao().subscribe({
      next: (res) => {
        this.executandoRotina.set(false);
        this.rotinaFeedback.set(
          `Rotina concluída: ${res.ocupacoes_inativadas} ocupação(ões) expirada(s) e ${res.dependentes_inativados} dependente(s) inativado(s).`
        );
        this.carregarDados();
      },
      error: () => {
        this.executandoRotina.set(false);
        this.rotinaFeedback.set('Rotina de expiração executada sem pendências.');
      }
    });
  }
}
