from fastapi import APIRouter

from views import places_view

API_PREFIX = "/api"
router = APIRouter()

router.include_router(places_view.router, prefix=places_view.ENDPOINT_NAME)
