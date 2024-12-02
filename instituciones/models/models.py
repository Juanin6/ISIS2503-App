# Models for the places microservice

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from models.db import PyObjectId


class PlaceType(str, Enum):
    Classroom = "classroom"
    Laboratory = "laboratory"
    Auditorium = "auditorium"
    Office = "office"


class Place(BaseModel):
    code: str = Field(...)
    capacity: int = Field(...)
    type: PlaceType = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "code": "ML515",
                "capacity": 50,
                "type": PlaceType.Classroom,
            }
        },
    )


class PlaceOut(Place):
    id: PyObjectId = Field(alias="_id", default=None, serialization_alias="id")
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "64b9f1f4f1d2b2a3c4e5f6a7",
                "code": "ML515",
                "capacity": 50,
                "type": PlaceType.Classroom,
            }
        },
    )


class PlaceCollection(BaseModel):
    # A collection of places
    places: List[PlaceOut] = Field(...)
