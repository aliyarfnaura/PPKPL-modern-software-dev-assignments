# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Aliya Raffa Naura Ayu**\
SUNet ID: **N/A** \
Citations: **N/A**

This assignment took me about **4** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement an LLM-powered alternative for action item extraction in the Week 2 FastAPI app.

Tasks:

1. In week2/app/services/extract.py:

Implement a new function:
def extract_action_items_llm(text: str) -> List[str]

- Use Ollama via from ollama import chat
- Use model "llama3.1"
- Send a system prompt instructing the model to extract action items
- Return ONLY a JSON array of strings (structured output)
- Use format="json" in the chat() call
- Safely parse the JSON using json.loads
- If parsing fails, return an empty list
- Do NOT modify the existing extract_action_items() heuristic function

2. In week2/app/main.py:

- Add a new FastAPI endpoint:
POST /extract_llm
- Accept a JSON body with a "text" field
- Call extract_action_items_llm
- Return the extracted action items as JSON
- Do not modify existing endpoints

Keep code style consistent with the existing project.
```

Generated Code Snippets:
```
File modified: week2/app/services/extract.py

Added:
- import: json (around line 6)
- import: from ollama import chat (around line 8)
- function: extract_action_items_llm(text: str) -> List[str] (around lines 92–122)

File modified: week2/app/main.py

Added:
- import: from pydantic import BaseModel (around line 9)
- import: from .services.extract import extract_action_items_llm (around line 14)
- class ExtractLLMRequest (around lines 26–27)
- POST /extract_llm endpoint (around lines 30–34)
```

### Exercise 2: Add Unit Tests
Prompt: 
```
In week2/tests/test_extract.py, write unit tests for extract_action_items_llm().

Project structure:
- extract_action_items_llm is defined in:
  week2/app/services/extract.py
- That file imports Ollama using:
  from ollama import chat

Requirements:
- Use pytest
- Use unittest.mock.patch to mock the Ollama `chat` function
- IMPORTANT: Patch the correct module path:
  "week2.app.services.extract.chat"
- Do NOT call the real Ollama model
- Do NOT modify any application code
- Keep tests clean, readable, and deterministic

Test cases to cover:
1. Valid bullet-style input returning multiple action items
2. Keyword-prefixed input (e.g., "TODO: fix bug")
3. Empty input (should return empty list without calling chat)
4. Invalid JSON response from the model (should return empty list)

Additional expectations:
- Use mock_chat.assert_called_once() where appropriate
- Ensure empty input does NOT call chat
- Keep the test file organized and easy to read
``` 

Generated Code Snippets:
```
File created: week2/tests/test_extract.py

Added:
- import pytest (around line 1)
- import from unittest.mock import patch (around line 2)
- import extract_action_items and extract_action_items_llm (around line 4)
- constant: CHAT_PATCH = "week2.app.services.extract.chat" (around line 24)

Test cases:
- test_extract_bullets_and_checkboxes() (around lines 7–20)
- test_extract_llm_valid_bullet_style() (around lines 27–36)
- test_extract_llm_keyword_prefix() (around lines 39–48)
- test_extract_llm_empty_input() (around lines 51–57)
- test_extract_llm_invalid_json_returns_empty_list() (around lines 60–69)

Mocking:
- Patched Ollama chat using @patch("week2.app.services.extract.chat")
- Used mock_chat.assert_called_once() and mock_chat.assert_not_called()
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Perform a refactor of the backend code in the Week 2 FastAPI project to improve clarity, structure, and maintainability.

IMPORTANT CONSTRAINTS:
- Do NOT change existing functionality or behavior.
- Do NOT remove any existing endpoints.
- Do NOT modify business logic.
- Keep the application fully working.
- Focus only on improving structure and clarity.

Refactor goals:

1. API Contracts / Schemas:
   - Add explicit response models to FastAPI endpoints where appropriate.
   - Ensure request/response types are clearly defined using Pydantic models.
   - Add type hints consistently across functions.
   - Improve docstrings for public functions and endpoints.

