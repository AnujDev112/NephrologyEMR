"""AI-powered clinical summary endpoint."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.ai_summary import generate_clinical_summary

router = APIRouter(prefix="/api/patients/{patient_id}/ai-summary", tags=["ai"])


@router.post("", response_model=schemas.AISummaryResponse)
def create_ai_summary(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        summary_text, model = generate_clinical_summary(patient)
    except RuntimeError as exc:
        # Invalid/empty LLM response or upstream API failure.
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return schemas.AISummaryResponse(
        generated_at=datetime.utcnow(),
        model=model,
        summary=summary_text,
    )
