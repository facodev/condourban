import { Component, ViewEncapsulation, model, input } from '@angular/core';

@Component({
  selector: 'app-modal',
  standalone: true,
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ModalComponent {
  isOpen = model<boolean>(false);
  title = input<string>('');

  close(): void {
    this.isOpen.set(false);
  }
}
