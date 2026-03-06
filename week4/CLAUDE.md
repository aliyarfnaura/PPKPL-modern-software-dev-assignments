# Claude Code Automation Setup

This repository contains a starter application for the "Week 4 — The Autonomous Coding Agent IRL" assignment.

## Project Structure

```
assignment.md          # Assignment instructions
Makefile              # Build automation
pre-commit-config.yaml # Pre-commit hooks
writeup.md            # Assignment writeup
backend/              # FastAPI application
├── app/
│   ├── main.py       # FastAPI app entry point
│   ├── db.py         # Database configuration
│   ├── models.py     # SQLAlchemy models
│   ├── schemas.py    # Pydantic schemas
│   ├── routers/      # API route handlers
│   │   ├── notes.py
│   │   └── action_items.py
│   └── services/     # Business logic
├── tests/            # pytest test files
frontend/             # Static UI files
├── index.html
├── styles.css
└── app.js
data/                 # SQLite database files
docs/                 # Documentation
.claude/              # Claude automations
└── commands/
    ├── run-tests.md  # Test automation
    └── fix-code.md   # Code quality automation
```

## How to Run the App

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```bash
   cd backend && uvicorn app.main:app --reload
   ```

3. **Access the application:**
   - Frontend: http://localhost:8000
   - API docs: http://localhost:8000/docs

## API Structure

- **Routers:** Located in `backend/app/routers/`
  - `notes.py` - Note management endpoints
  - `action_items.py` - Action item management endpoints

- **Tests:** Located in `backend/tests/`
  - `test_notes.py` - Tests for note functionality
  - `test_action_items.py` - Tests for action item functionality
  - `test_extract.py` - Tests for extraction services

## Developer Workflow

1. **Write Tests First:** Create or update tests in `backend/tests/`
2. **Run Tests:** Use `/run-tests` to execute the test suite
3. **Implement Code:** Make changes to the application code
4. **Fix Code Quality:** Use `/fix-code` to format and lint the code
5. **Commit:** Ensure all tests pass and code is properly formatted

## Claude Automations

This project includes two Claude Code automations:

### `/run-tests`
Runs the pytest test suite and summarizes results. This ensures code changes don't break existing functionality.

### `/fix-code`
Runs `black` for code formatting and `ruff` for linting with automatic fixes. This maintains consistent code style and catches potential issues.

## Technologies Used

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database engine
- **pytest** - Testing framework
- **black** - Code formatter
- **ruff** - Fast Python linter