"""Smoke tests for the core API surface, using an isolated in-memory SQLite DB."""
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import clinical
from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSession = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def _fresh_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db
client = TestClient(app)


def _create_patient():
    resp = client.post(
        "/api/patients",
        json={
            "name": "Test Patient",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "primary_diagnosis": "CKD Stage 2",
        },
    )
    assert resp.status_code == 201
    return resp.json()


def test_create_and_list_patient():
    patient = _create_patient()
    resp = client.get("/api/patients")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["name"] == "Test Patient"
    assert body[0]["age"] >= 40  # born 1980


def test_search_patient_by_name():
    _create_patient()
    resp = client.get("/api/patients", params={"q": "test"})
    assert len(resp.json()) == 1
    resp = client.get("/api/patients", params={"q": "nomatch"})
    assert len(resp.json()) == 0


def test_get_patient_404():
    resp = client.get("/api/patients/999")
    assert resp.status_code == 404


def test_create_encounter_and_lab():
    patient = _create_patient()
    pid = patient["id"]

    enc_resp = client.post(
        f"/api/patients/{pid}/encounters",
        json={
            "visit_date": "2026-01-10",
            "bp_systolic": 130,
            "bp_diastolic": 85,
            "heart_rate": 76,
            "chief_complaint": "Routine check",
        },
    )
    assert enc_resp.status_code == 201
    assert enc_resp.json()["bp_systolic"] == 130

    lab_resp = client.post(
        f"/api/patients/{pid}/labs",
        json={"test_date": "2026-01-10", "serum_creatinine": 1.5, "egfr": 42},
    )
    assert lab_resp.status_code == 201
    lab = lab_resp.json()
    assert lab["ckd_stage"] == "G3b (Moderately to severely decreased)"
    assert lab["abnormal_flags"]["serum_creatinine"] is True


def test_ai_summary_mock_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    patient = _create_patient()
    resp = client.post(f"/api/patients/{patient['id']}/ai-summary")
    assert resp.status_code == 200
    body = resp.json()
    assert body["model"] == "mock"
    assert "disclaimer" in body
    assert "MOCK SUMMARY" in body["summary"]


def test_groq_client_resolution(monkeypatch):
    from app.services.ai_summary import _get_client_and_model

    monkeypatch.setenv("GROQ_API_KEY", "gsk_test_key_12345")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client, model = _get_client_and_model()
    assert client is not None
    assert client.api_key == "gsk_test_key_12345"
    assert "api.groq.com" in str(client.base_url)
    assert model == "llama-3.3-70b-versatile"


def test_ckd_staging():
    assert clinical.ckd_stage(95) == "G1 (Normal or high)"
    assert clinical.ckd_stage(50) == "G3a (Mildly to moderately decreased)"
    assert clinical.ckd_stage(10) == "G5 (Kidney failure)"
    assert clinical.ckd_stage(None) is None


def test_uacr_category():
    assert clinical.uacr_category(10) == "A1 (Normal to mildly increased)"
    assert clinical.uacr_category(150) == "A2 (Moderately increased)"
    assert clinical.uacr_category(400) == "A3 (Severely increased)"
