from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from .. import db
from ..schemas import (
    ActionItemResponse,
    ExtractActionItemsRequest,
    ExtractActionItemsResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    """Extract action items from text using heuristic rules; optionally save text as a note and link items."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractActionItemsResponse(
        note_id=note_id,
        items=[{"id": i, "text": t} for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemResponse])
def list_all(
    note_id: Optional[int] = Query(None, description="Filter by note id"),
) -> list[ActionItemResponse]:
    """List action items, optionally filtered by note_id."""
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    """Mark an action item as done or not done."""
    done = payload.done
    db.mark_action_item_done(action_item_id, done)
    return MarkDoneResponse(id=action_item_id, done=done)


