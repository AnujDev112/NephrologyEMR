"""Seeds the SQLite database with synthetic nephrology patient data.

Run with: python seed.py
Safe to re-run: drops and recreates all tables first.
"""
from datetime import date

from app.database import Base, SessionLocal, engine
from app import models

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

patients_data = [
    {
        "patient": dict(
            name="Ramesh Gupta", date_of_birth=date(1962, 4, 12), gender="Male",
            primary_diagnosis="Chronic Kidney Disease Stage 3b",
            contact_number="+91-9876500001",
            medical_history="Type 2 diabetes for 15 years, hypertension for 10 years.",
        ),
        "conditions": [
            dict(name="Type 2 Diabetes Mellitus", diagnosed_date=date(2010, 3, 1), notes="On insulin"),
            dict(name="Hypertension", diagnosed_date=date(2014, 6, 15), notes="Controlled"),
        ],
        "medications": [
            dict(name="Insulin Glargine", dosage="20 units", frequency="Once nightly"),
            dict(name="Amlodipine", dosage="5mg", frequency="Once daily"),
            dict(name="Sodium Bicarbonate", dosage="500mg", frequency="Twice daily"),
        ],
        "allergies": [dict(substance="Sulfa drugs", reaction="Rash", severity="Moderate")],
        "encounters": [
            dict(visit_date=date(2026, 9, 1), bp_systolic=138, bp_diastolic=86, heart_rate=78,
                 temperature_c=36.8, weight_kg=74.5, chief_complaint="Routine CKD follow-up",
                 symptoms="Mild fatigue, no edema", examination_notes="No pedal edema, chest clear",
                 assessment="CKD stage 3b, stable", plan="Continue current meds, repeat labs in 3 months"),
            dict(visit_date=date(2026, 6, 2), bp_systolic=142, bp_diastolic=90, heart_rate=80,
                 temperature_c=36.9, weight_kg=75.0, chief_complaint="Increased fatigue",
                 symptoms="Fatigue, occasional nausea", examination_notes="Mild pallor noted",
                 assessment="CKD progression, anemia of CKD suspected", plan="Start iron supplementation, recheck Hb"),
        ],
        "labs": [
            dict(test_date=date(2026, 9, 1), serum_creatinine=2.1, egfr=32, bun=38, potassium=4.8,
                 hemoglobin=10.8, calcium=8.9, phosphorus=4.8, uacr=210),
            dict(test_date=date(2026, 6, 2), serum_creatinine=2.3, egfr=29, bun=42, potassium=5.0,
                 hemoglobin=10.2, calcium=8.7, phosphorus=5.1, uacr=260),
            dict(test_date=date(2026, 3, 1), serum_creatinine=1.9, egfr=36, bun=34, potassium=4.6,
                 hemoglobin=11.3, calcium=9.0, phosphorus=4.4, uacr=180),
        ],
    },
    {
        "patient": dict(
            name="Sunita Verma", date_of_birth=date(1978, 11, 2), gender="Female",
            primary_diagnosis="Early CKD secondary to Hypertensive Nephrosclerosis",
            contact_number="+91-9876500002",
            medical_history="Hypertension for 8 years, no diabetes.",
        ),
        "conditions": [dict(name="Hypertension", diagnosed_date=date(2018, 1, 10), notes="")],
        "medications": [dict(name="Losartan", dosage="50mg", frequency="Once daily")],
        "allergies": [],
        "encounters": [
            dict(visit_date=date(2026, 8, 20), bp_systolic=128, bp_diastolic=82, heart_rate=72,
                 temperature_c=36.7, weight_kg=68.0, chief_complaint="Routine follow-up",
                 symptoms="None", examination_notes="Unremarkable",
                 assessment="Early CKD, well controlled BP", plan="Continue losartan, annual labs"),
        ],
        "labs": [
            dict(test_date=date(2026, 8, 20), serum_creatinine=1.1, egfr=68, bun=16, potassium=4.2,
                 hemoglobin=13.1, calcium=9.4, phosphorus=3.6, uacr=22),
            dict(test_date=date(2025, 8, 18), serum_creatinine=1.0, egfr=72, bun=15, potassium=4.1,
                 hemoglobin=13.3, calcium=9.5, phosphorus=3.5, uacr=18),
        ],
    },
    {
        "patient": dict(
            name="Mohammed Imran", date_of_birth=date(1955, 2, 20), gender="Male",
            primary_diagnosis="End Stage Renal Disease on Hemodialysis",
            contact_number="+91-9876500003",
            medical_history="ESRD on thrice-weekly hemodialysis since 2023. History of MI in 2019.",
        ),
        "conditions": [
            dict(name="Coronary Artery Disease", diagnosed_date=date(2019, 5, 5), notes="Post-MI, stent placed"),
            dict(name="Secondary Hyperparathyroidism", diagnosed_date=date(2023, 2, 1), notes=""),
        ],
        "medications": [
            dict(name="Sevelamer", dosage="800mg", frequency="With meals"),
            dict(name="Erythropoietin", dosage="4000 IU", frequency="Weekly, post-dialysis"),
            dict(name="Aspirin", dosage="75mg", frequency="Once daily"),
        ],
        "allergies": [dict(substance="Penicillin", reaction="Anaphylaxis", severity="Severe")],
        "encounters": [
            dict(visit_date=date(2026, 10, 5), bp_systolic=150, bp_diastolic=92, heart_rate=84,
                 temperature_c=36.6, weight_kg=66.2, chief_complaint="Pre-dialysis review",
                 symptoms="Shortness of breath on exertion", examination_notes="Bilateral mild pedal edema",
                 assessment="Fluid overload, ESRD on HD", plan="Adjust dry weight, continue HD schedule"),
        ],
        "labs": [
            dict(test_date=date(2026, 10, 5), serum_creatinine=7.8, egfr=6, bun=68, potassium=5.6,
                 hemoglobin=9.8, calcium=8.2, phosphorus=6.1, uacr=None),
            dict(test_date=date(2026, 7, 2), serum_creatinine=8.1, egfr=5, bun=72, potassium=5.8,
                 hemoglobin=9.5, calcium=8.0, phosphorus=6.4, uacr=None),
        ],
    },
    {
        "patient": dict(
            name="Anjali Nair", date_of_birth=date(1990, 7, 30), gender="Female",
            primary_diagnosis="IgA Nephropathy",
            contact_number="+91-9876500004",
            medical_history="Biopsy-proven IgA nephropathy diagnosed 2024. No other comorbidities.",
        ),
        "conditions": [dict(name="IgA Nephropathy", diagnosed_date=date(2024, 1, 15), notes="Biopsy confirmed")],
        "medications": [dict(name="Lisinopril", dosage="10mg", frequency="Once daily")],
        "allergies": [],
        "encounters": [
            dict(visit_date=date(2026, 9, 28), bp_systolic=118, bp_diastolic=76, heart_rate=70,
                 temperature_c=36.7, weight_kg=58.0, chief_complaint="Follow-up, no new symptoms",
                 symptoms="None", examination_notes="Unremarkable",
                 assessment="IgA nephropathy, stable proteinuria", plan="Continue ACE inhibitor, repeat UACR in 6 months"),
        ],
        "labs": [
            dict(test_date=date(2026, 9, 28), serum_creatinine=0.9, egfr=88, bun=14, potassium=4.0,
                 hemoglobin=12.8, calcium=9.3, phosphorus=3.4, uacr=145),
        ],
    },
]

for entry in patients_data:
    patient = models.Patient(**entry["patient"])
    db.add(patient)
    db.flush()  # assign patient.id

    for c in entry["conditions"]:
        db.add(models.Condition(patient_id=patient.id, **c))
    for m in entry["medications"]:
        db.add(models.Medication(patient_id=patient.id, **m))
    for a in entry["allergies"]:
        db.add(models.Allergy(patient_id=patient.id, **a))
    for e in entry["encounters"]:
        db.add(models.Encounter(patient_id=patient.id, **e))
    for lab in entry["labs"]:
        db.add(models.LabResult(patient_id=patient.id, **lab))

db.commit()
db.close()

print(f"Seeded {len(patients_data)} synthetic patients into nephro_emr.db")
