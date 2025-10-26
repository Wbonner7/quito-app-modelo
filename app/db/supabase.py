from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from app.models.entities import (
    AdvertiserProfile,
    AdvertiserType,
    Plan,
    Property,
    PropertyAnalytics,
    QueueItem,
    Review,
)

_STORAGE_FILE = Path(".supabase_simulator.json")


class SupabaseSimulator:
    """Lightweight persistence layer that emulates Supabase tables."""

    def __init__(self) -> None:
        self.plans: Dict[str, Plan] = {}
        self.advertisers: Dict[str, AdvertiserProfile] = {}
        self.properties: Dict[str, Property] = {}
        self.analytics: Dict[str, PropertyAnalytics] = {}
        self.reviews: Dict[str, Review] = {}
        self.queue: Dict[str, QueueItem] = {}
        self._load()
        if not self.plans:
            self.seed()

    # -- Persistence -----------------------------------------------------
    def _load(self) -> None:
        if not _STORAGE_FILE.exists():
            return
        data = json.loads(_STORAGE_FILE.read_text())
        for plan in data.get("plans", []):
            self.plans[plan["id"]] = Plan(
                id=plan["id"],
                name=plan["name"],
                price=plan["price"],
                description=plan["description"],
                ideal_for=AdvertiserType(plan["ideal_for"]),
                features=plan["features"],
            )
        for advertiser in data.get("advertisers", []):
            advertiser["advertiser_type"] = AdvertiserType(advertiser["advertiser_type"])
            advertiser["created_at"] = _parse_datetime(advertiser.get("created_at"))
            self.advertisers[advertiser["id"]] = AdvertiserProfile(**advertiser)
        for property_ in data.get("properties", []):
            property_["created_at"] = _parse_datetime(property_.get("created_at"))
            self.properties[property_["id"]] = Property(**property_)
        for analytics in data.get("analytics", []):
            analytics["updated_at"] = _parse_datetime(analytics.get("updated_at"))
            self.analytics[analytics["property_id"]] = PropertyAnalytics(**analytics)
        for review in data.get("reviews", []):
            review["created_at"] = _parse_datetime(review.get("created_at"))
            self.reviews[review["id"]] = Review(**review)
        for queue in data.get("queue", []):
            queue["created_at"] = _parse_datetime(queue.get("created_at"))
            self.queue[queue["id"]] = QueueItem(**queue)

    def _persist(self) -> None:
        snapshot = {
            "plans": [self._serialize(plan) for plan in self.plans.values()],
            "advertisers": [self._serialize(adv) for adv in self.advertisers.values()],
            "properties": [self._serialize(prop) for prop in self.properties.values()],
            "analytics": [self._serialize(analytic) for analytic in self.analytics.values()],
            "reviews": [self._serialize(review) for review in self.reviews.values()],
            "queue": [self._serialize(item) for item in self.queue.values()],
        }
        _STORAGE_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))

    @staticmethod
    def _serialize(entity) -> dict:
        data = asdict(entity)
        for key, value in list(data.items()):
            if hasattr(value, "isoformat"):
                data[key] = value.isoformat()
            if isinstance(value, AdvertiserType):
                data[key] = value.value
        return data

    # -- Seed data -------------------------------------------------------
    def seed(self) -> None:
        self.plans = {
            "broker": Plan(
                id="broker",
                name="Corretor",
                price=800,
                description="Plano individual para corretores",
                ideal_for=AdvertiserType.BROKER,
                features=[
                    "Validação automática de CRECI",
                    "Até 30 anúncios ativos",
                    "Analytics com leads e visualizações",
                ],
            ),
            "agency": Plan(
                id="agency",
                name="Imobiliária",
                price=2500,
                description="Plano para imobiliárias com múltiplos corretores",
                ideal_for=AdvertiserType.AGENCY,
                features=[
                    "Gestão de equipe",
                    "Integração com CRM",
                    "Relatórios personalizáveis",
                ],
            ),
            "developer": Plan(
                id="developer",
                name="Incorporadora",
                price=7000,
                description="Plano corporativo para incorporadoras",
                ideal_for=AdvertiserType.DEVELOPER,
                features=[
                    "Campanhas de lançamento",
                    "Analytics por empreendimento",
                    "Suporte dedicado",
                ],
            ),
        }

        advertiser = AdvertiserProfile(
            id="adv-1",
            name="Carla Souza",
            email="carla@example.com",
            advertiser_type=AdvertiserType.BROKER,
            plan_id="broker",
            document="123456",
            document_status="active",
            metadata={"creci": "12345-F"},
        )
        self.advertisers[advertiser.id] = advertiser

        property_ = Property(
            id="prop-1",
            advertiser_id=advertiser.id,
            title="Apartamento moderno no centro",
            description="2 quartos, 2 banheiros, 80m²",
            price=650000,
            address="Rua Principal, 100",
            bedrooms=2,
            bathrooms=2,
            area_m2=80,
            amenities=["Piscina", "Academia"],
        )
        self.properties[property_.id] = property_
        self.analytics[property_.id] = PropertyAnalytics(
            property_id=property_.id,
            views=150,
            leads=12,
            shares=5,
        )

        review = Review(
            id="rev-1",
            property_id=property_.id,
            rating=5,
            comment="Imóvel excelente!",
        )
        self.reviews[review.id] = review

        queue_item = QueueItem(
            id="queue-1",
            advertiser_id=advertiser.id,
            property_id=property_.id,
            status="under_review",
            notes="Verificar documentação complementar",
        )
        self.queue[queue_item.id] = queue_item
        self._persist()

    # -- Query helpers ---------------------------------------------------
    def list_plans(self) -> List[Plan]:
        return list(self.plans.values())

    def add_advertiser(self, advertiser: AdvertiserProfile) -> AdvertiserProfile:
        self.advertisers[advertiser.id] = advertiser
        self._persist()
        return advertiser

    def list_advertisers(self) -> Iterable[AdvertiserProfile]:
        return self.advertisers.values()

    def get_advertiser(self, advertiser_id: str) -> Optional[AdvertiserProfile]:
        return self.advertisers.get(advertiser_id)

    def add_property(self, property_: Property) -> Property:
        self.properties[property_.id] = property_
        if property_.id not in self.analytics:
            self.analytics[property_.id] = PropertyAnalytics(property_id=property_.id)
        self._persist()
        return property_

    def list_properties(self) -> Iterable[Property]:
        return self.properties.values()

    def get_property(self, property_id: str) -> Optional[Property]:
        return self.properties.get(property_id)

    def get_property_analytics(self, property_id: str) -> Optional[PropertyAnalytics]:
        return self.analytics.get(property_id)

    def upsert_analytics(self, analytics: PropertyAnalytics) -> PropertyAnalytics:
        self.analytics[analytics.property_id] = analytics
        self._persist()
        return analytics

    def list_reviews(self, property_id: Optional[str] = None) -> Iterable[Review]:
        reviews = self.reviews.values()
        if property_id:
            reviews = [review for review in reviews if review.property_id == property_id]
        return reviews

    def add_review(self, review: Review) -> Review:
        self.reviews[review.id] = review
        self._persist()
        return review

    def list_queue(self, advertiser_id: Optional[str] = None) -> Iterable[QueueItem]:
        queue_items = self.queue.values()
        if advertiser_id:
            queue_items = [item for item in queue_items if item.advertiser_id == advertiser_id]
        return queue_items

    def add_queue_item(self, item: QueueItem) -> QueueItem:
        self.queue[item.id] = item
        self._persist()
        return item


def _parse_datetime(value):
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    return value

supabase_db = SupabaseSimulator()
