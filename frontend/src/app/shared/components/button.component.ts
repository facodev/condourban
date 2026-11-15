import { Component, ViewEncapsulation, input } from '@angular/core';
import { MatRipple } from '@angular/material/core';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MatRipple],
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ButtonComponent {
  variant = input<'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'>('primary');
  size = input<'md' | 'sm'>('md');
  type = input<'button' | 'submit' | 'reset'>('button');
  disabled = input<boolean>(false);
}
