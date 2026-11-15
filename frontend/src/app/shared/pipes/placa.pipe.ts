import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'placa',
  standalone: true
})
export class PlacaPipe implements PipeTransform {
  transform(value: string | null | undefined): string {
    if (!value) return '';

    const clean = value.toUpperCase().replace(/[^A-Z0-9]/g, '');

    // Formato antigo: ABC1234 -> ABC-1234
    if (/^[A-Z]{3}[0-9]{4}$/.test(clean)) {
      return `${clean.substring(0, 3)}-${clean.substring(3)}`;
    }

    // Formato Mercosul: ABC1D23 -> ABC-1D23
    if (/^[A-Z]{3}[0-9][A-Z][0-9]{2}$/.test(clean)) {
      return `${clean.substring(0, 3)}-${clean.substring(3)}`;
    }

    return clean;
  }
}
