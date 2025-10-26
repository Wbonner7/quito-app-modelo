from __future__ import annotations
from typing import List

from app.db.supabase import supabase_db
from app.models.entities import Review


def list_reviews(property_id: str) -> List[Review]:
    return [review for review in supabase_db.list_reviews(property_id)]


def create_review(data: dict) -> Review:
    review_id = f"rev-{len(list(supabase_db.list_reviews())) + 1}"
    review = Review(
        id=review_id,
        property_id=data["property_id"],
        rating=data["rating"],
        comment=data.get("comment"),
    )
    return supabase_db.add_review(review)

