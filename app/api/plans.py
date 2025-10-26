from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.db.supabase import supabase_db
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/")
def list_plans() -> List[dict]:
    return [to_serializable(plan) for plan in supabase_db.list_plans()]
