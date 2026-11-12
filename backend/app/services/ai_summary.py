"""Builds patient context and calls an LLM to draft a clinical summary.

Design notes:
  - Context is built entirely from DB records; nothing is invented here.
  - If no OPENAI_API_KEY is configured, falls back to a deterministic,
    clearly-labeled mock summary (per the assignment: "a documented mock
    implementation" is acceptable where API access is restricted).
  - The LLM is instructed to only use the supplied context, never to
    diagnose or prescribe, and to flag missing/inconsistent information.
"""
import os

from openai import APIError, APIStatusError, OpenAI

from app import clinical, models

SYSTEM_PROMPT = """You are a clinical documentation assistant for a nephrology clinic.
You draft a structured summary for a physician to review. You NEVER invent facts that
are not present in the provided patient context, and you NEVER state a diagnosis or
prescribe/alter treatment yourself - you only summarize, highlight trends/abnormalities
found in the data, and suggest topics for the clinician to consider.
If the context is missing information needed for a section, say so explicitly instead
of guessing. Structure your response with these headings:
1. Nephrology History Summary
2. Comorbidities & Medical Conditions
3. Creatinine / eGFR Trend
4. Abnormal Laboratory Findings
5. Missing or Inconsistent Information
6. Follow-up Considerations for Clinician Review
"""


def _build_context(patient: models.Patient) -> str:
    """Flatten DB records for this patient into a plain-text context block."""
    lines = [
        f"Patient: {patient.name}, gender: {patient.gender}, DOB: {patient.date_of_birth}",
        f"Primary diagnosis on file: {patient.primary_diagnosis or 'not recorded'}",
        f"Medical history notes: {patient.medical_history or 'not recorded'}",
    ]

    lines.append("\nComorbidities / Established Diagnoses:")
    if patient.conditions:
        for c in patient.conditions:
            lines.append(f"- {c.name} (diagnosed: {c.diagnosed_date or 'unknown'}) {c.notes}".strip())
    else:
        lines.append("- None recorded")

    lines.append("\nCurrent Medications:")
    if patient.medications:
        for m in patient.medications:
            status = "active" if m.active else "inactive"
            lines.append(f"- {m.name} {m.dosage} {m.frequency} ({status})".strip())
    else:
        lines.append("- None recorded")

    lines.append("\nAllergies:")
    if patient.allergies:
        for a in patient.allergies:
            lines.append(f"- {a.substance}: {a.reaction} (severity: {a.severity or 'unknown'})")
    else:
        lines.append("- None recorded")

    lines.append("\nRecent Encounters (most recent first):")
    if patient.encounters:
        for e in patient.encounters[:5]:
            lines.append(
                f"- {e.visit_date}: complaint='{e.chief_complaint}'; "
                f"assessment='{e.assessment}'; plan='{e.plan}'; "
                f"vitals: BP {e.bp_systolic}/{e.bp_diastolic}, HR {e.heart_rate}, "
                f"Temp {e.temperature_c}C, Weight {e.weight_kg}kg"
            )
    else:
        lines.append("- None recorded")

    lines.append("\nLaboratory Results (most recent first):")
    if patient.lab_results:
        for lab in patient.lab_results[:10]:
            stage = clinical.ckd_stage(lab.egfr)
            lines.append(
                f"- {lab.test_date}: Creatinine={lab.serum_creatinine} mg/dL, "
                f"eGFR={lab.egfr} mL/min/1.73m2 ({stage or 'n/a'}), BUN={lab.bun} mg/dL, "
                f"K={lab.potassium} mmol/L, Hb={lab.hemoglobin} g/dL, "
                f"Ca={lab.calcium} mg/dL, Phosphorus={lab.phosphorus} mg/dL, "
                f"UACR={lab.uacr} mg/g"
            )
    else:
        lines.append("- None recorded")

    return "\n".join(lines)


def _mock_summary(patient: models.Patient) -> str:
    """Deterministic fallback used when no LLM API key is configured."""
    latest_lab = patient.lab_results[0] if patient.lab_results else None
    stage = clinical.ckd_stage(latest_lab.egfr) if latest_lab else None
    parts = [
        "[MOCK SUMMARY - no OPENAI_API_KEY configured, generated without an LLM call]",
        f"1. Nephrology History Summary: {patient.name} has a primary diagnosis of "
        f"'{patient.primary_diagnosis or 'not recorded'}' with {len(patient.encounters)} "
        f"encounter(s) on file.",
        f"2. Comorbidities & Medical Conditions: {', '.join(c.name for c in patient.conditions) or 'None recorded'}.",
        f"3. Creatinine / eGFR Trend: latest eGFR is {latest_lab.egfr if latest_lab else 'not available'} "
        f"({stage or 'stage unknown'}).",
        "4. Abnormal Laboratory Findings: see lab table for values flagged outside reference range.",
        "5. Missing or Inconsistent Information: unable to assess without an LLM call; "
        "review the record directly.",
        "6. Follow-up Considerations for Clinician Review: configure OPENAI_API_KEY to "
        "enable full AI-assisted analysis.",
    ]
    return "\n".join(parts)


def generate_clinical_summary(patient: models.Patient) -> tuple[str, str]:
    """Return (summary_text, model_name_used)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _mock_summary(patient), "mock"

    context = _build_context(patient)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Patient context:\n\n{context}"},
            ],
        )
    except (APIError, APIStatusError) as exc:
        raise RuntimeError(f"LLM API call failed: {exc}") from exc

    choice = response.choices[0] if response.choices else None
    content = choice.message.content if choice and choice.message else None
    if not content or not content.strip():
        raise RuntimeError("LLM returned an empty or invalid response")

    return content.strip(), model
