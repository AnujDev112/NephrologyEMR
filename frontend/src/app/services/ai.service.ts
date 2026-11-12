import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AISummaryResponse } from '../models/ai-summary';

@Injectable({ providedIn: 'root' })
export class AiService {
  constructor(private http: HttpClient) {}

  generateSummary(patientId: number): Observable<AISummaryResponse> {
    return this.http.post<AISummaryResponse>(
      `${environment.apiUrl}/patients/${patientId}/ai-summary`,
      {}
    );
  }
}
