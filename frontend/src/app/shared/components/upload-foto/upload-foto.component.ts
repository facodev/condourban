import { Component, ViewEncapsulation, input, output, signal } from '@angular/core';

@Component({
  selector: 'app-upload-foto',
  standalone: true,
  templateUrl: './upload-foto.component.html',
  styleUrls: ['./upload-foto.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class UploadFotoComponent {
  readonly label = input<string>('Capturar ou Anexar Foto');
  readonly currentUrl = input<string | null>(null);

  readonly photoSelected = output<File>();
  readonly photoCleared = output<void>();

  readonly previewUrl = signal<string | null>(null);

  onFileSelected(event: Event): void {
    const inputEl = event.target as HTMLInputElement;
    if (inputEl.files && inputEl.files.length > 0) {
      const file = inputEl.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.previewUrl.set(reader.result as string);
        this.photoSelected.emit(file);
      };
      reader.readAsDataURL(file);
    }
  }

  clearPhoto(): void {
    this.previewUrl.set(null);
    this.photoCleared.emit();
  }
}
