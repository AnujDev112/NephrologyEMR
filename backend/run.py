"""Convenience runner for the Nephrology EMR backend.

Guarantees execution using the active virtual environment:
    python run.py
"""
import sys
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
