"""Demo `things` resource.

In-memory CRUD so the scaffolded plugin runs with no DB. Replace with your
own resource(s) backed by whatever store fits — Postgres + SQLAlchemy,
upstream HTTP API, etc. Mirror `martha-scoring/api/routes/rubrics.py` if
you want a SQLAlchemy + version-history reference.
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/things", tags=["things"])


class Thing(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""


_store: dict[str, Thing] = {}


@router.get("", response_model=list[Thing])
def list_things() -> list[Thing]:
    return list(_store.values())


@router.post("", response_model=Thing, status_code=201)
def create_thing(payload: dict[str, Any]) -> Thing:
    thing = Thing(**payload)
    _store[thing.id] = thing
    return thing


@router.get("/{thing_id}", response_model=Thing)
def get_thing(thing_id: str) -> Thing:
    thing = _store.get(thing_id)
    if not thing:
        raise HTTPException(status_code=404, detail="Thing not found")
    return thing


@router.delete("/{thing_id}", status_code=204)
def delete_thing(thing_id: str) -> None:
    if thing_id not in _store:
        raise HTTPException(status_code=404, detail="Thing not found")
    del _store[thing_id]
