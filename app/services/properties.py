from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.db.supabase import supabase_db
from app.models.entities import Property, PropertyAnalytics


def list_properties(advertiser_id: Optional[str] = None, status: Optional[str] = None) -> List[Property]:
    properties = list(supabase_db.list_properties())
    if advertiser_id:
        properties = [p for p in properties if p.advertiser_id == advertiser_id]
    if status:
        properties = [p for p in properties if p.status == status]
    return properties


def create_property(data: dict) -> Property:
    property_id = f"prop-{len(list(supabase_db.list_properties())) + 1}"
    if not supabase_db.get_advertiser(data["advertiser_id"]):
        raise ValueError("Anunciante não encontrado")
    property_ = Property(
        id=property_id,
        advertiser_id=data["advertiser_id"],
        title=data["title"],
        description=data["description"],
        price=data["price"],
        address=data["address"],
        bedrooms=data["bedrooms"],
        bathrooms=data["bathrooms"],
        area_m2=data["area_m2"],
        amenities=data.get("amenities", []),
    )
    supabase_db.add_property(property_)
    supabase_db.upsert_analytics(PropertyAnalytics(property_id=property_id))
    return property_


def get_property(property_id: str) -> Optional[Property]:
    return supabase_db.get_property(property_id)


def get_property_analytics(property_id: str) -> Optional[PropertyAnalytics]:
    return supabase_db.get_property_analytics(property_id)


def increment_property_metric(property_id: str, metric: str, amount: int = 1) -> Optional[PropertyAnalytics]:
    analytics = supabase_db.get_property_analytics(property_id)
    if not analytics:
        return None
    if not hasattr(analytics, metric):
        raise ValueError("Métrica inválida")
    current_value = getattr(analytics, metric)
    setattr(analytics, metric, current_value + amount)
    analytics.updated_at = datetime.utcnow()
    return supabase_db.upsert_analytics(analytics)


def top_properties_by_leads(limit: int = 5) -> List[Property]:
    sorted_properties = sorted(
        supabase_db.analytics.values(), key=lambda a: a.leads, reverse=True
    )
    top_ids = [analytics.property_id for analytics in sorted_properties[:limit]]
    return [supabase_db.get_property(prop_id) for prop_id in top_ids if supabase_db.get_property(prop_id)]

