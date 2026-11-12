"""Static reference data the frontend needs for rendering (ranges, units)."""
from fastapi import APIRouter

from app import clinical

router = APIRouter(prefix="/api/reference", tags=["reference"])


@router.get("/lab-ranges")
def lab_ranges():
    return {
        field: {"low": low, "high": high, "unit": unit}
        for field, (low, high, unit) in clinical.REFERENCE_RANGES.items()
    }
