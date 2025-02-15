import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CommentAnalyzerComponent } from './components/comment-analyzer/comment-analyzer.component';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    CommentAnalyzerComponent,
  ],
  template: '<app-comment-analyzer></app-comment-analyzer>'
})
export class AppComponent {
  title = 'youtube-comment-analyzer';
}
