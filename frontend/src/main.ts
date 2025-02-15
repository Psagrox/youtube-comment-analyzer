import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { YoutubeService } from './app/service/youtube.service';
import { Chart, registerables } from 'chart.js';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

Chart.register(...registerables);

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    YoutubeService, provideAnimationsAsync()
  ]
}).catch(err => console.error(err));
