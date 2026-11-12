"""Outpatient clinical encounter CRUD."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/patients/{patient_id}/encounters", tags=["encounters"])


def _get_patient_or_404(patient_id: int, db: Session) -> models.Patient:
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("", response_model=list[schemas.EncounterOut])
def list_encounters(patient_id: int, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    return (
        db.query(models.Encounter)
        .filter(models.Encounter.patient_id == patient_id)
        .order_by(models.Encounter.visit_date.desc())
        .all()
    )


@router.post("", response_model=schemas.EncounterOut, status_code=201)
def create_encounter(patient_id: int, payload: schemas.EncounterIn, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    encounter = models.Encounter(patient_id=patient_id, **payload.model_dump())
    db.add(encounter)
    db.commit()
    db.refresh(encounter)
    return encounter


@router.get("/{encounter_id}", response_model=schemas.EncounterOut)
def get_encounter(patient_id: int, encounter_id: int, db: Session = Depends(get_db)):
    encounter = db.get(models.Encounter, encounter_id)
    if encounter is None or encounter.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter
