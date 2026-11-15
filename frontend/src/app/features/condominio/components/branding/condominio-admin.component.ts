import { Component, OnInit, inject, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { BrandingService } from '../../services/branding.service';
import { SessionService } from '../../../../core/services/session.service';
import { Condominio } from '../../models/condominio.model';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-condominio-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, ButtonComponent, ConfirmDialogComponent],
  templateUrl: './condominio-admin.component.html',
  styleUrls: ['./condominio-admin.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class CondominioAdminComponent implements OnInit {
  private readonly service = inject(BrandingService);
  private readonly sessionService = inject(SessionService);

  condominios = signal<Condominio[]>([]);
  condominioAtivo = signal<Condominio | null>(null);
  isLoading = signal<boolean>(true);
  salvando = signal<boolean>(false);

  mostrarFormNovoCondominio = signal<boolean>(false);
  novoCondoForm = {
    nome: '',
    razao_social: '',
    cnpj: '',
    cidade: '',
    uf: '',
    cep: ''
  };

  ativoEditForm: Partial<Condominio> = {
    nome: '',
    razaoSocial: '',
    cnpj: '',
    logradouro: '',
    numero: '',
    bairro: '',
    cidade: '',
    uf: '',
    cep: ''
  };

  condominioParaExcluir = signal<Condominio | null>(null);

  toastMensagem = signal<string>('');
  toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    this.isLoading.set(true);
    this.service.getTodosCondominios().subscribe({
      next: (lista) => {
        this.condominios.set(lista);
        const ativoId = this.sessionService.condominioAtivoId() || (lista.length > 0 ? lista[0].id : undefined);
        this.service.getInfo(ativoId || undefined).subscribe({
          next: (ativo) => {
            this.condominioAtivo.set(ativo);
            this.ativoEditForm = {
              ...ativo,
              razaoSocial: ativo.razaoSocial || (ativo as any).razao_social || '',
              razao_social: (ativo as any).razao_social || ativo.razaoSocial || '',
            };
            this.isLoading.set(false);
          },
          error: () => this.isLoading.set(false)
        });
      },
      error: (err) => {
        this.isLoading.set(false);
        this.mostrarToast('Erro ao carregar condomínios: ' + (err?.error?.detail || err.message), 'erro');
      }
    });
  }

  isCondominioAtivo(id: string): boolean {
    const atual = this.sessionService.condominioAtivoId() || this.condominioAtivo()?.id;
    return atual === id;
  }

  getCondominioAtivoNome(): string {
    const atualId = this.sessionService.condominioAtivoId() || this.condominioAtivo()?.id;
    const condo = this.condominios().find(c => c.id === atualId);
    return condo ? condo.nome : (this.condominioAtivo()?.nome || 'Condomínio Principal');
  }

  alternarCondominioAtivo(c: Condominio): void {
    this.sessionService.setCondominio({ id: c.id, nome: c.nome });
    this.condominioAtivo.set(c);
    this.ativoEditForm = {
      ...c,
      razaoSocial: c.razaoSocial || (c as any).razao_social || '',
      razao_social: (c as any).razao_social || c.razaoSocial || '',
    };
    this.mostrarToast(`Condomínio alterado para "${c.nome}". As operações agora operam sob esta instância.`);
  }

  salvarNovoCondominio(): void {
    if (!this.novoCondoForm.nome.trim()) return;

    this.salvando.set(true);
    this.service.createCondominio({
      nome: this.novoCondoForm.nome.trim(),
      razao_social: this.novoCondoForm.razao_social.trim() || undefined,
      cnpj: this.novoCondoForm.cnpj.trim() || undefined,
      cidade: this.novoCondoForm.cidade.trim() || undefined,
      uf: this.novoCondoForm.uf.trim().toUpperCase() || undefined,
      cep: this.novoCondoForm.cep.trim() || undefined
    }).subscribe({
      next: (criado) => {
        this.salvando.set(false);
        this.mostrarFormNovoCondominio.set(false);
        this.novoCondoForm = { nome: '', razao_social: '', cnpj: '', cidade: '', uf: '', cep: '' };
        this.sessionService.setCondominio({ id: criado.id, nome: criado.nome });
        this.mostrarToast(`Condomínio "${criado.nome}" criado com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao criar condomínio.', 'erro');
      }
    });
  }

  salvarDadosCadastrais(): void {
    const ativo = this.condominioAtivo();
    if (!ativo) return;

    this.salvando.set(true);
    const payload = {
      ...this.ativoEditForm,
      razao_social: this.ativoEditForm.razaoSocial || (this.ativoEditForm as any).razao_social,
      razaoSocial: this.ativoEditForm.razaoSocial || (this.ativoEditForm as any).razao_social,
    };
    this.service.updateInfo(payload, ativo.id).subscribe({
      next: (atualizado) => {
        this.salvando.set(false);
        this.condominioAtivo.set(atualizado);
        this.ativoEditForm = {
          ...atualizado,
          razaoSocial: atualizado.razaoSocial || (atualizado as any).razao_social || '',
          razao_social: (atualizado as any).razao_social || atualizado.razaoSocial || '',
        };
        this.sessionService.setCondominio({ id: atualizado.id, nome: atualizado.nome });
        this.mostrarToast('Dados cadastrais e institucionais atualizados com sucesso!');
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao atualizar dados cadastrais.', 'erro');
      }
    });
  }

  confirmarExclusaoCondominio(c: Condominio): void {
    this.condominioParaExcluir.set(c);
  }

  executarExclusaoCondominio(): void {
    const c = this.condominioParaExcluir();
    if (!c) return;

    this.salvando.set(true);
    this.service.deleteCondominio(c.id).subscribe({
      next: () => {
        this.salvando.set(false);
        this.condominioParaExcluir.set(null);
        this.mostrarToast(`Condomínio "${c.nome}" excluído com sucesso!`);
        this.carregarDados();
      },
      error: (err) => {
        this.salvando.set(false);
        this.mostrarToast(err?.error?.detail || 'Erro ao excluir condomínio.', 'erro');
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
