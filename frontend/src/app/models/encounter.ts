export interface Encounter {
  id?: number;
  patient_id?: number;
  visit_date: string;
  bp_systolic: number | null;
  bp_diastolic: number | null;
  heart_rate: number | null;
  temperature_c: number | null;
  weight_kg: number | null;
  chief_complaint: string;
  symptoms: string;
  examination_notes: string;
  assessment: string;
  plan: string;
  created_at?: string;
}
