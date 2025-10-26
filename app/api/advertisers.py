from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.services import advertisers as advertisers_service
from app.utils.serialization import to_serializable

router = APIRouter()


@router.get("/")
def list_advertisers(advertiser_type: Optional[str] = Query(default=None)) -> List[dict]:
    advertisers = advertisers_service.list_advertisers(advertiser_type)
    return [to_serializable(advertiser) for advertiser in advertisers]


@router.post("/", status_code=201)
def create_advertiser(payload: dict) -> dict:
    try:
        advertiser = advertisers_service.create_advertiser(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return to_serializable(advertiser)


@router.get("/{advertiser_id}")
def get_advertiser(advertiser_id: str) -> dict:
    advertiser = advertisers_service.get_advertiser(advertiser_id)
    if not advertiser:
        raise HTTPException(status_code=404, detail="Anunciante não encontrado")
    return to_serializable(advertiser)
