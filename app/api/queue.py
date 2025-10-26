from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from app.services import queue as queue_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/")
def list_queue_items(status: Optional[str] = Query(default=None)) -> List[dict]:
    return [to_serializable(item) for item in queue_service.list_queue_items(status)]


@router.post("/", status_code=201)
def create_queue_item(payload: dict) -> dict:
    item = queue_service.create_queue_item(payload)
    return to_serializable(item)
