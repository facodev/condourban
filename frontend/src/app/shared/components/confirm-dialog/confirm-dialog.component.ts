import { Component, ViewEncapsulation, input, output } from '@angular/core';
import { MatRipple } from '@angular/material/core';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [MatRipple],
  templateUrl: './confirm-dialog.component.html',
  styleUrls: ['./confirm-dialog.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ConfirmDialogComponent {
  readonly isOpen = input<boolean>(false);
  readonly title = input<string>('Confirmar exclusão');
  readonly message = input<string>('Tem certeza de que deseja excluir este registro? Esta ação é irreversível.');
  readonly confirmText = input<string>('Excluir');
  readonly cancelText = input<string>('Cancelar');
  readonly isDestructive = input<boolean>(true);

  readonly confirmed = output<void>();
  readonly cancelled = output<void>();

  onConfirm(): void {
    this.confirmed.emit();
  }

  onCancel(): void {
    this.cancelled.emit();
  }
}
