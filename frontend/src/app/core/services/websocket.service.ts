import { Injectable, signal } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket | null = null;
  private readonly messages$ = new Subject<any>();

  readonly isConnected = signal<boolean>(false);

  connect(url: string): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) return;

    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      this.isConnected.set(true);
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.messages$.next(data);
      } catch {
        this.messages$.next(event.data);
      }
    };

    this.socket.onclose = () => {
      this.isConnected.set(false);
    };

    this.socket.onerror = () => {
      this.isConnected.set(false);
    };
  }

  send(data: any): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(typeof data === 'string' ? data : JSON.stringify(data));
    }
  }

  getMessages(): Observable<any> {
    return this.messages$.asObservable();
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}