import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ItemMuralSocial } from '../../services/comunicacao.service';

@Component({
  selector: 'app-mural-social',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mural-social.component.html',
  styleUrls: ['./mural-social.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class MuralSocialComponent {
  readonly itens = signal<ItemMuralSocial[]>([
    {
      id: 1,
      tipo: 'enquete',
      titulo: 'Instalação de Mini Mercado no Bloco B',
      descricao: 'Você aprova a instalação de uma conveniência autônoma no subsolo do Bloco B?',
      autorNome: 'Comissão de Moradores',
      publicadoEm: '16/10/2026'
    },
    {
      id: 2,
      tipo: 'achado_perdido',
      titulo: 'Chaveiro encontrado próximo à piscina',
      descricao: 'Chave com chaveiro vermelho e símbolo de carro deixado no banco da área externa.',
      autorNome: 'Portaria Principal',
      publicadoEm: '17/10/2026'
    }
  ]);

  formatTipo(tipo: string): string {
    switch (tipo) {
      case 'enquete': return '🗳️ ENQUETE';
      case 'achado_perdido': return '🔍 ACHADOS E PERDIDOS';
      case 'classificado': return '🏷️ CLASSIFICADOS';
      default: return tipo.toUpperCase();
    }
  }
}
