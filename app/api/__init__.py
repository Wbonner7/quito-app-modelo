from fastapi import APIRouter

from app.api import plans, advertisers, properties, analytics, reviews, queue, recommendations

router = APIRouter()

router.include_router(plans.router, prefix="/plans", tags=["plans"])
router.include_router(advertisers.router, prefix="/advertisers", tags=["advertisers"])
router.include_router(properties.router, prefix="/properties", tags=["properties"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
router.include_router(queue.router, prefix="/queue", tags=["queue"])
router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
