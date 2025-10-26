from __future__ import annotations

from typing import List

from app.models.entities import Property
from app.services.properties import top_properties_by_leads


def recommended_properties(limit: int = 3) -> List[Property]:
    return top_properties_by_leads(limit=limit)

