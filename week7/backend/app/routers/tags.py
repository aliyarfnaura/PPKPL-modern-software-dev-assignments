from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, Tag
from ..schemas import NoteRead, TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagRead])
def list_tags(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[TagRead]:
    stmt = select(Tag)

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Tag, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Tag, sort_field)))
    else:
        stmt = stmt.order_by(desc(Tag.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [TagRead.model_validate(row) for row in rows]


@router.post("/", response_model=TagRead, status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    existing = db.execute(select(Tag).where(Tag.name == payload.name)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Tag already exists")
    tag = Tag(name=payload.name)
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return TagRead.model_validate(tag)


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagRead:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagRead.model_validate(tag)


@router.post("/{tag_id}/notes/{note_id}", response_model=NoteRead, status_code=200)
def add_tag_to_note(
    tag_id: int, note_id: int, db: Session = Depends(get_db)
) -> NoteRead:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if tag not in note.tags:
        note.tags.append(tag)
        db.flush()
        db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{tag_id}/notes/{note_id}", response_model=NoteRead, status_code=200)
def remove_tag_from_note(
    tag_id: int, note_id: int, db: Session = Depends(get_db)
) -> NoteRead:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if tag in note.tags:
        note.tags.remove(tag)
        db.flush()
        db.refresh(note)
    return NoteRead.model_validate(note)
