import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  constructor() {}

  async uploadFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    let response: Response;
    try {
      response = await fetch(`${environment.apiUrl}/upload`, {
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
}