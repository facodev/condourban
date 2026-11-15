import { Injectable, inject, signal } from '@angular/core';
import { SwUpdate, VersionReadyEvent } from '@angular/service-worker';
import { filter } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PwaSyncService {
  private readonly swUpdate = inject(SwUpdate, { optional: true });

  readonly updateAvailable = signal<boolean>(false);
  readonly isOnline = signal<boolean>(navigator.onLine);

  constructor() {
    this.initConnectivityListeners();
    this.initUpdateListeners();
  }

  private initConnectivityListeners(): void {
    window.addEventListener('online', () => this.isOnline.set(true));
    window.addEventListener('offline', () => this.isOnline.set(false));
  }

  private initUpdateListeners(): void {
    if (!this.swUpdate?.isEnabled) return;

    this.swUpdate.versionUpdates
      .pipe(filter((evt): evt is VersionReadyEvent => evt.type === 'VERSION_READY'))
      .subscribe(() => {
        this.updateAvailable.set(true);
      });
  }

  activateUpdate(): void {
    if (!this.swUpdate) return;
    this.swUpdate.activateUpdate().then(() => document.location.reload());
  }
}