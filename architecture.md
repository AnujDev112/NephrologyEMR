# Architecture

## Overview

A standard 3-tier app: Angular SPA -> FastAPI REST API -> SQLite, plus an
AI service layer the API calls into for clinical summaries.

```
┌─────────────────┐      HTTPS/JSON       ┌──────────────────┐      SQL      ┌──────────┐
│ Angular (4200)   │ ───────────────────▶ │ FastAPI (8000)    │ ────────────▶ │ SQLite    │
│ components/      │ ◀─────────────────── │ routers/           │ ◀──────────── │ nephro_   │
│ services/        │                      │  patients/encounters│              │ emr.db    │
└─────────────────┘                      │  /labs/reference/ai │              └──────────┘
                                          │ services/ai_summary │
                                          └──────────┬──────────┘
                                                     │ (only when OPENAI_API_KEY set)
                                                     ▼
                                            OpenAI Chat Completions API
```

## Backend

FastAPI chosen for fast iteration and automatic OpenAPI docs. Layering:

- **`models.py`** — SQLAlchemy ORM (the only place that knows about tables/FKs).
- **`schemas.py`** — Pydantic request/response contracts, decoupled from the
  ORM models so the API shape can evolve independently of storage (e.g.
  `PatientListItem` computes `age` instead of exposing `date_of_birth`).
- **`routers/*`** — one module per resource, each a thin FastAPI `APIRouter`
  doing validation + a DB call; no business logic beyond simple lookups.
- **`clinical.py`** — the one place lab reference ranges and KDIGO CKD/UACR
  classification rules live, reused by both the lab endpoints (for
  `abnormal_flags`/`ckd_stage`) and the AI context builder, so the two never
  disagree about what counts as "abnormal."
- **`services/ai_summary.py`** — builds a plain-text patient context from DB
  records and calls the LLM; isolated from the router so the prompt/context
  logic is independently testable and swappable.

Database relationships (all 1→N from `patients`, cascade-delete):
`conditions`, `medications`, `allergies`, `encounters`, `lab_results`.

### Why SQLite + SQLAlchemy over a JSON file

The assignment allowed either. SQLAlchemy + SQLite was chosen to get real
relational integrity (foreign keys, cascade deletes) and a migration path to
Postgres/SQL Server with only a connection-string change — "maintain
meaningful database relationships" is an explicit requirement, and that is
easiest to demonstrate with actual foreign keys rather than nested JSON.

## Frontend

Angular standalone components (no NgModules) — each route lazy-loads its
top-level component via `loadComponent`. Components split so each is reusable
and independently testable:

- `patient-list` / `patient-form` — top-level routed pages.
- `patient-detail` — the routed page for a single patient; owns data loading
  (`forkJoin` of patient/encounters/labs/reference-ranges) and tab state, and
  composes the reusable pieces below via `@Input`/`@Output`.
- `encounter-form`, `lab-form` — dumb, reusable entry forms; emit `saved` so
  the parent can patch its local list without a full reload.
- `lab-chart` — wraps `ng2-charts`' `BaseChartDirective`; takes a `labs`
  array and renders Creatinine (left axis) / eGFR (right axis) as a dual-axis
  line chart.
- `ai-summary` — calls the AI endpoint and renders the result in a visually
  distinct panel with its disclaimer, separate from clinician-entered data.

Services (`patient.service.ts`, `encounter.service.ts`, `lab.service.ts`,
`ai.service.ts`) are thin `HttpClient` wrappers, one per REST resource,
matching the backend's router split.

## AI integration

**Flow:** `patient-detail` → `AiService.generateSummary(id)` → `POST
/api/patients/{id}/ai-summary` → `ai_summary.generate_clinical_summary()`:

1. Load the patient and all related records (conditions, medications,
   allergies, encounters, labs) from the DB.
2. Flatten them into a plain-text context block (`_build_context`) — every
   fact in the prompt traces back to a DB row; nothing is invented.
3. Send a system prompt that pins the model to 6 fixed sections, forbids
   diagnosis/prescription, and requires it to flag missing information,
   plus the context as the user message.
4. Parse the response; raise `RuntimeError` (→ HTTP 502) on an API error or
   an empty/invalid response, instead of returning something misleading.
5. If no `OPENAI_API_KEY` is set, skip the network call entirely and return
   a deterministic `[MOCK SUMMARY ...]`-prefixed summary built from the same
   context data, so the feature is reviewable offline/without billing.

The API response always includes a `disclaimer` field, and the frontend
renders AI output inside a visually distinct blue panel labeled
"AI-GENERATED" with the model name and timestamp, never mixed into the
clinician-entered record.

## Testing

`backend/tests/test_api.py` uses an in-memory SQLite DB (via `StaticPool`)
and FastAPI's `TestClient`/dependency override, covering: patient
create/list/search/404, encounter + lab creation, CKD/UACR classification,
and the AI endpoint's mock fallback path. Run with `pytest -q`.
