
"""
This module contains the logic for the places app.
Main functions:
- get_places: Get a list of all places
- get_place: Get a single place
- create_place: Create a new place
- update_place: Update a place
- delete_place: Delete a place
"""

from models.models import Place, PlaceCollection
from models.db import places_collection
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException


async def get_places():
    """
    Get a list of places
    :return: A list of places
    """
    places = await places_collection.find().to_list(1000)
    return PlaceCollection(places=places)


async def get_place(place_code: str):
    """
    Get a single place
    :param place_code: The code of the place
    :return: The place
    """
    if (place := await places_collection.find_one({"code": place_code})) is not None:
        return place

    raise HTTPException(
        status_code=404, detail=f"Place with code {place_code} not found"
    )


async def create_place(place: Place):
    """
    Insert a new place record.
    """

    try:
        new_place = await places_collection.insert_one(
            place.model_dump(by_alias=True, exclude=["id"])
        )
        created_place = await places_collection.find_one({"_id": new_place.inserted_id})
        return created_place

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail=f"Place with code {place.code} already exists"
        )


async def update_place(place_code: str, place: Place):
    """
    Update a place
    :param place_code: The code of the place
    :param place: The place data
    :return: The updated place
    """

    try:
        update_result = await places_collection.update_one(
            {"code": place_code},
            {"$set": place.model_dump(by_alias=True, exclude=["id"])},
        )
        if update_result.modified_count == 1:
            if (
                updated_place := await places_collection.find_one({"code": place.code})
            ) is not None:
                return updated_place
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail=f"Place with code {place.code} already exists"
        )

    raise HTTPException(
        status_code=404,
        detail=f"Place with code {place_code} not found or no updates were made",
    )


async def delete_place(place_code: str):
    """
    Delete a place
    :param place_code: The code of the place
    """
    delete_result = await places_collection.delete_one({"code": place_code})

    if delete_result.deleted_count == 1:
        return

    raise HTTPException(
        status_code=404, detail=f"Place with code {place_code} not found"
    )
