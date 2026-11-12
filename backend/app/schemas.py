"""Pydantic request/response schemas (API boundary, decoupled from ORM models)."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- Conditions / Medications / Allergies ----------

class ConditionIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    diagnosed_date: date | None = None
    notes: str = ""


class ConditionOut(ConditionIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MedicationIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    dosage: str = ""
    frequency: str = ""
    active: bool = True


class MedicationOut(MedicationIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AllergyIn(BaseModel):
    substance: str = Field(min_length=1, max_length=200)
    reaction: str = ""
    severity: str = ""


class AllergyOut(AllergyIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Patient ----------

class PatientIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    date_of_birth: date
    gender: str = Field(min_length=1, max_length=20)
    primary_diagnosis: str = ""
    contact_number: str = ""
    medical_history: str = ""


class PatientListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int
    gender: str
    primary_diagnosis: str


class PatientDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    date_of_birth: date
    age: int
    gender: str
    primary_diagnosis: str
    contact_number: str
    medical_history: str
    conditions: list[ConditionOut] = []
    medications: list[MedicationOut] = []
    allergies: list[AllergyOut] = []


# ---------- Encounter ----------

class EncounterIn(BaseModel):
    visit_date: date
    bp_systolic: int | None = Field(default=None, ge=40, le=300)
    bp_diastolic: int | None = Field(default=None, ge=20, le=200)
    heart_rate: int | None = Field(default=None, ge=20, le=250)
    temperature_c: float | None = Field(default=None, ge=30, le=45)
    weight_kg: float | None = Field(default=None, ge=1, le=400)
    chief_complaint: str = ""
    symptoms: str = ""
    examination_notes: str = ""
    assessment: str = ""
    plan: str = ""


class EncounterOut(EncounterIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    created_at: datetime


# ---------- Lab Results ----------

class LabResultIn(BaseModel):
    test_date: date
    serum_creatinine: float | None = Field(default=None, ge=0)
    egfr: float | None = Field(default=None, ge=0)
    bun: float | None = Field(default=None, ge=0)
    potassium: float | None = Field(default=None, ge=0)
    hemoglobin: float | None = Field(default=None, ge=0)
    calcium: float | None = Field(default=None, ge=0)
    phosphorus: float | None = Field(default=None, ge=0)
    uacr: float | None = Field(default=None, ge=0)


class LabResultOut(LabResultIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    ckd_stage: str | None = None
    uacr_category: str | None = None
    abnormal_flags: dict[str, bool] = {}


# ---------- AI Assistant ----------

class AISummaryResponse(BaseModel):
    generated_at: datetime
    model: str
    summary: str
    disclaimer: str = (
        "AI-generated content is a drafting aid for clinician review only. "
        "It does not constitute a diagnosis or treatment recommendation and "
        "must be verified against the full medical record before any clinical decision."
    )
