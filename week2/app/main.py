from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .db import init_db
from .routers import action_items, notes
from . import db
from .services.extract import extract_action_items_llm

init_db()

app = FastAPI(title="Action Item Extractor")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


class ExtractRequest(BaseModel):
    text: str


@app.post("/extract_llm")
def extract_llm(request: ExtractRequest) -> Dict[str, list[str]]:
    action_items = extract_action_items_llm(request.text)
    return {"action_items": action_items}


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")