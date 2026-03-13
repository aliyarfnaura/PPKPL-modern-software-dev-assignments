# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Build & Run

All commands must be run from the `week5/` directory. The project uses Poetry for dependency management (`pyproject.toml` is in the repo root).

```
# Install dependencies (from repo root)
pip install -e .[dev]

# Run the dev server (from week5/)
make run
# equivalent: PYTHONPATH=. uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

The app serves the frontend at `http://localhost:8000` and the Swagger API docs at `http://localhost:8000/docs`.

## Testing

```
make test
# equivalent: PYTHONPATH=. pytest -q backend/tests
```

Run a single test file:
```
PYTHONPATH=. pytest -q backend/tests/test_notes.py
```

Run a single test function:
```
PYTHONPATH=. pytest -q backend/tests/test_notes.py::test_create_and_list_notes
```

Tests use a temporary SQLite database created per-test via the `client` fixture in `backend/tests/conftest.py`. This fixture overrides the FastAPI `get_db` dependency so tests are isolated and don't touch `data/app.db`.

## Linting & Formatting

```
make lint     # ruff check .
make format   # black . && ruff check . --fix
```

Configured in `pyproject.toml`:
- **black**: line-length 100, target Python 3.10–3.12
- **ruff**: line-length 100, enabled rules: E, F, I, UP, B (ignoring E501 and B008)

Pre-commit hooks (`.pre-commit-config.yaml`) run black, ruff --fix, end-of-file-fixer, and trailing-whitespace.

## Architecture

This is a full-stack app with a FastAPI backend + vanilla JS frontend, backed by SQLite via SQLAlchemy.

### Backend (`backend/`)

Layered as:

- **`backend/app/main.py`** — FastAPI app entrypoint. Mounts the static frontend at `/static`, includes routers, and runs DB setup + seeding on startup.
- **`backend/app/models.py`** — SQLAlchemy ORM models (`Note`, `ActionItem`) using `declarative_base()`.
- **`backend/app/schemas.py`** — Pydantic v2 schemas for request/response validation (`NoteCreate`, `NoteRead`, `ActionItemCreate`, `ActionItemRead`). All read models use `from_attributes = True`.
- **`backend/app/db.py`** — Engine, session factory, `get_db()` dependency (yields a session with commit/rollback), and `apply_seed_if_needed()` which runs `data/seed.sql` on first DB creation. DB path is configurable via `DATABASE_PATH` env var (defaults to `./data/app.db`).
- **`backend/app/routers/`** — One router per resource:
  - `notes.py`: `GET /notes/`, `POST /notes/`, `GET /notes/search/?q=`, `GET /notes/{id}`
  - `action_items.py`: `GET /action-items/`, `POST /action-items/`, `PUT /action-items/{id}/complete`
- **`backend/app/services/extract.py`** — Utility that extracts action items from text (lines ending with `!` or starting with `TODO:`).

### Frontend (`frontend/`)

Plain HTML/CSS/JS (no build step). Served as static files by FastAPI. `app.js` calls the backend REST API using `fetch()`. The root route `/` serves `frontend/index.html` directly.

### Data (`data/`)

- `seed.sql` — Creates tables and inserts sample data on first run.
- `app.db` — SQLite database (auto-created, gitignored).

### Key Patterns

- DB sessions are provided to route handlers via FastAPI's `Depends(get_db)`.
- Tests override `get_db` with a temp-DB-backed session factory in `conftest.py`.
- `PYTHONPATH=.` is required for all CLI invocations from `week5/` because the backend package uses relative imports from the `backend` root.
