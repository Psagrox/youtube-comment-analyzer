import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { YoutubeService } from '../../service/youtube.service';
import { ChartData, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';


@Component({
  selector: 'app-comment-analyzer',
  standalone: true,
  imports: [
    CommonModule,
    BaseChartDirective,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatNativeDateModule,
    MatSlideToggleModule,
  ],
  templateUrl: './comment-analyzer.component.html',
  styleUrls: ['./comment-analyzer.component.css']
})
export class CommentAnalyzerComponent {
  videoUrl: string = '';
  analysisResult: any = null;
  isLoading: boolean = false;
  wordcloudImage: any = null;

  // Datos y opciones del gráfico
  chartData: ChartData<'bar'> = {
    labels: [], // Etiquetas (comentarios)
    datasets: [
      {
        data: [], // Datos de polaridad
        label: 'Polarity',
        backgroundColor: 'rgba(41, 123, 255, 0.6)',
        borderColor: 'rgba(41, 123, 255, 1)',
        borderWidth: 1
      }
    ]
  };

  chartOptions: ChartOptions = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        type: 'linear'
      }
    }
  };

  constructor(private youtubeService: YoutubeService) { }

  analyzeComments() {
    if (this.videoUrl) {
      this.isLoading = true;
      this.youtubeService.analyzeComments(this.videoUrl).subscribe({
        next: (response) => {
          this.analysisResult = response;
          this.wordcloudImage = response.wordcloud;
          this.updateChartData(response);
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error analyzing comments:', error);
          this.isLoading = false;
        }
      });
    }
  }

  onInputChange(event: Event) {
    this.videoUrl = (event.target as HTMLInputElement).value;
  }

  // Función para actualizar los datos del gráfico
  updateChartData(response: any) {
    // Asegúrate de que la respuesta tenga el campo 'comments'
    const comments = Array.isArray(response.comments) ? response.comments : [];

    // Si no hay comentarios, no continúes
    if (comments.length === 0) {
      console.error('No comments found or invalid response format.');
      return;
    }

    // Actualiza los datos del gráfico
    this.chartData.labels = comments.map((comment: any) => comment.text);  // Usa el texto del comentario como etiqueta
    this.chartData.datasets[0].data = comments.map((comment: any) => comment.polarity); // Usa la polaridad como dato
  }
}
