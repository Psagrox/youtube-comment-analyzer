import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class YoutubeService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  analyzeComments(videoUrl: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/analyze`, { videoUrl });
  }
}
