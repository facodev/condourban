import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'cu-root',
  imports: [RouterOutlet],
  template: `<router-outlet />`,
})
export class App {}
