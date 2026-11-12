"""Reference ranges and KDIGO-style classification used across the app.

Kept as plain functions/constants (no class needed) so both the lab
endpoints and the AI context-builder can reuse the same single source of
truth for "is this value abnormal" / "what CKD stage is this".
"""

# (low, high, unit) — None bound means unbounded on that side.
REFERENCE_RANGES: dict[str, tuple[float | None, float | None, str]] = {
    "serum_creatinine": (0.6, 1.3, "mg/dL"),
    "egfr": (90, None, "mL/min/1.73m2"),
    "bun": (7, 20, "mg/dL"),
    "potassium": (3.5, 5.1, "mmol/L"),
    "hemoglobin": (12, 17, "g/dL"),
    "calcium": (8.6, 10.3, "mg/dL"),
    "phosphorus": (2.5, 4.5, "mg/dL"),
    "uacr": (0, 30, "mg/g"),
}


def is_abnormal(field: str, value: float | None) -> bool | None:
    """Return True/False if out of range, or None if not measured/known."""
    if value is None or field not in REFERENCE_RANGES:
        return None
    low, high, _unit = REFERENCE_RANGES[field]
    if low is not None and value < low:
        return True
    if high is not None and value > high:
        return True
    return False


def ckd_stage(egfr: float | None) -> str | None:
    """Classify eGFR into KDIGO CKD G-stages."""
    if egfr is None:
        return None
    if egfr >= 90:
        return "G1 (Normal or high)"
    if egfr >= 60:
        return "G2 (Mildly decreased)"
    if egfr >= 45:
        return "G3a (Mildly to moderately decreased)"
    if egfr >= 30:
        return "G3b (Moderately to severely decreased)"
    if egfr >= 15:
        return "G4 (Severely decreased)"
    return "G5 (Kidney failure)"


def uacr_category(uacr: float | None) -> str | None:
    """Classify UACR into KDIGO A-categories."""
    if uacr is None:
        return None
    if uacr < 30:
        return "A1 (Normal to mildly increased)"
    if uacr <= 300:
        return "A2 (Moderately increased)"
    return "A3 (Severely increased)"
