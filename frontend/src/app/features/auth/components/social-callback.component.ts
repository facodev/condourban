import { Component, OnInit, inject, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-social-callback',
  templateUrl: './social-callback.component.html',
  styleUrls: ['./social-callback.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class SocialCallbackComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  ngOnInit(): void {
    const token = this.route.snapshot.queryParamMap.get('token');
    if (token) {
      localStorage.setItem('condourban_token', token);
      this.router.navigate(['/condominio']);
    } else {
      this.router.navigate(['/auth/login']);
    }
  }
}