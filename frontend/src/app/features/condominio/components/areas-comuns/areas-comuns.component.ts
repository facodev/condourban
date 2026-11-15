import { Component, OnInit, inject, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CondominioService, AreaComum } from '../../services/condominio.service';
import { SessionService } from '../../../../core/services/session.service';
import { MoedaPipe } from '../../../../shared/pipes/moeda.pipe';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';
import { ButtonComponent } from '../../../../shared/components/button.component';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';

export interface RegraDiaItem {
  aberto: boolean;
  horario_abertura: string;
  horario_fechamento: string;
  valor: number | null;
}

@Component({
  selector: 'app-areas-comuns',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, MoedaPipe, StatusBadgeComponent, ButtonComponent, ConfirmDialogComponent],
  templateUrl: './areas-comuns.component.html',
  styleUrls: ['./areas-comuns.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class AreasComunsComponent implements OnInit {
  private readonly service = inject(CondominioService);
  readonly sessionService = inject(SessionService);

  readonly areas = signal<AreaComum[]>([]);
  readonly mostrarForm = signal<boolean>(false);
  readonly areaEmEdicao = signal<AreaComum | null>(null);
  readonly areaParaExcluir = signal<AreaComum | null>(null);
  readonly salvando = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  toastMensagem = signal<string>('');
  toastTipo = signal<'sucesso' | 'erro'>('sucesso');

  readonly DIAS_SEMANA = [
    { key: 'seg', label: 'Segunda-feira', abrev: 'Seg' },
    { key: 'ter', label: 'Terça-feira', abrev: 'Ter' },
    { key: 'qua', label: 'Quarta-feira', abrev: 'Qua' },
    { key: 'qui', label: 'Quinta-feira', abrev: 'Qui' },
    { key: 'sex', label: 'Sexta-feira', abrev: 'Sex' },
    { key: 'sab', label: 'Sábado', abrev: 'Sáb' },
    { key: 'dom', label: 'Domingo', abrev: 'Dom' },
  ];

  formModel: {
    nome: string;
    descricao: string;
    capacidade: number;
    taxa_reserva: number;
    horario_abertura: string;
    horario_fechamento: string;
    requer_aprovacao: boolean;
    regras_dias: Record<string, RegraDiaItem>;
  } = this.gerarFormModelPadrao();

  readonly capacidadeTotal = computed(() => {
    return this.areas().reduce((acc, curr) => acc + (Number(curr.capacidade) || 0), 0);
  });

  readonly espacosDisponiveis = computed(() => {
    return this.areas().filter(a => (a.status === 'ATIVO' || a.status === 'disponivel') && a.ativo !== false).length;
  });

  ngOnInit(): void {
    this.carregarAreas();
  }

  gerarFormModelPadrao() {
    const regras: Record<string, RegraDiaItem> = {};
    for (const d of this.DIAS_SEMANA) {
      regras[d.key] = {
        aberto: true,
        horario_abertura: '08:00',
        horario_fechamento: '22:00',
        valor: null
      };
    }
    return {
      nome: '',
      descricao: '',
      capacidade: 20,
      taxa_reserva: 0,
      horario_abertura: '08:00',
      horario_fechamento: '22:00',
      requer_aprovacao: false,
      regras_dias: regras
    };
  }

  carregarAreas(): void {
    const cid = this.sessionService.condominioAtivoId() || undefined;
    this.service.getAreasComuns(cid).subscribe({
      next: (dados) => this.areas.set(dados),
      error: (e) => {
        console.warn('Erro ao carregar áreas comuns:', e);
        this.mostrarToast('Erro ao carregar áreas comuns: ' + (e?.error?.detail || e.message), 'erro');
      }
    });
  }

  abrirCriacao(): void {
    this.areaEmEdicao.set(null);
    this.formModel = this.gerarFormModelPadrao();
    this.errorMessage.set('');
    this.mostrarForm.set(true);
  }

  abrirEdicao(area: AreaComum): void {
    this.areaEmEdicao.set(area);
    const regrasSalvas = area.regras_dias || area.regrasDias || {};

    const regras: Record<string, RegraDiaItem> = {};
    for (const d of this.DIAS_SEMANA) {
      const salva = regrasSalvas[d.key] || {};
      regras[d.key] = {
        aberto: salva.aberto !== undefined ? !!salva.aberto : true,
        horario_abertura: salva.horario_abertura || area.horarioAbertura || '08:00',
        horario_fechamento: salva.horario_fechamento || area.horarioFechamento || '22:00',
        valor: salva.valor !== undefined && salva.valor !== null ? Number(salva.valor) : null
      };
    }

    this.formModel = {
      nome: area.nome || '',
      descricao: area.descricao || '',
      capacidade: Number(area.capacidade) || 20,
      taxa_reserva: Number(area.taxaReserva || area.valorReserva || 0),
      horario_abertura: area.horarioAbertura || '08:00',
      horario_fechamento: area.horarioFechamento || '22:00',
      requer_aprovacao: !!area.requerAprovacao,
      regras_dias: regras
    };

    this.errorMessage.set('');
    this.mostrarForm.set(true);
  }

  fecharForm(): void {
    this.mostrarForm.set(false);
    this.areaEmEdicao.set(null);
  }

  salvarArea(): void {
    if (!this.formModel.nome.trim() || !this.formModel.capacidade) return;

    this.salvando.set(true);
    this.errorMessage.set('');

    const areaEditando = this.areaEmEdicao();

    if (areaEditando) {
      // Atualização
      const payload: Partial<AreaComum> = {
        nome: this.formModel.nome.trim(),
        descricao: this.formModel.descricao?.trim() || undefined,
        capacidade: Number(this.formModel.capacidade),
        taxaReserva: Number(this.formModel.taxa_reserva) || 0,
        horarioAbertura: this.formModel.horario_abertura || undefined,
        horarioFechamento: this.formModel.horario_fechamento || undefined,
        requerAprovacao: this.formModel.requer_aprovacao,
        regras_dias: this.formModel.regras_dias
      };

      this.service.updateAreaComum(areaEditando.id, payload).subscribe({
        next: (atualizada) => {
          this.salvando.set(false);
          this.mostrarToast(`Espaço "${atualizada.nome}" atualizado com sucesso!`);
          this.fecharForm();
          this.carregarAreas();
        },
        error: (err) => {
          this.salvando.set(false);
          this.errorMessage.set(err?.error?.detail || 'Erro ao atualizar espaço comum.');
        }
      });
    } else {
      // Criação
      const payload = {
        nome: this.formModel.nome.trim(),
        descricao: this.formModel.descricao?.trim() || undefined,
        capacidade: Number(this.formModel.capacidade),
        taxa_reserva: Number(this.formModel.taxa_reserva) || 0,
        horario_abertura: this.formModel.horario_abertura || undefined,
        horario_fechamento: this.formModel.horario_fechamento || undefined,
        requer_aprovacao: this.formModel.requer_aprovacao,
        regras_dias: this.formModel.regras_dias,
        condominio_id: this.sessionService.condominioAtivoId() || undefined
      };

      this.service.createAreaComum(payload).subscribe({
        next: (nova) => {
          this.salvando.set(false);
          this.mostrarToast(`Espaço "${nova.nome}" cadastrado com sucesso!`);
          this.fecharForm();
          this.carregarAreas();
        },
        error: (err) => {
          this.salvando.set(false);
          this.errorMessage.set(err?.error?.detail || 'Erro ao cadastrar espaço comum.');
        }
      });
    }
  }

  toggleAtivo(area: AreaComum): void {
    const isAtivo = (area.status === 'ATIVO' || area.status === 'disponivel') && area.ativo !== false;
    const novoStatus = isAtivo ? 'INATIVO' : 'ATIVO';

    this.service.updateAreaStatus(area.id, !isAtivo).subscribe({
      next: (atualizada: any) => {
        this.areas.update(lista =>
          lista.map(item => item.id === area.id ? { ...item, ativo: !isAtivo, status: atualizada?.status || novoStatus } : item)
        );
        this.mostrarToast(`Espaço "${area.nome}" ${isAtivo ? 'interditado' : 'liberado'} com sucesso.`);
      },
      error: (err: any) => {
        this.mostrarToast(err?.error?.detail || 'Erro ao atualizar status da área.', 'erro');
      }
    });
  }

  confirmarExclusao(area: AreaComum): void {
    this.areaParaExcluir.set(area);
  }

  executarExclusao(): void {
    const area = this.areaParaExcluir();
    if (!area) return;

    this.service.deleteAreaComum(area.id).subscribe({
      next: () => {
        this.areas.update(lista => lista.filter(item => item.id !== area.id));
        this.mostrarToast(`Espaço "${area.nome}" excluído com sucesso!`);
        this.areaParaExcluir.set(null);
      },
      error: (err: any) => {
        this.mostrarToast(err?.error?.detail || 'Erro ao excluir espaço comum.', 'erro');
        this.areaParaExcluir.set(null);
      }
    });
  }

  temRegrasPersonalizadas(area: AreaComum): boolean {
    const r = area.regras_dias || area.regrasDias;
    if (!r || typeof r !== 'object') return false;
    return Object.keys(r).length > 0;
  }

  getResumoDias(area: AreaComum): { key: string; label: string; aberto: boolean; resumo: string; detalhe: string }[] {
    const r = area.regras_dias || area.regrasDias || {};
    return this.DIAS_SEMANA.map(d => {
      const config = r[d.key];
      if (!config) {
        return { key: d.key, label: d.abrev, aberto: true, resumo: 'Padrão', detalhe: 'Horário padrão' };
      }
      if (!config.aberto) {
        return { key: d.key, label: d.abrev, aberto: false, resumo: 'Fechado', detalhe: `${d.label}: Não abre para reservas` };
      }
      const valorStr = config.valor !== null && config.valor !== undefined ? `R$ ${config.valor}` : '';
      const horasStr = (config.horario_abertura || config.horario_fechamento) ? `${config.horario_abertura || ''}-${config.horario_fechamento || ''}` : '';
      const resumo = valorStr || horasStr || 'Padrão';
      const detalhe = `${d.label}: ${horasStr ? horasStr + ' ' : ''}${valorStr ? '(' + valorStr + ')' : ''}`;
      return { key: d.key, label: d.abrev, aberto: true, resumo, detalhe };
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
