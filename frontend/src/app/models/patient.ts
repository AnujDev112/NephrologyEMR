export interface PatientListItem {
  id: number;
  name: string;
  age: number;
  gender: string;
  primary_diagnosis: string;
}

export interface Condition {
  id?: number;
  name: string;
  diagnosed_date: string | null;
  notes: string;
}

export interface Medication {
  id?: number;
  name: string;
  dosage: string;
  frequency: string;
  active: boolean;
}

export interface Allergy {
  id?: number;
  substance: string;
  reaction: string;
  severity: string;
}

export interface PatientDetail {
  id: number;
  name: string;
  date_of_birth: string;
  age: number;
  gender: string;
  primary_diagnosis: string;
  contact_number: string;
  medical_history: string;
  conditions: Condition[];
  medications: Medication[];
  allergies: Allergy[];
}

export interface PatientCreate {
  name: string;
  date_of_birth: string;
  gender: string;
  primary_diagnosis: string;
  contact_number: string;
  medical_history: string;
}
