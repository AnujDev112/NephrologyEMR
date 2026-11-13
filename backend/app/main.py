"""FastAPI application entrypoint for the Nephrology EMR backend."""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.database import Base, engine
from app.routers import ai, encounters, labs, patients, reference

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nephrology EMR API",
    description="Patient management, clinical encounters, lab trends, and an AI clinical assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(encounters.router)
app.include_router(labs.router)
app.include_router(reference.router)
app.include_router(ai.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
