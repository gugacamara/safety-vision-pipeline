import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private apiUrl: string;
  private wsUrl: string;

  constructor() {
    const { apiProtocol, apiHost, apiPort } = environment;
    this.apiUrl = `${apiProtocol}://${apiHost}${apiPort && apiPort !== 80 && apiPort !== 443 ? ':' + apiPort : ''}`;
    const wsProtocol = apiProtocol === 'https' ? 'wss' : 'ws';
    this.wsUrl = `${wsProtocol}://${apiHost}${apiPort && apiPort !== 80 && apiPort !== 443 ? ':' + apiPort : ''}`;
  }

  /**
   * Faz upload de um arquivo para o servidor.
   * @param file 
   * @returns 
   */
  async uploadFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    let response: Response;
    try {
      response = await fetch(`${this.apiUrl}/upload`, {
        method: 'POST',
        body: formData
      });
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : String(error));
    }

    if (!response.ok) {
      throw new Error(response.statusText || 'Erro inesperado do servidor');
    }
    return await response.json();
  }

  /**
   * Abre um WebSocket para monitorar o status do processamento.
   * Retorna um Observable que emite os status recebidos.
   * @param fileId
   * @return Observable<any>
   */
  watchStatus(fileId: string): Observable<any> {
    return new Observable(observer => {
      const wsUrl = `${this.wsUrl}/ws/status/${fileId}`;
      const ws = new WebSocket(wsUrl);

      ws.onmessage = (event) => {
        try {
          const status = JSON.parse(event.data);
          observer.next(status);
          if (status.final) {
            ws.close();
            observer.complete();
          }
        } catch (e) {
          observer.error(e);
        }
      };

      ws.onerror = (event) => {
        observer.error(event);
      };

      ws.onclose = () => {
        observer.complete();
      };

      // Cleanup
      return () => {
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
      };
    });
  }
}