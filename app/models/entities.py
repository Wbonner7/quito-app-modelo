from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class AdvertiserType(str, Enum):
    BROKER = "broker"
    AGENCY = "agency"
    DEVELOPER = "developer"


@dataclass
class Plan:
    id: str
    name: str
    price: float
    description: str
    ideal_for: AdvertiserType
    features: List[str]


@dataclass
class AdvertiserProfile:
    id: str
    name: str
    email: str
    advertiser_type: AdvertiserType
    plan_id: str
    document: str
    document_status: str
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Property:
    id: str
    advertiser_id: str
    title: str
    description: str
    price: float
    address: str
    bedrooms: int
    bathrooms: int
    area_m2: float
    amenities: List[str]
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PropertyAnalytics:
    property_id: str
    views: int = 0
    leads: int = 0
    shares: int = 0
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Review:
    id: str
    property_id: str
    rating: int
    comment: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class QueueItem:
    id: str
    advertiser_id: str
    property_id: Optional[str]
    status: str
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

