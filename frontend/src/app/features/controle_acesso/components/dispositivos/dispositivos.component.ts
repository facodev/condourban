import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DispositivoAcesso } from '../../services/controle-acesso.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-dispositivos',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './dispositivos.component.html',
  styleUrls: ['./dispositivos.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class DispositivosComponent {
  readonly dispositivos = signal<DispositivoAcesso[]>([
    { id: '1', nome: 'Facial Portaria Social', tipo: 'leitor_facial', localizacao: 'Entrada Social', ip: '192.168.1.101', online: true, ultimoSync: 'Agora há pouco' },
    { id: '2', nome: 'Cancela Veicular Entrada', tipo: 'cancela', localizacao: 'Garagem Subsolo', ip: '192.168.1.102', online: true, ultimoSync: 'Há 5 min' },
    { id: '3', nome: 'Antena RFID Veicular', tipo: 'antena_rfid', localizacao: 'Acesso Principal Garagem', ip: '192.168.1.103', online: false, ultimoSync: 'Ontem às 22:00' }
  ]);

  getDeviceIcon(tipo: string): string {
    switch (tipo) {
      case 'leitor_facial': return '👤';
      case 'cancela': return '🚧';
      case 'antena_rfid': return '📡';
      default: return '📟';
    }
  }

  sincronizar(id: string): void {
    this.dispositivos.update(list =>
      list.map(d => (d.id === id ? { ...d, online: true, ultimoSync: 'Agora há pouco' } : d))
    );
  }
}
