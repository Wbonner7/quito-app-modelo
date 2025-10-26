from __future__ import annotations

from typing import List, Optional

from app.db.supabase import supabase_db
from app.models.entities import QueueItem


def list_queue_items(status: Optional[str] = None) -> List[QueueItem]:
    items = list(supabase_db.list_queue())
    if status:
        items = [item for item in items if item.status == status]
    return items


def create_queue_item(data: dict) -> QueueItem:
    queue_id = f"queue-{len(list(supabase_db.list_queue())) + 1}"
    item = QueueItem(
        id=queue_id,
        advertiser_id=data["advertiser_id"],
        property_id=data.get("property_id"),
        status=data["status"],
        notes=data.get("notes"),
    )
    return supabase_db.add_queue_item(item)

