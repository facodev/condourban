import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatRipple } from '@angular/material/core';
import {
  IdentidadeCadastroService,
  UsuarioPerfil,
  Pessoa,
  OcupacaoUnidade
} from '../../services/identidade-cadastro.service';
import { CondominioService, Bloco, Unidade } from '../../../condominio/services/condominio.service';
import { SessionService } from '../../../../core/services/session.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    RouterLinkActive,
    MatRipple,
    StatusBadgeComponent,
    ButtonComponent,
    ConfirmDialogComponent
  ],
  templateUrl: './usuarios.component.html',
  styleUrls: ['./usuarios.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class UsuariosComponent implements OnInit {
  private readonly service = inject(IdentidadeCadastroService);
  private readonly condService = inject(CondominioService);
  readonly sessionService = inject(SessionService);

  readonly usuarios = signal<UsuarioPerfil[]>([]);
  readonly pessoas = signal<Pessoa[]>([]);
  readonly ocupacoes = signal<OcupacaoUnidade[]>([]);
  readonly blocos = signal<Bloco[]>([]);
  readonly unidades = signal<Unidade[]>([]);

  readonly mostrarModal = signal<boolean>(false);
  readonly usuarioEmEdicao = signal<UsuarioPerfil | null>(null);
  readonly usuarioParaExcluir = signal<UsuarioPerfil | null>(null);
  readonly salvando = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  // Filtros no mesmo padrão de Vínculos & Ocupações
  readonly busca = signal<string>('');
  readonly filtroBloco = signal<string>('TODOS');
  readonly filtroUnidade = signal<string>('TODOS');
  readonly filtroPapel = signal<string>('TODOS');
  readonly filtroStatus = signal<string>('TODOS');

  // Paginação da tabela
  readonly paginaAtual = signal<number>(1);
  readonly itensPorPagina = signal<number>(10);

  toastMensagem = signal<string>('');
  toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  formModel = {
    nome_completo: '',
    email: '',
    senha: '',
    papel: 'MORADOR',
    ativo: true
  };

  readonly totalAtivos = computed(() => {
    return this.usuarios().filter(u => u.ativo !== false).length;
  });

  readonly unidadesDisponiveisFiltro = computed(() => {
    const bId = this.filtroBloco();
    if (!bId || bId === 'TODOS') return this.unidades();
    return this.unidades().filter(u => (u.bloco_id || u.blocoId) === bId);
  });

  readonly usuariosFiltrados = computed(() => {
    const termo = this.busca().trim().toLowerCase();
    const blocoId = this.filtroBloco();
    const unidadeId = this.filtroUnidade();
    const papel = this.filtroPapel();
    const status = this.filtroStatus();

    return this.usuarios().filter(user => {
      // Filtro por Status
      const isAtivo = user.ativo !== false;
      if (status === 'ATIVO' && !isAtivo) return false;
      if (status === 'INATIVO' && isAtivo) return false;

      // Filtro por Papel RBAC
      if (papel !== 'TODOS') {
        const codigoPapel = this.getRoleCode(user);
        if (codigoPapel !== papel) return false;
      }

      // Filtro por Unidade e Bloco (via pessoa/ocupação vinculada)
      const unidadesDoUsuario = this.getUnidadesDoUsuario(user);
      if (unidadeId !== 'TODOS') {
        if (!unidadesDoUsuario.some(u => u.id === unidadeId)) return false;
      }
      if (blocoId !== 'TODOS') {
        if (!unidadesDoUsuario.some(u => (u.bloco_id || u.blocoId) === blocoId)) return false;
      }

      if (!termo) return true;

      const nome = (user.nomeCompleto || user.nome_completo || user.nome || '').toLowerCase();
      const email = (user.email || '').toLowerCase();
      const roleLabel = this.getRoleLabel(user).toLowerCase();
      const unidadeLabel = this.getUnidadeResumo(user).toLowerCase();

      return (
        nome.includes(termo) ||
        email.includes(termo) ||
        roleLabel.includes(termo) ||
        unidadeLabel.includes(termo)
      );
    });
  });

  readonly totalPaginas = computed(() => {
    return Math.max(1, Math.ceil(this.usuariosFiltrados().length / this.itensPorPagina()));
  });

  readonly usuariosPaginados = computed(() => {
    const tam = this.itensPorPagina();
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    const inicio = (pag - 1) * tam;
    return this.usuariosFiltrados().slice(inicio, inicio + tam);
  });

  readonly indiceInicial = computed(() => {
    if (this.usuariosFiltrados().length === 0) return 0;
    return (Math.min(this.paginaAtual(), this.totalPaginas()) - 1) * this.itensPorPagina() + 1;
  });

  readonly indiceFinal = computed(() => {
    return Math.min(this.usuariosFiltrados().length, this.indiceInicial() + this.usuariosPaginados().length - 1);
  });

  readonly paginasArray = computed(() => {
    return Array.from({ length: this.totalPaginas() }, (_, i) => i + 1);
  });

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    const cid = this.sessionService.condominioAtivoId() || undefined;
    this.carregarUsuarios();
    this.service.getPessoas(cid).subscribe({
      next: (dados) => this.pessoas.set(dados),
      error: () => {}
    });
    this.service.getOcupacoes(undefined, false, cid).subscribe({
      next: (dados) => this.ocupacoes.set(dados),
      error: () => {}
    });
    this.condService.getBlocks().subscribe({
      next: (dados) => this.blocos.set(dados),
      error: () => {}
    });
    this.condService.getUnits().subscribe({
      next: (dados) => this.unidades.set(dados),
      error: () => {}
    });
  }

  carregarUsuarios(): void {
    const cid = this.sessionService.condominioAtivoId() || undefined;
    this.service.getUsuarios(cid).subscribe({
      next: (dados) => this.usuarios.set(dados),
      error: (e) => {
        console.warn('Erro ao carregar usuários:', e);
        this.mostrarToast('Erro ao carregar usuários: ' + (e?.error?.detail || e.message), 'erro');
      }
    });
  }

  aoMudarBusca(valor: string): void {
    this.busca.set(valor);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroBloco(novoBlocoId: string): void {
    this.filtroBloco.set(novoBlocoId);
    const unidAtual = this.filtroUnidade();
    if (unidAtual !== 'TODOS') {
      const u = this.unidades().find(item => item.id === unidAtual);
      if (novoBlocoId !== 'TODOS' && u && (u.bloco_id || u.blocoId) !== novoBlocoId) {
        this.filtroUnidade.set('TODOS');
      }
    }
    this.paginaAtual.set(1);
  }

  aoMudarFiltroUnidade(unidadeId: string): void {
    this.filtroUnidade.set(unidadeId);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroPapel(papel: string): void {
    this.filtroPapel.set(papel);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroStatus(status: string): void {
    this.filtroStatus.set(status);
    this.paginaAtual.set(1);
  }

  limparFiltros(): void {
    this.busca.set('');
    this.filtroBloco.set('TODOS');
    this.filtroUnidade.set('TODOS');
    this.filtroPapel.set('TODOS');
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

  getUnidadesDoUsuario(user: UsuarioPerfil): Unidade[] {
    const emailNorm = (user.email || '').trim().toLowerCase();
    if (!emailNorm) return [];
    const pessoa = this.pessoas().find(p => (p.email || '').trim().toLowerCase() === emailNorm);
    if (!pessoa) return [];
    const ocs = this.ocupacoes().filter(oc => oc.pessoa_id === pessoa.id && oc.status === 'ATIVA');
    const uIds = new Set(ocs.map(oc => oc.unidade_id));
    return this.unidades().filter(u => uIds.has(u.id));
  }

  getUnidadeResumo(user: UsuarioPerfil): string {
    const unids = this.getUnidadesDoUsuario(user);
    if (unids.length === 0) return 'Administração / Geral';
    return unids
      .map(u => {
        const b = this.blocos().find(item => item.id === (u.bloco_id || u.blocoId));
        const bNome = b ? (b.nome || b.name) : '';
        return bNome ? `Unid. ${u.identificacao || u.number} (${bNome})` : `Unid. ${u.identificacao || u.number}`;
      })
      .join(', ');
  }

  abrirCriacao(): void {
    this.usuarioEmEdicao.set(null);
    this.formModel = {
      nome_completo: '',
      email: '',
      senha: '',
      papel: 'MORADOR',
      ativo: true
    };
    this.errorMessage.set('');
    this.mostrarModal.set(true);
  }

  abrirEdicao(user: UsuarioPerfil): void {
    this.usuarioEmEdicao.set(user);
    const papelAtual = this.getRoleCode(user);
    this.formModel = {
      nome_completo: user.nomeCompleto || user.nome_completo || user.nome || '',
      email: user.email || '',
      senha: '',
      papel: papelAtual,
      ativo: user.ativo !== false
    };
    this.errorMessage.set('');
    this.mostrarModal.set(true);
  }

  fecharModal(): void {
    this.mostrarModal.set(false);
    this.usuarioEmEdicao.set(null);
    this.errorMessage.set('');
  }

  salvarUsuario(): void {
    if (!this.formModel.email.trim()) return;

    this.salvando.set(true);
    this.errorMessage.set('');

    const editando = this.usuarioEmEdicao();

    if (editando) {
      const payload: any = {
        email: this.formModel.email.trim(),
        nome_completo: this.formModel.nome_completo.trim() || undefined,
        papel: this.formModel.papel,
        ativo: this.formModel.ativo
      };
      if (this.formModel.senha.trim()) {
        payload.senha = this.formModel.senha.trim();
      }

      this.service.updateUsuario(editando.id, payload).subscribe({
        next: (atualizado) => {
          this.salvando.set(false);
          this.mostrarToast(`Usuário "${atualizado.email}" atualizado com sucesso!`);
          this.fecharModal();
          this.carregarUsuarios();
        },
        error: (err) => {
          this.salvando.set(false);
          this.errorMessage.set(err?.error?.detail || 'Erro ao atualizar usuário.');
        }
      });
    } else {
      if (!this.formModel.senha.trim()) {
        this.salvando.set(false);
        this.errorMessage.set('Informe uma senha inicial para o novo usuário.');
        return;
      }

      const payload = {
        email: this.formModel.email.trim(),
        senha: this.formModel.senha.trim(),
        nome_completo: this.formModel.nome_completo.trim() || undefined,
        papel: this.formModel.papel,
        condominio_id: this.sessionService.condominioAtivoId() || undefined
      };

      this.service.createUsuario(payload).subscribe({
        next: (criado) => {
          this.salvando.set(false);
          this.mostrarToast(`Usuário "${criado.email}" criado com sucesso!`);
          this.fecharModal();
          this.carregarUsuarios();
        },
        error: (err) => {
          this.salvando.set(false);
          this.errorMessage.set(err?.error?.detail || 'Erro ao criar usuário.');
        }
      });
    }
  }

  confirmarExclusao(user: UsuarioPerfil): void {
    this.usuarioParaExcluir.set(user);
  }

  executarExclusao(): void {
    const user = this.usuarioParaExcluir();
    if (!user) return;

    this.service.deleteUsuario(user.id).subscribe({
      next: () => {
        this.usuarios.update(lista => lista.filter(u => u.id !== user.id));
        this.mostrarToast(`Usuário "${user.email}" excluído com sucesso!`);
        this.usuarioParaExcluir.set(null);
      },
      error: (err) => {
        this.mostrarToast(err?.error?.detail || 'Erro ao excluir usuário.', 'erro');
        this.usuarioParaExcluir.set(null);
      }
    });
  }

  getRoleCode(user: UsuarioPerfil): string {
    const papel = (
      user.papeis && user.papeis.length
        ? user.papeis[0]
        : user.roles && user.roles.length
          ? user.roles[0]
          : ''
    )?.toUpperCase();

    if (papel === 'SUPERADMIN' || papel === 'ADMIN' || papel === 'SINDICO') return 'SINDICO';
    if (papel === 'SUBSINDICO' || papel === 'CONSELHO') return 'SUBSINDICO';
    if (papel === 'ADMINISTRADORA') return 'ADMINISTRADORA';
    if (papel === 'PORTARIA' || papel === 'PORTEIRO') return 'PORTARIA';
    if (papel === 'ZELADOR') return 'ZELADOR';
    if (papel === 'MORADOR') return 'MORADOR';

    const email = (user.email || '').toLowerCase();
    if (email.includes('sindico') || email.includes('admin')) return 'SINDICO';
    if (email.includes('portaria') || email.includes('guarita')) return 'PORTARIA';
    return 'MORADOR';
  }

  getRoleLabel(user: UsuarioPerfil): string {
    const code = this.getRoleCode(user);
    if (code === 'SINDICO') return 'SÍNDICO GERAL';
    if (code === 'SUBSINDICO') return 'SUBSÍNDICO';
    if (code === 'ADMINISTRADORA') return 'ADMINISTRADORA';
    if (code === 'PORTARIA') return 'PORTARIA & CONTROLE';
    if (code === 'ZELADOR') return 'ZELADORIA';
    return 'MORADOR TITULAR';
  }

  getRoleClass(user: UsuarioPerfil): string {
    const code = this.getRoleCode(user);
    if (code === 'SINDICO' || code === 'SUBSINDICO' || code === 'ADMINISTRADORA') return 'sindico';
    if (code === 'PORTARIA' || code === 'ZELADOR') return 'portaria';
    return 'morador';
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
