import { Component, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CredencialAcesso } from '../../services/controle-acesso.service';
import { StatusBadgeComponent } from '../../../../shared/components/status-badge/status-badge.component';

@Component({
  selector: 'app-credenciais',
  standalone: true,
  imports: [CommonModule, StatusBadgeComponent],
  templateUrl: './credenciais.component.html',
  styleUrls: ['./credenciais.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class CredenciaisComponent {
  readonly credenciais = signal<CredencialAcesso[]>([
    { id: '1', pessoaNome: 'Carlos Eduardo Silva', tipo: 'facial', codigoIdentificador: 'BIO-FACIAL-00192', status: 'ativo' },
    { id: '2', pessoaNome: 'Carlos Eduardo Silva', tipo: 'tag_rfid', codigoIdentificador: 'TAG-E280-1122', status: 'ativo' },
    { id: '3', pessoaNome: 'Mariana Costa Ferreira', tipo: 'facial', codigoIdentificador: 'BIO-FACIAL-00193', status: 'ativo' }
  ]);

  formatTipo(tipo: string): string {
    switch (tipo) {
      case 'facial': return 'Biometria Facial';
      case 'tag_rfid': return 'Tag RFID Veicular';
      case 'qr_code': return 'QR Code Temporário';
      default: return tipo;
    }
  }
}
