"""SQLAlchemy ORM models for the Nephrology EMR.

Relationships:
    Patient 1--N Condition (comorbidities / established diagnoses)
    Patient 1--N Medication
    Patient 1--N Allergy
    Patient 1--N Encounter (clinical visits)
    Patient 1--N LabResult (lab panels over time)
"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    primary_diagnosis: Mapped[str] = mapped_column(String(200), default="")
    contact_number: Mapped[str] = mapped_column(String(30), default="")
    medical_history: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    conditions: Mapped[list["Condition"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    medications: Mapped[list["Medication"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    allergies: Mapped[list["Allergy"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    encounters: Mapped[list["Encounter"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan", order_by="desc(Encounter.visit_date)"
    )
    lab_results: Mapped[list["LabResult"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan", order_by="desc(LabResult.test_date)"
    )


class Condition(Base):
    """Comorbidity / established diagnosis."""

    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    diagnosed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(String(300), default="")

    patient: Mapped[Patient] = relationship(back_populates="conditions")


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    dosage: Mapped[str] = mapped_column(String(100), default="")
    frequency: Mapped[str] = mapped_column(String(100), default="")
    active: Mapped[bool] = mapped_column(default=True)

    patient: Mapped[Patient] = relationship(back_populates="medications")


class Allergy(Base):
    __tablename__ = "allergies"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    substance: Mapped[str] = mapped_column(String(200), nullable=False)
    reaction: Mapped[str] = mapped_column(String(200), default="")
    severity: Mapped[str] = mapped_column(String(50), default="")

    patient: Mapped[Patient] = relationship(back_populates="allergies")


class Encounter(Base):
    """A single outpatient clinical encounter/visit."""

    __tablename__ = "encounters"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Vitals
    bp_systolic: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bp_diastolic: Mapped[int | None] = mapped_column(Integer, nullable=True)
    heart_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)

    chief_complaint: Mapped[str] = mapped_column(Text, default="")
    symptoms: Mapped[str] = mapped_column(Text, default="")
    examination_notes: Mapped[str] = mapped_column(Text, default="")
    assessment: Mapped[str] = mapped_column(Text, default="")
    plan: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped[Patient] = relationship(back_populates="encounters")


class LabResult(Base):
    """One laboratory panel for a patient on a given date."""

    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    test_date: Mapped[date] = mapped_column(Date, nullable=False)

    serum_creatinine: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/dL
    egfr: Mapped[float | None] = mapped_column(Float, nullable=True)  # mL/min/1.73m2
    bun: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/dL
    potassium: Mapped[float | None] = mapped_column(Float, nullable=True)  # mmol/L
    hemoglobin: Mapped[float | None] = mapped_column(Float, nullable=True)  # g/dL
    calcium: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/dL
    phosphorus: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/dL
    uacr: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/g

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped[Patient] = relationship(back_populates="lab_results")
