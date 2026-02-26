"""
Pydantic models for API request and response contracts.
Ensures consistent types and documentation across endpoints.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ----- Notes -----


class CreateNoteRequest(BaseModel):
    """Request body for POST /notes."""

    content: str = Field(..., description="Note content.")


class NoteResponse(BaseModel):
    """Response for a single note (create or get)."""

    id: int
    content: str
    created_at: str


# ----- Action items -----


class ExtractActionItemsRequest(BaseModel):
    """Request body for POST /action-items/extract."""

    text: str = Field(..., description="Raw text to extract action items from.")
    save_note: bool = Field(default=False, description="If true, save text as a note and link items to it.")


class ActionItemSummary(BaseModel):
    """Action item with id and text (e.g. in extract response)."""

    id: int
    text: str


class ExtractActionItemsResponse(BaseModel):
    """Response for POST /action-items/extract."""

    note_id: Optional[int] = None
    items: list[ActionItemSummary]


class ActionItemResponse(BaseModel):
    """Full action item as returned by GET /action-items."""

    id: int
    note_id: Optional[int] = None
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    """Request body for POST /action-items/{id}/done."""

    done: bool = Field(default=True, description="Whether the item is marked done.")


class MarkDoneResponse(BaseModel):
    """Response for POST /action-items/{id}/done."""

    id: int
    done: bool


# ----- Extract LLM (root endpoint) -----


class ExtractLLMRequest(BaseModel):
    """Request body for POST /extract_llm."""

    text: str = Field(..., description="Raw text to extract action items from.")


class ExtractLLMResponse(BaseModel):
    """Response for POST /extract_llm."""

    action_items: list[str] = Field(..., description="Extracted action items from the LLM.")
