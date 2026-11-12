import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  Allergy,
  Condition,
  Medication,
  PatientCreate,
  PatientDetail,
  PatientListItem,
} from '../models/patient';

@Injectable({ providedIn: 'root' })
export class PatientService {
  private readonly base = `${environment.apiUrl}/patients`;

  constructor(private http: HttpClient) {}

  list(query?: string): Observable<PatientListItem[]> {
    const params: Record<string, string> = query ? { q: query } : {};
    return this.http.get<PatientListItem[]>(this.base, { params });
  }

  get(id: number): Observable<PatientDetail> {
    return this.http.get<PatientDetail>(`${this.base}/${id}`);
  }

  create(payload: PatientCreate): Observable<PatientDetail> {
    return this.http.post<PatientDetail>(this.base, payload);
  }

  addCondition(patientId: number, payload: Condition): Observable<Condition> {
    return this.http.post<Condition>(`${this.base}/${patientId}/conditions`, payload);
  }

  addMedication(patientId: number, payload: Medication): Observable<Medication> {
    return this.http.post<Medication>(`${this.base}/${patientId}/medications`, payload);
  }

  addAllergy(patientId: number, payload: Allergy): Observable<Allergy> {
    return this.http.post<Allergy>(`${this.base}/${patientId}/allergies`, payload);
  }
}
