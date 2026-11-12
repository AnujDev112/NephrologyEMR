"""Laboratory results CRUD, with CKD staging and abnormal-value flags."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import clinical, models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/patients/{patient_id}/labs", tags=["labs"])


def _get_patient_or_404(patient_id: int, db: Session) -> models.Patient:
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def _to_out(lab: models.LabResult) -> schemas.LabResultOut:
    fields = (
        "serum_creatinine", "egfr", "bun", "potassium",
        "hemoglobin", "calcium", "phosphorus", "uacr",
    )
    flags = {
        f: flag
        for f in fields
        if (flag := clinical.is_abnormal(f, getattr(lab, f))) is not None
    }
    return schemas.LabResultOut(
        id=lab.id,
        patient_id=lab.patient_id,
        test_date=lab.test_date,
        serum_creatinine=lab.serum_creatinine,
        egfr=lab.egfr,
        bun=lab.bun,
        potassium=lab.potassium,
        hemoglobin=lab.hemoglobin,
        calcium=lab.calcium,
        phosphorus=lab.phosphorus,
        uacr=lab.uacr,
        ckd_stage=clinical.ckd_stage(lab.egfr),
        uacr_category=clinical.uacr_category(lab.uacr),
        abnormal_flags=flags,
    )


@router.get("", response_model=list[schemas.LabResultOut])
def list_labs(patient_id: int, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    labs = (
        db.query(models.LabResult)
        .filter(models.LabResult.patient_id == patient_id)
        .order_by(models.LabResult.test_date.desc())
        .all()
    )
    return [_to_out(lab) for lab in labs]


@router.post("", response_model=schemas.LabResultOut, status_code=201)
def create_lab(patient_id: int, payload: schemas.LabResultIn, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    lab = models.LabResult(patient_id=patient_id, **payload.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return _to_out(lab)
