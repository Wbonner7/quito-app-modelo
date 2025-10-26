from __future__ import annotations

from typing import List

from fastapi import APIRouter, Query

from app.services import recommendations as recommendations_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/properties")
def recommended_properties(limit: int = Query(default=3)) -> List[dict]:
    properties = recommendations_service.recommended_properties(limit=limit)
    return [to_serializable(property_) for property_ in properties]
