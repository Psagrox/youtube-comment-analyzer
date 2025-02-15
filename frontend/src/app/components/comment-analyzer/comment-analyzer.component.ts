import { Component } from '@angular/core';
import { YoutubeService } from '../../service/youtube.service';
import { CommonModule } from '@angular/common'; // Para usar directivas como *ngIf
import { FormsModule } from '@angular/forms'; // Para usar [(ngModel)]
import { HttpClientModule } from '@angular/common/http'; // Para usar HttpClient

@Component({
  selector: 'app-comment-analyzer',
  standalone: true, // Marca el componente como independiente
  imports: [CommonModule, FormsModule, HttpClientModule], // Importa los módulos necesarios
  templateUrl: './comment-analyzer.component.html',
  styleUrls: ['./comment-analyzer.component.css'],
})
export class CommentAnalyzerComponent {
  videoUrl: string = '';
  analysisResult: any = null;

  constructor(private youtubeService: YoutubeService) { }

  analyzeComments() {
    this.youtubeService.analyzeComments(this.videoUrl).subscribe(
      (response) => {
        this.analysisResult = response;
      },
      (error) => {
        console.error('Error analyzing comments:', error);
      }
    );
  }
}
