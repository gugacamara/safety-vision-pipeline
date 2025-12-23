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

  constructor(private fileService: FileService) {}

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    this.isUploading.set(true);
    this.uploadStatus.set(`Enviando ${file.name}...`);

    try {
      const result = await this.fileService.uploadFile(file);
      this.uploadStatus.set(`✅ Sucesso! Imagem enviada: ${result}`);
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      this.uploadStatus.set('❌ Erro ao enviar imagem: ' + msg);
      //console.error(error);
    } finally {
      this.isUploading.set(false);
      input.value = '';
    }
  }
}
