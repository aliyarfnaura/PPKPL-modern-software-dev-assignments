# Week 2: Action Item Extractor

## 1. Project Overview

This is a **FastAPI** web application that extracts **action items** (tasks, to-dos) from free-form text. Users paste notes into a simple frontend and can:

- **Heuristic extraction** — Rule-based parsing of bullets, keywords (e.g. `TODO:`, `Action:`), and checkboxes (`[ ]`), with optional imperative-sentence detection.
- **LLM extraction** — Ollama-powered extraction using the `llama3.1` model, returning a JSON array of action items.

Extracted items can be stored as **notes** in SQLite, and **action items** can be marked done via the API and UI. The app serves a minimal HTML/JS frontend and exposes a REST API for all operations.

---

## 2. Features

- **Heuristic action item extraction** — Bullets (`-`, `*`, `1.`), keywords (`TODO:`, `Action:`, `Next:`), checkboxes (`[ ]`, `[todo]`), and fallback imperative detection.
- **LLM-powered extraction** — Via Ollama; sends text to the model and parses a JSON array of strings. On parse or API errors, returns an empty list.
- **Note creation and retrieval** — Create notes (POST), get one by id (GET), list all notes (GET).
- **Action item completion** — List action items (optionally by note), mark items done/not done (POST).
- **Frontend integration** — Buttons: **Extract** (heuristic + optional save as note), **Extract LLM** (LLM-only, display in UI), **List Notes** (fetch and render all notes without refresh).

---

## 3. Project Structure

```
week2/
├── app/
│   ├── main.py          # FastAPI app: routes /, /extract_llm; mounts routers and static
│   ├── db.py            # SQLite layer: init_db, notes and action_items CRUD
│   ├── schemas.py       # Pydantic request/response models for the API
│   ├── routers/
│   │   ├── notes.py     # GET/POST /notes, GET /notes/{note_id}
│   │   └── action_items.py  # POST /action-items/extract, GET /action-items, POST /action-items/{id}/done
│   └── services/
│       └── extract.py   # extract_action_items (heuristic), extract_action_items_llm (Ollama)
├── frontend/
│   └── index.html       # Single-page UI: textarea, Extract / Extract LLM / List Notes
├── tests/
│   └── test_extract.py  # pytest: heuristic extraction + extract_action_items_llm (mocked)
├── data/                # Created at runtime; contains app.db (SQLite)
└── README.md
```

| Path | Purpose |
|------|--------|
| **app/** | Backend application package. |
| **app/main.py** | Application entry point; `init_db()`, root route, `/extract_llm`, router includes, static mount. |
| **app/db.py** | All database access; creates tables and exposes notes/action_items operations. |
| **app/schemas.py** | Pydantic models for API contracts (request/response). |
| **app/routers/** | FastAPI routers for notes and action-items. |
| **app/services/extract.py** | Extraction logic only; no HTTP or DB. |
| **frontend/** | Static HTML/JS served at `/` and `/static`. |
| **tests/** | pytest suite for extraction (heuristic + LLM with mocked Ollama). |

---

## 4. Setup Instructions

### Python

- **Python 3.10+** (or 3.9+ with compatible typing).

### Dependencies

Install dependencies (from repo root or `week2`):

```bash
pip install fastapi uvicorn ollama pydantic python-dotenv
```

If the project uses a `requirements.txt` in the repo, use:

```bash
pip install -r requirements.txt
```

### Ollama and model

1. Install and run [Ollama](https://ollama.com).
2. Pull the model used by the app:

```bash
ollama pull llama3.1
```

The app calls `chat(model="llama3.1", ...)` in `app/services/extract.py`.

### Run the FastAPI app

From the **project root** (parent of `week2`), so that `week2` is a package:

```bash
uvicorn week2.app.main:app --reload
```

Or from inside `week2`:

```bash
uvicorn app.main:app --reload
```

### Access the frontend

- Open **http://127.0.0.1:8000/** in a browser.  
- The root URL serves `week2/frontend/index.html`; static assets are under `/static`.

---

## 5. API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| **GET** | `/` | Serves the frontend index page (HTML). |
| **POST** | `/extract_llm` | Extract action items from text using the LLM. Body: `{ "text": "..." }`. Returns `{ "action_items": ["...", ...] }`. |
| **POST** | `/action-items/extract` | Heuristic extraction; optionally save text as a note and link items. Body: `{ "text": "...", "save_note": bool }`. Returns `{ "note_id": int|null, "items": [{ "id", "text" }, ...] }`. |
| **GET** | `/action-items` | List all action items. Query: optional `note_id` to filter by note. |
| **POST** | `/action-items/{action_item_id}/done` | Mark item done or not. Body: `{ "done": bool }`. Returns `{ "id", "done" }`. |
| **POST** | `/notes` | Create a note. Body: `{ "content": "..." }`. Returns note `{ "id", "content", "created_at" }`. |
| **GET** | `/notes` | List all notes (newest first). Returns array of `{ "id", "content", "created_at" }`. |
| **GET** | `/notes/{note_id}` | Get a single note by id. Returns 404 if not found. |

---

## 6. Running Tests

From the **project root** (so that `week2` is importable):

```bash
pytest week2/tests/ -v
```

Or from inside `week2`:

```bash
pytest tests/ -v
```

### What the test suite covers

- **Heuristic extraction** (`extract_action_items`): bullets, checkboxes, numbered list; asserts expected strings in the result.
- **LLM extraction** (`extract_action_items_llm`): all tests **mock** the Ollama `chat` function (patch target: `week2.app.services.extract.chat`) so no real model is called:
  - Valid bullet-style input → multiple action items.
  - Keyword-prefixed input (e.g. `TODO: fix bug`) → single item.
  - Empty/whitespace input → empty list and `chat` is **not** called.
  - Invalid JSON in the mock response → empty list.

---

## 7. Notes on Error Handling

- **LLM extraction** — On empty input, network/API errors, or invalid/malformed JSON from the model, `extract_action_items_llm` returns an **empty list**; it does not raise. The API therefore always returns 200 with `action_items` (possibly empty).
- **HTTP status codes** — Endpoints use standard codes: 400 (e.g. missing `content` or `text`), 404 (note or resource not found), 422 (validation error on request body), 500 (e.g. frontend file missing or note created but not retrievable).
- **Validation** — Request bodies are validated with **Pydantic**; invalid payloads yield 422 with error details. Response shapes are defined by Pydantic models in `app/schemas.py`.