2. Database Layer Cleanup:
   - Ensure database access is clearly separated from business logic.
   - Remove unused imports.
   - Improve function naming for clarity (if needed).
   - Add type annotations where missing.

3. App Lifecycle / Configuration:
   - Improve application initialization clarity.
   - Ensure init_db() is clearly placed and documented.
   - Move configuration-related logic into clearly defined sections.
   - Add explanatory comments where helpful.

4. Error Handling:
   - Add explicit error handling in API endpoints where needed.
   - Use HTTPException with proper status codes if applicable.
   - Avoid silent failures.
   - Ensure LLM-related errors are handled clearly.

Additional instructions:
- Keep code style consistent with the project.
- Do not introduce unnecessary complexity.
- Do not rewrite large sections unless necessary.
- Refactor incrementally and explain what was improved.

After refactoring:
- Clearly list all modified files.
- Highlight the specific changes made.
- Keep changes readable and minimal.
``` 

Generated/Modified Code Snippets:
```
File created: week2/app/schemas.py

Added:
- Pydantic models for API contracts:
  - CreateNoteRequest
  - NoteResponse
  - ExtractActionItemsRequest
  - ExtractActionItemsResponse
  - ActionItemResponse
  - ActionItemSummary
  - MarkDoneRequest
  - MarkDoneResponse
  - ExtractLLMRequest
  - ExtractLLMResponse
(Full file; around lines 1–XX)

File modified: week2/app/main.py

Changes:
- Added module-level docstring explaining app lifecycle (around lines 1–10)
- Added section comments:
  - Configuration & lifecycle
  - Root & static
  - Extract LLM endpoint
  - Routers
- Added response_model=ExtractLLMResponse to POST /extract_llm (around lines XX–XX)
- Updated extract_llm return type to ExtractLLMResponse
- Added explicit HTTPException(500, "Frontend index not found") in index() (around lines XX–XX)
- Improved endpoint docstrings

File modified: week2/app/db.py

Changes:
- Added module-level docstring (around lines 1–5)
- Added section comments separating Notes and Action Items logic
- Added one-line docstrings to all public DB functions
- No logic or database schema changes

File modified: week2/app/routers/notes.py

Changes:
- Replaced inline dict bodies with Pydantic request models (around lines XX–XX)
- Added response_model=NoteResponse to endpoints
- Added docstrings to endpoints
- Added explicit HTTPException(500, "Note created but could not be retrieved")
  if get_note(note_id) returns None after create (around lines XX–XX)
- Ensured consistent error handling (400/404 unchanged)

File modified: week2/app/routers/action_items.py

Changes:
- Added request/response schemas from app.schemas
- Added response_model declarations to endpoints
- Replaced raw note_id parameters with Query(...) where appropriate
- Added endpoint docstrings
- Improved type hints for clarity

File modified: week2/app/services/extract.py

Changes:
- Added module-level docstring (around lines 1–5)
- Removed unused imports (os, Any)
- Added docstring to extract_action_items_llm()
- Clarified error handling behavior in except block (comment explaining return [])
- No changes to extraction logic or return behavior
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Automate small frontend/backend integration tasks using agentic mode.

Tasks:

1. Integrate the LLM-powered extraction endpoint into the frontend:
   - The backend already exposes POST /extract_llm.
   - Update the frontend (week2/frontend/index.html and related JS) to:
     - Add a button labeled "Extract LLM"
     - When clicked:
       - Read the text input area
       - Send a POST request to /extract_llm
       - Display the returned action_items list in the UI
   - Handle errors gracefully (display message if request fails)
   - Do not remove or break existing extraction functionality.

2. Expose a new endpoint to retrieve all notes:
   - Add a GET endpoint in the backend (e.g., GET /notes/all or GET /notes)
   - Return a list of notes using an appropriate response model
   - Do not modify existing endpoints

