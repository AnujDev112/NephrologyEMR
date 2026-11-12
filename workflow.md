# Workflow

## Using the application

1. **Find a patient** — `Patients` page lists everyone with ID, name, age,
   gender, and primary diagnosis. Search by name or numeric patient ID.
2. **Add a patient** — `+ New Patient` captures demographics; conditions,
   medications and allergies are added afterward from the patient page
   (kept separate so the create form stays short).
3. **Open a patient record** — click a row to land on a tabbed detail page:
   - **Overview** — demographics, medical history notes, comorbidities,
     medications, allergies.
   - **Encounters** — log a new outpatient visit (vitals, chief complaint,
     symptoms, exam notes, assessment, plan) and review prior visits,
     newest first.
   - **Lab Results** — add a lab panel (Creatinine, eGFR, BUN, Potassium,
     Hemoglobin, Calcium, Phosphorus, UACR); the Creatinine/eGFR trend chart
     and history table update immediately. Out-of-range values are flagged
     red using the reference ranges in `clinical.py`; eGFR-derived CKD stage
     and UACR category are shown per row.
   - **AI Clinical Assistant** — click "Generate AI Clinical Summary" to get
     a structured draft (history, comorbidities, Creatinine/eGFR trend,
     abnormal findings, missing/inconsistent info, follow-up considerations)
     built only from that patient's recorded data, shown in a clearly
     labeled AI panel with a review disclaimer.

## Development workflow (how this was built)

Built end-to-end with Claude Code as the primary coding assistant, following
the assignment's stack choice (FastAPI + SQLite + Angular + OpenAI SDK):

1. **Backend first.** Modeled the domain (`patients` and the 5 related
   tables), then layered schemas → clinical reference-range/CKD logic →
   routers → AI service, verified at each step with `pytest` and live
   `curl` calls against a running `uvicorn` instance before touching the
   frontend.
2. **Synthetic data.** `seed.py` was written and run immediately so every
   later screen had real, varied data (different CKD stages, a dialysis
   patient, a stable early-CKD patient) to render against instead of
   placeholders.
3. **Frontend second.** Scaffolded with the Angular CLI, then built
   services → models → reusable form/chart components → the tabbed patient
   page, matching the backend's router split 1:1 so each HTTP service
   mirrors one FastAPI router.
4. **Verification.** Backend: `pytest` (7 tests covering CRUD, CKD/UACR
   classification, and the AI mock-fallback path). Frontend: `ng build`
   for type-checking, then a scripted headless-browser pass (Playwright)
   driving the real running app — patient list → detail tabs → lab chart →
   AI summary generation — checked for console errors and reviewed via
   screenshots, rather than only trusting a successful compile.
5. **Known environment snag:** the host's default Python was 3.14, which
   currently fails to build `pydantic-core`'s wheel; the backend venv uses
   Python 3.13 instead (see README prerequisites).
