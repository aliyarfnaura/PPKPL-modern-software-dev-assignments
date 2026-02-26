"""
FastAPI application entry point for the Action Item Extractor.

Application lifecycle:
- init_db() runs at import time to ensure the SQLite schema exists before handling requests.
- Routers are included for /notes and /action-items.
- Static files and the root HTML are served from the frontend directory.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes
from .schemas import ExtractLLMRequest, ExtractLLMResponse
from .services.extract import LLMUnavailableError, extract_action_items_llm

# ----- Configuration & lifecycle -----
# Ensure database tables exist before any request is handled.
init_db()

app = FastAPI(title="Action Item Extractor")


# ----- Root & static -----

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the frontend index page."""
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Frontend index not found")
    return html_path.read_text(encoding="utf-8")


# ----- Extract LLM endpoint -----

@app.post("/extract_llm", response_model=ExtractLLMResponse)
def extract_llm(request: ExtractLLMRequest) -> ExtractLLMResponse:
    """
    Extract action items from text using the LLM (Ollama).
    On success returns action_items list. On model/API unavailability returns 503.
    """
    try:
        items = extract_action_items_llm(request.text)
        return ExtractLLMResponse(action_items=items)
    except LLMUnavailableError:
        # Model not installed or Ollama not running; return 503 with clear message.
        raise HTTPException(
            status_code=503,
            detail="LLM model not available. Make sure Ollama is running and llama3.1 is installed.",
        )


# ----- Routers -----

app.include_router(notes.router)
app.include_router(action_items.router)

# Static files (must be after routers to avoid shadowing routes).
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")