3. Update the frontend:
   - Add a button labeled "List Notes"
   - When clicked:
       - Fetch all notes from the new endpoint
       - Render them clearly in the UI
   - Ensure the UI updates without refreshing the page

Constraints:
- Do not change existing routes or logic.
- Keep styling and structure consistent.
- Keep JavaScript clean and readable.
- Add comments explaining the new logic.
- Only modify necessary files.
- Clearly list modified files at the end.
``` 

Generated Code Snippets:
```
File modified: week2/app/routers/notes.py

Added:
- import: CreateNoteRequest, NoteResponse from ..schemas (around lines 5–6)
- New endpoint: (around lines 10–15)

Details:
- Uses existing db.list_notes()
- Maps DB rows to NoteResponse instances
- Registered BEFORE @router.get("/{note_id}") to prevent route shadowing
- Added explicit docstring for clarity

File modified: week2/frontend/index.html

Added (CSS improvements):
- .section-title styling (around lines 15–16)
- .notes-list styling (around line 17)
- .note-card styling (around lines 18–20)

Added (HTML structure):
- "Extract LLM" button (line 34)
- "Notes" section header <h2 class="section-title"> (line 39)
- "List Notes" button (line 41)
- <div id="notes_list"> container (line 43)

Added (JavaScript):

LLM extraction integration:
- Section comment: // ----- LLM extraction ----- (line 93)
- Button selector: const btnLlm = $('#extract_llm'); (line 94)
- Event listener for POST /extract_llm (lines 95–120)
  - Sends { text } to backend
  - Displays data.action_items in #items
  - Handles empty result
  - Shows error message on failure

List notes integration:
- Section comment: // ----- List notes ----- (line 122)
- Button selector: const btnListNotes = $('#list_notes'); (line 123)
- Event listener for GET /notes (lines 124–149)
  - Shows "Loading..."
  - Renders notes into #notes_list
  - Displays "No notes yet."
  - Handles errors gracefully

Utility function:
- escapeHtml() helper for safe rendering (lines 151–155)
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the entire Week 2 FastAPI codebase and generate a well-structured README.md file at the root of the week2 directory.

The README must include:

1. Project Overview
   - Brief explanation of what the application does
   - Mention both heuristic and LLM-based action item extraction

2. Features
   - Heuristic action item extraction
   - LLM-powered extraction via Ollama
   - Note creation and retrieval
   - Action item completion
   - Frontend integration (Extract, Extract LLM, List Notes)

3. Project Structure
   - Describe main folders (app/, routers/, services/, tests/, frontend/)
   - Brief explanation of what each module does

4. Setup Instructions
   - Python version requirement
   - How to install dependencies
   - How to run Ollama and pull llama3.1
   - How to start the FastAPI app
   - How to access the frontend

5. API Endpoints
   - List all endpoints with method + path + short description
   - Include:
       GET /
       POST /extract_llm
       POST /action-items/extract
       POST /action-items/{id}/done
       POST /notes
       GET /notes
       GET /notes/{note_id}

6. Running Tests
   - How to run pytest
   - What the test suite covers (LLM mocking, heuristic extraction)

7. Notes on Error Handling
   - LLM errors return empty list
   - Proper HTTP status codes
   - Validation via Pydantic

Constraints:
- Do not invent features that do not exist.
- Keep documentation accurate to the current codebase.
- Use clean Markdown formatting with headings.
- Keep tone professional and concise.
- Generate the full README content.
``` 

Generated Code Snippets:
```
File created: week2/README.md

Added:
- Project overview section (lines 1–20)
- Features section (lines 22–34)
- Project structure section with directory tree and table (lines 36–74)
- Setup instructions (lines 76–124)
- API endpoints table (lines 126–160)
- Running tests section (lines 162–188)
- Error handling notes (lines 190–208)

(Full file; lines 1–208)
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 