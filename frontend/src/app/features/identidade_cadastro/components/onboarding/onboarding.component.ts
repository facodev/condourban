import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { IdentidadeCadastroService, SolicitacaoOnboarding } from '../../services/identidade-cadastro.service';
import { CondominioService, Unidade } from '../../../condominio/services/condominio.service';
import { SessionService } from '../../../../core/services/session.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';
import { ButtonComponent } from '../../../../shared/components/button.component';

@Component({
  selector: 'app-onboarding',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RouterLinkActive, StatusBadgeComponent, ButtonComponent],
  templateUrl: './onboarding.component.html',
  styleUrls: ['./onboarding.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class OnboardingComponent implements OnInit {
  private readonly idService = inject(IdentidadeCadastroService);
  private readonly condService = inject(CondominioService);
  readonly sessionService = inject(SessionService);

  readonly solicitacoes = signal<SolicitacaoOnboarding[]>([]);
  readonly unidades = signal<Unidade[]>([]);
  readonly mostrarConvite = signal<boolean>(false);
  readonly enviandoConvite = signal<boolean>(false);
  readonly mensagemConvite = signal<string>('');
  readonly erroConvite = signal<string>('');

  conviteEmail = '';
  conviteUnidadeId = '';
  conviteTipo = 'MORADOR';

  readonly pendentesCount = computed(() => {
    return this.solicitacoes().filter(s => this.isPending(s.status)).length;
  });

  readonly aprovadasCount = computed(() => {
    return this.solicitacoes().filter(s => {
      const st = (s.status || '').toUpperCase();
      return st === 'APROVADO' || st === 'APROVADA';
    }).length;
  });

  ngOnInit(): void {
    this.carregarSolicitacoes();
    this.condService.getUnits().subscribe({
      next: (dados) => this.unidades.set(dados),
      error: (e) => console.warn('Erro ao carregar unidades:', e)
    });
  }

  isPending(status: string): boolean {
    const s = (status || '').toUpperCase();
    return s === 'EM_ANALISE' || s === 'ENVIADA' || s === 'PENDENTE';
  }

  carregarSolicitacoes(): void {
    this.idService.getSolicitacoesOnboarding().subscribe({
      next: (dados) => this.solicitacoes.set(dados),
      error: (e) => console.warn('Erro ao carregar solicitações de onboarding:', e)
    });
  }

  enviarConvite(): void {
    if (!this.conviteEmail.trim() || !this.conviteUnidadeId) return;

    this.enviandoConvite.set(true);
    this.mensagemConvite.set('');
    this.erroConvite.set('');

    this.idService.criarConviteOnboarding({
      email: this.conviteEmail.trim(),
      unidade_id: this.conviteUnidadeId,
      tipo_ocupacao: this.conviteTipo
    }).subscribe({
      next: (res: any) => {
        this.enviandoConvite.set(false);
        this.mensagemConvite.set(`Convite gerado com sucesso! Token: ${res?.token || 'Ativo por 7 dias'}.`);
        this.conviteEmail = '';
      },
      error: (err: any) => {
        this.enviandoConvite.set(false);
        this.erroConvite.set(err?.error?.detail || 'Erro ao gerar convite.');
      }
    });
  }

  aprovar(id: string): void {
    this.idService.aprovarSolicitacao(id).subscribe({
      next: () => {
        this.solicitacoes.update(lista =>
          lista.map(item => item.id === id ? { ...item, status: 'aprovado' } : item)
        );
      },
      error: (err: any) => console.error('Erro ao aprovar solicitação:', err)
    });
  }

  rejeitar(id: string): void {
    const motivo = prompt('Informe o motivo da rejeição do cadastro:');
    if (!motivo) return;

    this.idService.rejeitarSolicitacao(id, motivo).subscribe({
      next: () => {
        this.solicitacoes.update(lista =>
          lista.map(item => item.id === id ? { ...item, status: 'rejeitado' } : item)
        );
      },
      error: (err: any) => console.error('Erro ao rejeitar solicitação:', err)
    });
  }
}
