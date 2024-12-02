from fastapi import APIRouter, status, Body
import logic.places_logic as places_service
from models.models import Place, PlaceOut, PlaceCollection

router = APIRouter()
ENDPOINT_NAME = "/places"


@router.get(
    "/",
    response_description="List all places",
    response_model=PlaceCollection,
    status_code=status.HTTP_200_OK,
)
async def get_places():
    return await places_service.get_places()


@router.get(
    "/{place_code}",
    response_description="Get a single place by its code",
    response_model=PlaceOut,
    status_code=status.HTTP_200_OK,
)
async def get_place(place_code: str):
    return await places_service.get_place(place_code)


@router.post(
    "/",
    response_description="Create a new place",
    response_model=PlaceOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_place(place: Place = Body(...)):
    return await places_service.create_place(place)


@router.put(
    "/{place_code}",
    response_description="Update a place",
    response_model=PlaceOut,
    status_code=status.HTTP_200_OK,
)
async def update_place(place_code: str, place: Place = Body(...)):
    return await places_service.update_place(place_code, place)


@router.delete(
    "/{place_code}",
    response_description="Delete a place",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_place(place_code: str):
    return await places_service.delete_place(place_code)
