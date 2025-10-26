from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services import properties as properties_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/properties/{property_id}")
def get_property_analytics(property_id: str) -> dict:
    analytics = properties_service.get_property_analytics(property_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics não encontrado")
    return to_serializable(analytics)
