import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommentAnalyzerComponent } from './components/comment-analyzer/comment-analyzer.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    CommonModule,
    CommentAnalyzerComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'youtube-comment-analyzer';
}
