import { Injectable, inject, signal } from '@angular/core';
import { SwPush } from '@angular/service-worker';

export interface AppNotification {
  id: string;
  title: string;
  body: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: Date;
  read: boolean;
  link?: string;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private readonly swPush = inject(SwPush, { optional: true });

  readonly permissionStatus = signal<NotificationPermission>(
    typeof Notification !== 'undefined' ? Notification.permission : 'default'
  );
  readonly notifications = signal<AppNotification[]>([]);
  readonly unreadCount = signal<number>(0);

  constructor() {
    this.listenToPushMessages();
  }

  async requestPermission(): Promise<NotificationPermission> {
    if (typeof Notification === 'undefined') return 'denied';
    const permission = await Notification.requestPermission();
    this.permissionStatus.set(permission);
    return permission;
  }

  async subscribeToPush(serverPublicKey: string): Promise<PushSubscription | null> {
    if (!this.swPush?.isEnabled) return null;

    try {
      const subscription = await this.swPush.requestSubscription({
        serverPublicKey
      });
      return subscription;
    } catch (err) {
      console.error('Falha ao subscrever push notifications:', err);
      return null;
    }
  }

  addNotification(notification: Omit<AppNotification, 'id' | 'timestamp' | 'read'>): void {
    const item: AppNotification = {
      ...notification,
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      timestamp: new Date(),
      read: false
    };

    this.notifications.update(list => [item, ...list]);
    this.unreadCount.update(count => count + 1);
  }

  markAsRead(id: string): void {
    this.notifications.update(list =>
      list.map(n => (n.id === id ? { ...n, read: true } : n))
    );
    this.unreadCount.update(count => Math.max(0, count - 1));
  }

  clearAll(): void {
    this.notifications.set([]);
    this.unreadCount.set(0);
  }

  private listenToPushMessages(): void {
    if (!this.swPush?.isEnabled) return;

    this.swPush.messages.subscribe(msg => {
      const payload = msg as { title?: string; body?: string; link?: string };
      this.addNotification({
        title: payload.title || 'Nova Notificação',
        body: payload.body || '',
        type: 'info',
        link: payload.link
      });
    });
  }
}
