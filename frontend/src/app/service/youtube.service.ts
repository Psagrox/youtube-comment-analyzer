import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class YoutubeService {
  private apiUrl = 'http://127.0.0.1:5000';

  private http = inject(HttpClient);

  analyzeComments(videoUrl: string): Observable<any> {
    // Definir los headers, en este caso el Content-Type es application/json
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // Enviar la solicitud POST con el videoUrl
    return this.http.post(`${this.apiUrl}/analyze`, { videoUrl }, { headers }).pipe(
      catchError((error) => {
          console.error('Error from backend:', error);  // Imprime el error en la consola del navegador
          throw error;  // Re-lanza el error para manejarlo en el componente
      })
  );
  }
}
