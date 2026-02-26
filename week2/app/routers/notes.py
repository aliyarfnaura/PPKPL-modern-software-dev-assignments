from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import CreateNoteRequest, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteResponse])
def list_all_notes() -> list[NoteResponse]:
    """Return all notes, newest first."""
    rows = db.list_notes()
    return [NoteResponse(id=r["id"], content=r["content"], created_at=r["created_at"]) for r in rows]


@router.post("", response_model=NoteResponse)
def create_note(payload: CreateNoteRequest) -> NoteResponse:
    """Create a new note. Returns the created note with id and created_at."""
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=500, detail="Note created but could not be retrieved")
    return NoteResponse(id=note["id"], content=note["content"], created_at=note["created_at"])


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Get a note by id. Returns 404 if not found."""
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(id=row["id"], content=row["content"], created_at=row["created_at"])


