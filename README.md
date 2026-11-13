# Nephrology EMR — Patient Management & AI Clinical Assistant

A small EMR for a general nephrology clinic: patient management, outpatient
clinical encounters, laboratory/kidney-function tracking with trend charts,
and an AI-assisted clinical summary.

- **Frontend:** Angular 18 (standalone components), TypeScript, Chart.js (via ng2-charts)
- **Backend:** Python, FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **AI:** Groq (Free tier, Llama 3.3 70B via GroqCloud) & OpenAI, with a documented mock fallback when no API key is configured

See [architecture.md](architecture.md) for design details and [workflow.md](workflow.md)
for the user-facing walkthrough of each feature.

## Prerequisites

- Python 3.11–3.13 (3.14 currently breaks `pydantic-core` wheel builds via pip)
- Node.js 18+ and npm

## 1. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Optional: enable real AI summaries (otherwise a mock summary is returned)
cp .env.example .env
# edit .env and set GROQ_API_KEY=gsk-... (or OPENAI_API_KEY=sk-...)

# Seed the SQLite database with 4 synthetic patients
python seed.py

# Run the API (http://localhost:8000)
python run.py
# (or: python -m uvicorn app.main:app --reload --port 8000)
```

Interactive API docs (Swagger UI) are auto-generated at `http://localhost:8000/docs`.

Run the backend tests:

```bash
python -m pytest -q
```

## 2. Frontend setup

```bash
cd frontend
npm install --legacy-peer-deps
npm start          # ng serve, http://localhost:4200
```

The frontend expects the API at `http://localhost:8000/api`
(configured in `frontend/src/environments/environment.ts`).

## 3. Using the app

Open `http://localhost:4200`. The patient list loads the seeded synthetic
patients. Click a patient to view/add encounters and lab results, see the
Creatinine/eGFR trend chart, and generate an AI clinical summary.

## Project layout

```
backend/
  app/
    main.py              FastAPI app, CORS, router registration
    database.py           SQLAlchemy engine/session
    models.py              ORM models (Patient, Condition, Medication, Allergy, Encounter, LabResult)
    schemas.py             Pydantic request/response schemas
    clinical.py             Reference ranges, CKD/UACR classification (KDIGO)
    utils.py                 Small helpers (age calculation)
    routers/
      patients.py            Patient CRUD, search, conditions/medications/allergies
      encounters.py           Clinical encounter CRUD
      labs.py                  Lab result CRUD + computed CKD stage/abnormal flags
      reference.py             Reference-range lookup for the frontend
      ai.py                     AI clinical summary endpoint
    services/
      ai_summary.py             Builds patient context, calls Groq/OpenAI, mock fallback
  seed.py                     Synthetic patient data loader
  tests/test_api.py             Pytest smoke tests

frontend/
  src/app/
    models/                   TypeScript interfaces mirroring API schemas
    services/                  HttpClient wrappers (one per resource)
    components/
      patient-list/             Listing + search
      patient-form/              New patient
      patient-detail/            Tabs: overview / encounters / labs / AI assistant
      encounter-form/            Reusable encounter entry form
      lab-form/                   Reusable lab result entry form
      lab-chart/                  Creatinine/eGFR trend chart (ng2-charts)
      ai-summary/                 AI summary trigger + disclaimer display
```

## Screenshots

See `docs/screenshots/`: patient list, patient overview, encounters,
lab trend chart + abnormal-value table, and the AI clinical summary panel.

## API reference

Base URL: `http://localhost:8000/api`

| Method | Path | Description |
|---|---|---|
| GET | `/patients?q=` | List patients, optional search by name or numeric ID |
| GET | `/patients/{id}` | Patient demographics + conditions/medications/allergies |
| POST | `/patients` | Create a patient |
| POST | `/patients/{id}/conditions` | Add a comorbidity/diagnosis |
| POST | `/patients/{id}/medications` | Add a current medication |
| POST | `/patients/{id}/allergies` | Add an allergy |
| GET | `/patients/{id}/encounters` | List encounters (most recent first) |
| POST | `/patients/{id}/encounters` | Create a clinical encounter |
| GET | `/patients/{id}/labs` | List lab results with computed CKD stage, UACR category, abnormal flags |
| POST | `/patients/{id}/labs` | Add a lab panel |
| GET | `/reference/lab-ranges` | Reference ranges/units for each lab parameter |
| POST | `/patients/{id}/ai-summary` | Generate an AI-assisted clinical summary |
| GET | `/health` | Liveness check |

Full request/response schemas: `http://localhost:8000/docs`.

## Database schema

SQLite, 6 tables (see `backend/app/models.py` for the SQLAlchemy definitions):

- `patients` (1) — `conditions`, `medications`, `allergies`, `encounters`, `lab_results` (N), each FK'd to `patients.id` with cascade delete.

Synthetic data for 4 patients (varying CKD stages, including one on
hemodialysis) is created by `backend/seed.py` — no real patient data is used.

## AI integration notes

- `backend/app/services/ai_summary.py` builds a plain-text context block from
  the patient's DB records only (demographics, conditions, medications,
  allergies, recent encounters, lab history with CKD staging) — nothing is
  fabricated.
- The LLM is explicitly instructed to only use supplied context, to never
  diagnose or prescribe, and to say so when information is missing.
- If `OPENAI_API_KEY` is unset, a deterministic mock summary is returned
  instead (clearly labeled `[MOCK SUMMARY ...]`) so the feature is reviewable
  without a paid API key.
- API/parsing failures surface as HTTP 502 with a message; they are not
  silently swallowed.
- Every response carries a clinical-review disclaimer and is visually
  distinguished from the original patient record in the UI (blue "AI-GENERATED" panel).
