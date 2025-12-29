import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileService } from '../../services/file.service';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.css'
})
export class FileUploadComponent {
  isUploading = signal(false);
  uploadStatus = signal<string>('');
  imagePreviewUrl: string = "image-default.png";

  constructor(private fileService: FileService) {}

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    if (input.files && input.files[0]) {
      const file = input.files[0];
      this.imagePreviewUrl = URL.createObjectURL(file);
    }

    const file = input.files[0];
    this.isUploading.set(true);
    this.uploadStatus.set(`Enviando ${file.name}...`);

    try {
      const result = await this.fileService.uploadFile(file);
      this.uploadStatus.set(`✅ Sucesso! Imagem enviada: ${result.filename}`);

      this.fileService.watchStatus(result.file_id).subscribe({
        next: (message) => {
          this.processWebSocketMessage(message);
          // console.log('WebSocket: Status:', message);
        },
        complete: () => {
          // console.log('WebSocket: Processo concluído.');
        },
        error: (err) => {
          // console.error('WebSocket: Erro: ', err);
        }
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      this.uploadStatus.set('❌ Erro ao enviar imagem: ' + msg);
    } finally {
      this.isUploading.set(false);
      input.value = '';
    }
  }

  private processWebSocketMessage(message: any) {
    if (!message.final) {
      this.uploadStatus.set('⏳ Processando imagem...');
    } else if (message.code === 200) {
      if (message.result && message.result.length > 0) {
        const total = message.result.length;
        const semEpi = message.result.filter((p: any) => !p.complete).length;
        this.uploadStatus.set(`✅ Processamento concluído! ${total} pessoa(s) detectada(s), ${(semEpi === 0 ? 'nenhuma' : semEpi)} sem EPI.`);
      } else {
        this.uploadStatus.set('✅ Processamento concluído! Nenhuma pessoa detectada.');
      }
    } else {
      this.uploadStatus.set('⚠️ Erro ou status desconhecido.');
    }
  }

}
