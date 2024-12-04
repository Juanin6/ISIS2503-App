from pydantic import BaseModel, Field , ConfigDict
from typing import List
from models.db import PyObjectId

class Institution(BaseModel):
    course: str = Field(..., example="Mathematics")
    students: List[int] = Field(..., example=[101, 102, 103])

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "course": "10B",
                "students": [101, 102, 103]
            }
        },
    )

class InstitutionOut(Institution):
    id: PyObjectId = Field(alias="_id", default=None, serialization_alias="id")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "64b9f1f4f1d2b2a3c4e5f6a7",
                "course": "Mathematics",
                "students": [101, 102, 103]
            }
        },
    )
class InstitutionCollection(BaseModel):
    institutions: List[InstitutionOut] = Field(...)
