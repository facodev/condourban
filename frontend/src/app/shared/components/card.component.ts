import { Component, ViewEncapsulation, input } from '@angular/core';

@Component({
  selector: 'app-card',
  standalone: true,
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class CardComponent {
  title = input<string>('');
  subtitle = input<string>('');
  hoverable = input<boolean>(false);
}
