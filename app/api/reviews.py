from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.services import reviews as reviews_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/property/{property_id}")
def list_reviews(property_id: str) -> List[dict]:
    return [to_serializable(review) for review in reviews_service.list_reviews(property_id)]


@router.post("/", status_code=201)
def create_review(payload: dict) -> dict:
    review = reviews_service.create_review(payload)
    return to_serializable(review)
