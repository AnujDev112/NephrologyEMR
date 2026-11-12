import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { LabResult, ReferenceRange } from '../models/lab-result';

@Injectable({ providedIn: 'root' })
export class LabService {
  constructor(private http: HttpClient) {}

  private base(patientId: number): string {
    return `${environment.apiUrl}/patients/${patientId}/labs`;
  }

  list(patientId: number): Observable<LabResult[]> {
    return this.http.get<LabResult[]>(this.base(patientId));
  }

  create(patientId: number, payload: LabResult): Observable<LabResult> {
    return this.http.post<LabResult>(this.base(patientId), payload);
  }

  referenceRanges(): Observable<Record<string, ReferenceRange>> {
    return this.http.get<Record<string, ReferenceRange>>(
      `${environment.apiUrl}/reference/lab-ranges`
    );
  }
}
