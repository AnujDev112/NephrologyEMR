import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Encounter } from '../models/encounter';

@Injectable({ providedIn: 'root' })
export class EncounterService {
  constructor(private http: HttpClient) {}

  private base(patientId: number): string {
    return `${environment.apiUrl}/patients/${patientId}/encounters`;
  }

  list(patientId: number): Observable<Encounter[]> {
    return this.http.get<Encounter[]>(this.base(patientId));
  }

  create(patientId: number, payload: Encounter): Observable<Encounter> {
    return this.http.post<Encounter>(this.base(patientId), payload);
  }
}
