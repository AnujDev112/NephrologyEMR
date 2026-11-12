"""Patient listing, search, demographics, and medical-history sub-resources."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import calculate_age

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[schemas.PatientListItem])
def list_patients(q: str | None = None, db: Session = Depends(get_db)):
    """List patients, optionally filtered by name or patient ID (``q``)."""
    query = db.query(models.Patient)
    if q:
        filters = [models.Patient.name.ilike(f"%{q}%")]
        if q.isdigit():
            filters.append(models.Patient.id == int(q))
        query = query.filter(or_(*filters))
    patients = query.order_by(models.Patient.name).all()
    return [
        schemas.PatientListItem(
            id=p.id,
            name=p.name,
            age=calculate_age(p.date_of_birth),
            gender=p.gender,
            primary_diagnosis=p.primary_diagnosis,
        )
        for p in patients
    ]


def _get_patient_or_404(patient_id: int, db: Session) -> models.Patient:
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/{patient_id}", response_model=schemas.PatientDetail)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = _get_patient_or_404(patient_id, db)
    return schemas.PatientDetail(
        id=patient.id,
        name=patient.name,
        date_of_birth=patient.date_of_birth,
        age=calculate_age(patient.date_of_birth),
        gender=patient.gender,
        primary_diagnosis=patient.primary_diagnosis,
        contact_number=patient.contact_number,
        medical_history=patient.medical_history,
        conditions=patient.conditions,
        medications=patient.medications,
        allergies=patient.allergies,
    )


@router.post("", response_model=schemas.PatientDetail, status_code=201)
def create_patient(payload: schemas.PatientIn, db: Session = Depends(get_db)):
    patient = models.Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return get_patient(patient.id, db)


@router.post("/{patient_id}/conditions", response_model=schemas.ConditionOut, status_code=201)
def add_condition(patient_id: int, payload: schemas.ConditionIn, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    condition = models.Condition(patient_id=patient_id, **payload.model_dump())
    db.add(condition)
    db.commit()
    db.refresh(condition)
    return condition


@router.post("/{patient_id}/medications", response_model=schemas.MedicationOut, status_code=201)
def add_medication(patient_id: int, payload: schemas.MedicationIn, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    medication = models.Medication(patient_id=patient_id, **payload.model_dump())
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


@router.post("/{patient_id}/allergies", response_model=schemas.AllergyOut, status_code=201)
def add_allergy(patient_id: int, payload: schemas.AllergyIn, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    allergy = models.Allergy(patient_id=patient_id, **payload.model_dump())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy
