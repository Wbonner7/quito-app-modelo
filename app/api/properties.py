from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.services import properties as properties_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/")
def list_properties(
    advertiser_id: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
) -> List[dict]:
    properties = properties_service.list_properties(advertiser_id, status)
    return [to_serializable(property_) for property_ in properties]


@router.post("/", status_code=201)
def create_property(payload: dict) -> dict:
    try:
        property_ = properties_service.create_property(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return to_serializable(property_)


@router.get("/{property_id}")
def get_property(property_id: str) -> dict:
    property_ = properties_service.get_property(property_id)
    if not property_:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    analytics = properties_service.get_property_analytics(property_id)
    if not analytics:
        analytics = properties_service.increment_property_metric(property_id, "views", 0)
    response = to_serializable(property_)
    response["analytics"] = to_serializable(analytics) if analytics else None
    return response


@router.post("/{property_id}/metrics/{metric}", status_code=200)
def increment_metric(property_id: str, metric: str) -> dict:
    try:
        analytics = properties_service.increment_property_metric(property_id, metric)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics não encontrado")
    return to_serializable(analytics)
