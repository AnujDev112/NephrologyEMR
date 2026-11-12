export interface LabResult {
  id?: number;
  patient_id?: number;
  test_date: string;
  serum_creatinine: number | null;
  egfr: number | null;
  bun: number | null;
  potassium: number | null;
  hemoglobin: number | null;
  calcium: number | null;
  phosphorus: number | null;
  uacr: number | null;
  ckd_stage?: string | null;
  uacr_category?: string | null;
  abnormal_flags?: Record<string, boolean>;
}

export interface ReferenceRange {
  low: number | null;
  high: number | null;
  unit: string;
}

export type LabField = keyof Omit<
  LabResult,
  'id' | 'patient_id' | 'test_date' | 'ckd_stage' | 'uacr_category' | 'abnormal_flags'
>;

export const LAB_FIELD_LABELS: Record<LabField, string> = {
  serum_creatinine: 'Serum Creatinine',
  egfr: 'eGFR',
  bun: 'Blood Urea Nitrogen (BUN)',
  potassium: 'Potassium',
  hemoglobin: 'Hemoglobin',
  calcium: 'Calcium',
  phosphorus: 'Phosphorus',
  uacr: 'Urine Albumin-Creatinine Ratio (UACR)',
};
