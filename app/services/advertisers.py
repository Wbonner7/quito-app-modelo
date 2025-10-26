from __future__ import annotations
from typing import List, Optional

from app.db.supabase import supabase_db
from app.models.entities import AdvertiserProfile, AdvertiserType
from app.services.validation import validate_advertiser_payload


def list_advertisers(advertiser_type: Optional[str] = None) -> List[AdvertiserProfile]:
    advertisers = list(supabase_db.list_advertisers())
    if advertiser_type:
        advertisers = [
            adv for adv in advertisers if adv.advertiser_type.value == advertiser_type
        ]
    return advertisers


def create_advertiser(data: dict) -> AdvertiserProfile:
    validate_advertiser_payload(data)
    advertiser_id = f"adv-{len(list(supabase_db.list_advertisers())) + 1}"
    if data["plan_id"] not in {plan.id for plan in supabase_db.list_plans()}:
        raise ValueError("Plano informado é inválido")

    advertiser = AdvertiserProfile(
        id=advertiser_id,
        name=data["name"],
        email=data["email"],
        advertiser_type=AdvertiserType(data["advertiser_type"]),
        plan_id=data["plan_id"],
        document=data["document"],
        document_status=data["document_status"],
        metadata=data.get("metadata", {}),
    )
    return supabase_db.add_advertiser(advertiser)


def get_advertiser(advertiser_id: str) -> Optional[AdvertiserProfile]:
    return supabase_db.get_advertiser(advertiser_id)

