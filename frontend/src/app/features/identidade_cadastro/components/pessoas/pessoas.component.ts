import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatRipple } from '@angular/material/core';
import { IdentidadeCadastroService, Pessoa, PessoaUpdate, TelefoneItem } from '../../services/identidade-cadastro.service';
import { SessionService } from '../../../../core/services/session.service';
import { CpfPipe } from '../../../../shared/pipes/cpf.pipe';
import { PhonePipe } from '../../../../shared/pipes/phone.pipe';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import {
  validarCpf,
  formatarCpf,
  validarTelefone,
  formatarTelefone,
  validarEmail,
  formatarMensagemErro,
  TelefoneModel
} from '../../utils/validacoes';

@Component({
  selector: 'app-pessoas',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    RouterLinkActive,
    MatRipple,
    CpfPipe,
    PhonePipe,
    ButtonComponent,
    StatusBadgeComponent,
    ConfirmDialogComponent
  ],
  templateUrl: './pessoas.component.html',
  styleUrls: ['./pessoas.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class PessoasComponent implements OnInit {
  private readonly service = inject(IdentidadeCadastroService);
  readonly sessionService = inject(SessionService);

  readonly pessoas = signal<Pessoa[]>([]);
  readonly mostrarForm = signal<boolean>(false);
  readonly salvando = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  // Filtros
  readonly busca = signal<string>('');
  readonly filtroCadastro = signal<string>('TODOS');

  // Paginação da tabela
  readonly paginaAtual = signal<number>(1);
  readonly itensPorPagina = signal<number>(10);

  toastMensagem = signal<string>('');
  toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  // CAMPOS DE NOVO CADASTRO
  novoNome = '';
  novoEmail = '';
  novoCpf = '';
  readonly telefonesNovo = signal<TelefoneModel[]>([
    { numero: '', tipo: 'celular', principal: true, whatsapp: true }
  ]);

  // ESTADO DE EDIÇÃO DE PESSOA (MODAL)
  readonly pessoaEmEdicao = signal<Pessoa | null>(null);
  readonly salvandoEdicao = signal<boolean>(false);
  readonly erroEdicao = signal<string>('');

  editNome = '';
  editEmail = '';
  editCpf = '';
  readonly telefonesEdicao = signal<TelefoneModel[]>([]);

  // ESTADO DE EXCLUSÃO DE PESSOA
  readonly pessoaEmExclusao = signal<Pessoa | null>(null);
  readonly excluindo = signal<boolean>(false);
  readonly erroExclusao = signal<string>('');

  readonly pessoasFiltradas = computed(() => {
    const termo = this.busca().trim().toLowerCase();
    const filtro = this.filtroCadastro();

    return this.pessoas().filter(p => {
      if (filtro === 'COM_CPF' && !p.cpf) return false;
      if (filtro === 'SEM_CPF' && !!p.cpf) return false;
      if (filtro === 'COM_CONTATO' && !(p.celular || p.telefone || (p.telefones && p.telefones.length > 0))) return false;

      if (!termo) return true;
      const nome = (p.nome_completo || p.nomeCompleto || p.nome || '').toLowerCase();
      const email = (p.email || '').toLowerCase();
      const cpf = (p.cpf || '').toLowerCase();
      const fone = (p.celular || p.telefone || '').toLowerCase();
      const telefonesStr = (p.telefones || []).map(t => t.numero).join(' ').toLowerCase();
      return nome.includes(termo) || email.includes(termo) || cpf.includes(termo) || fone.includes(termo) || telefonesStr.includes(termo);
    });
  });

  readonly totalPaginas = computed(() => {
    return Math.max(1, Math.ceil(this.pessoasFiltradas().length / this.itensPorPagina()));
  });

  readonly pessoasPaginadas = computed(() => {
    const tam = this.itensPorPagina();
    const pag = Math.min(this.paginaAtual(), this.totalPaginas());
    const inicio = (pag - 1) * tam;
    return this.pessoasFiltradas().slice(inicio, inicio + tam);
  });

  readonly indiceInicial = computed(() => {
    if (this.pessoasFiltradas().length === 0) return 0;
    return (Math.min(this.paginaAtual(), this.totalPaginas()) - 1) * this.itensPorPagina() + 1;
  });

  readonly indiceFinal = computed(() => {
    return Math.min(this.pessoasFiltradas().length, this.indiceInicial() + this.pessoasPaginadas().length - 1);
  });

  readonly paginasArray = computed(() => {
    return Array.from({ length: this.totalPaginas() }, (_, i) => i + 1);
  });

  readonly totalComCpf = computed(() => {
    return this.pessoas().filter(p => !!p.cpf).length;
  });

  readonly totalComContato = computed(() => {
    return this.pessoas().filter(p => !!(p.celular || p.telefone || (p.telefones && p.telefones.length > 0))).length;
  });

  ngOnInit(): void {
    this.carregarPessoas();
  }

  carregarPessoas(): void {
    this.service.getPessoas().subscribe({
      next: (dados) => this.pessoas.set(dados),
      error: (e) => console.warn('Erro ao carregar pessoas:', e)
    });
  }

  aoMudarBusca(valor: string): void {
    this.busca.set(valor);
    this.paginaAtual.set(1);
  }

  aoMudarFiltroCadastro(valor: string): void {
    this.filtroCadastro.set(valor);
    this.paginaAtual.set(1);
  }

  limparFiltros(): void {
    this.busca.set('');
    this.filtroCadastro.set('TODOS');
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

  // ============================================================================
  // FORMATAÇÃO E MANIPULAÇÃO DE CONTATOS (TELEFONES) - NOVO CADASTRO
  // ============================================================================

  aoDigitarCpfNovo(valor: string): void {
    this.novoCpf = formatarCpf(valor);
  }

  aoDigitarTelefoneNovo(index: number, valor: string): void {
    const lista = [...this.telefonesNovo()];
    lista[index].numero = formatarTelefone(valor);
    this.telefonesNovo.set(lista);
  }

  adicionarTelefoneNovo(): void {
    const lista = this.telefonesNovo();
    if (lista.length >= 3) return;
    const tiposUsados = lista.map(t => t.tipo);
    const tiposDisponiveis: Array<'celular' | 'residencial' | 'comercial'> = ['celular', 'residencial', 'comercial'];
    const proximoTipo = tiposDisponiveis.find(t => !tiposUsados.includes(t)) || 'celular';
    const temPrincipal = lista.some(t => t.principal);
    this.telefonesNovo.set([
      ...lista,
      { numero: '', tipo: proximoTipo, principal: !temPrincipal, whatsapp: false }
    ]);
  }

  removerTelefoneNovo(index: number): void {
    const lista = this.telefonesNovo().filter((_, i) => i !== index);
    if (lista.length > 0 && !lista.some(t => t.principal)) {
      lista[0].principal = true;
    }
    this.telefonesNovo.set(lista);
  }

  definirPrincipalNovo(index: number): void {
    const lista = this.telefonesNovo().map((item, i) => ({
      ...item,
      principal: i === index
    }));
    this.telefonesNovo.set(lista);
  }

  toggleWhatsappNovo(index: number): void {
    const lista = [...this.telefonesNovo()];
    lista[index].whatsapp = !lista[index].whatsapp;
    this.telefonesNovo.set(lista);
  }

  // ============================================================================
  // FORMATAÇÃO E MANIPULAÇÃO DE CONTATOS (TELEFONES) - EDIÇÃO
  // ============================================================================

  aoDigitarCpfEdicao(valor: string): void {
    this.editCpf = formatarCpf(valor);
  }

  aoDigitarTelefoneEdicao(index: number, valor: string): void {
    const lista = [...this.telefonesEdicao()];
    lista[index].numero = formatarTelefone(valor);
    this.telefonesEdicao.set(lista);
  }

  adicionarTelefoneEdicao(): void {
    const lista = this.telefonesEdicao();
    if (lista.length >= 3) return;
    const tiposUsados = lista.map(t => t.tipo);
    const tiposDisponiveis: Array<'celular' | 'residencial' | 'comercial'> = ['celular', 'residencial', 'comercial'];
    const proximoTipo = tiposDisponiveis.find(t => !tiposUsados.includes(t)) || 'celular';
    const temPrincipal = lista.some(t => t.principal);
    this.telefonesEdicao.set([
      ...lista,
      { numero: '', tipo: proximoTipo, principal: !temPrincipal, whatsapp: false }
    ]);
  }

  removerTelefoneEdicao(index: number): void {
    const lista = this.telefonesEdicao().filter((_, i) => i !== index);
    if (lista.length > 0 && !lista.some(t => t.principal)) {
      lista[0].principal = true;
    }
    this.telefonesEdicao.set(lista);
  }

  definirPrincipalEdicao(index: number): void {
    const lista = this.telefonesEdicao().map((item, i) => ({
      ...item,
      principal: i === index
    }));
    this.telefonesEdicao.set(lista);
  }

  toggleWhatsappEdicao(index: number): void {
    const lista = [...this.telefonesEdicao()];
    lista[index].whatsapp = !lista[index].whatsapp;
    this.telefonesEdicao.set(lista);
  }

  // ============================================================================
  // PERSISTÊNCIA & VALIDAÇÕES
  // ============================================================================

  salvarPessoa(): void {
    if (!this.novoNome.trim()) {
      this.errorMessage.set('Informe o nome completo da pessoa física.');
      return;
    }
    if (!this.novoEmail.trim()) {
      this.errorMessage.set('Informe o e-mail principal.');
      return;
    }
    if (!validarEmail(this.novoEmail)) {
      this.errorMessage.set('Informe um e-mail válido (exemplo: usuario@dominio.com).');
      return;
    }

    if (this.novoCpf.trim() && !validarCpf(this.novoCpf)) {
      this.errorMessage.set('CPF inválido. Verifique os dígitos informados.');
      return;
    }

    // Validações de Telefones
    const fonesPreenchidos = this.telefonesNovo().filter(t => t.numero.trim() !== '');
    const tipos = fonesPreenchidos.map(t => t.tipo);
    if (new Set(tipos).size !== tipos.length) {
      this.errorMessage.set('Permitido cadastrar somente um telefone por tipo (celular, residencial, comercial).');
      return;
    }

    for (const f of fonesPreenchidos) {
      if (!validarTelefone(f.numero, f.tipo)) {
        this.errorMessage.set(`Número de telefone ${f.tipo} inválido. Informe o DDD e os dígitos corretos.`);
        return;
      }
    }

    if (fonesPreenchidos.length > 0 && !fonesPreenchidos.some(t => t.principal)) {
      fonesPreenchidos[0].principal = true;
    }

    this.salvando.set(true);
    this.errorMessage.set('');

    const principalPhone = fonesPreenchidos.find(t => t.principal) || fonesPreenchidos[0];
    const payload = {
      nome: this.novoNome.trim(),
      email: this.novoEmail.trim(),
      celular: principalPhone ? principalPhone.numero.trim() : undefined,
      cpf: this.novoCpf.trim() ? this.novoCpf.replace(/\D/g, '') : undefined,
      telefones: fonesPreenchidos.map(t => ({
        numero: t.numero.trim(),
        tipo: t.tipo,
        principal: t.principal,
        whatsapp: t.whatsapp
      }))
    };

    this.service.createPessoa(payload).subscribe({
      next: (nova) => {
        this.salvando.set(false);
        this.pessoas.update(lista => [nova, ...lista]);
        this.mostrarForm.set(false);
        this.novoNome = '';
        this.novoEmail = '';
        this.novoCpf = '';
        this.telefonesNovo.set([
          { numero: '', tipo: 'celular', principal: true, whatsapp: true }
        ]);
        this.mostrarToast('Pessoa física cadastrada com sucesso!');
        this.carregarPessoas();
      },
      error: (err) => {
        this.salvando.set(false);
        this.errorMessage.set(formatarMensagemErro(err, 'Erro ao cadastrar pessoa física.'));
      }
    });
  }

  iniciarEdicao(p: Pessoa): void {
    this.pessoaEmEdicao.set(p);
    this.editNome = p.nome_completo || p.nomeCompleto || p.nome || '';
    this.editEmail = p.email || '';
    this.editCpf = formatarCpf(p.cpf || '');
    this.erroEdicao.set('');

    // Preenche lista de telefones a partir do modelo
    const fones: TelefoneModel[] = Array.isArray(p.telefones) && p.telefones.length > 0
      ? p.telefones.map(t => ({
          numero: formatarTelefone(t.numero),
          tipo: t.tipo || 'celular',
          principal: Boolean(t.principal),
          whatsapp: Boolean(t.whatsapp)
        }))
      : (p.celular || p.telefone)
        ? [{
            numero: formatarTelefone(p.celular || p.telefone || ''),
            tipo: 'celular' as const,
            principal: true,
            whatsapp: true
          }]
        : [{
            numero: '',
            tipo: 'celular' as const,
            principal: true,
            whatsapp: true
          }];

    this.telefonesEdicao.set(fones);
  }

  cancelarEdicao(): void {
    this.pessoaEmEdicao.set(null);
    this.erroEdicao.set('');
  }

  salvarEdicao(): void {
    const pessoa = this.pessoaEmEdicao();
    if (!pessoa) return;

    if (!this.editEmail.trim()) {
      this.erroEdicao.set('Informe o e-mail de contato.');
      return;
    }
    if (!validarEmail(this.editEmail)) {
      this.erroEdicao.set('Informe um e-mail válido (exemplo: usuario@dominio.com).');
      return;
    }

    if (this.sessionService.podeEditarDadosCivis() && !this.editNome.trim()) {
      this.erroEdicao.set('Nome completo é obrigatório.');
      return;
    }

    if (this.editCpf.trim() && !validarCpf(this.editCpf)) {
      this.erroEdicao.set('CPF inválido. Verifique os dígitos informados.');
      return;
    }

    // Validações de telefones
    const fonesPreenchidos = this.telefonesEdicao().filter(t => t.numero.trim() !== '');
    const tipos = fonesPreenchidos.map(t => t.tipo);
    if (new Set(tipos).size !== tipos.length) {
      this.erroEdicao.set('Permitido cadastrar somente um telefone por tipo (celular, residencial, comercial).');
      return;
    }

    for (const f of fonesPreenchidos) {
      if (!validarTelefone(f.numero, f.tipo)) {
        this.erroEdicao.set(`Número de telefone ${f.tipo} inválido. Informe o DDD e os dígitos corretos.`);
        return;
      }
    }

    if (fonesPreenchidos.length > 0 && !fonesPreenchidos.some(t => t.principal)) {
      fonesPreenchidos[0].principal = true;
    }

    this.salvandoEdicao.set(true);
    this.erroEdicao.set('');

    const principalPhone = fonesPreenchidos.find(t => t.principal) || fonesPreenchidos[0];
    const payload: PessoaUpdate = {
      email: this.editEmail.trim(),
      celular: principalPhone ? principalPhone.numero.trim() : undefined,
      telefones: fonesPreenchidos.map(t => ({
        numero: t.numero.trim(),
        tipo: t.tipo,
        principal: t.principal,
        whatsapp: t.whatsapp
      }))
    };

    if (this.sessionService.podeEditarDadosCivis()) {
      payload.nome = this.editNome.trim();
      payload.nome_completo = this.editNome.trim();
      payload.cpf = this.editCpf.trim() ? this.editCpf.replace(/\D/g, '') : undefined;
    }

    this.service.updatePessoa(pessoa.id, payload).subscribe({
      next: (atualizada) => {
        this.salvandoEdicao.set(false);
        this.pessoas.update(lista =>
          lista.map(item => (item.id === pessoa.id ? { ...item, ...atualizada } : item))
        );
        this.pessoaEmEdicao.set(null);
        this.mostrarToast('Registro civil atualizado com sucesso!');
        this.carregarPessoas();
      },
      error: (err) => {
        this.salvandoEdicao.set(false);
        this.erroEdicao.set(formatarMensagemErro(err, 'Erro ao atualizar dados da pessoa.'));
      }
    });
  }

  iniciarExclusao(p: Pessoa): void {
    this.pessoaEmExclusao.set(p);
    this.pessoaEmEdicao.set(null);
    this.erroExclusao.set('');
  }

  cancelarExclusao(): void {
    this.pessoaEmExclusao.set(null);
    this.erroExclusao.set('');
  }

  confirmarExclusao(): void {
    const p = this.pessoaEmExclusao();
    if (!p) return;

    this.excluindo.set(true);
    this.erroExclusao.set('');

    this.service.deletePessoa(p.id).subscribe({
      next: () => {
        this.excluindo.set(false);
        this.pessoas.update(lista => lista.filter(item => item.id !== p.id));
        this.pessoaEmExclusao.set(null);
        this.mostrarToast('Pessoa física excluída com sucesso!');
      },
      error: (err) => {
        this.excluindo.set(false);
        this.pessoaEmExclusao.set(null);
        this.mostrarToast(formatarMensagemErro(err, 'Erro ao excluir pessoa física.'), 'erro');
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
