from fastapi import APIRouter, status, Body
import logic.logic as instituciones_service
from models.models import Institution, InstitutionOut, InstitutionCollection

router = APIRouter()
ENDPOINT_NAME = "/instituciones"

@router.get(
    "/",
    response_description="List all institutions",
    response_model=InstitutionCollection,
    status_code=status.HTTP_200_OK,
)
async def get_institutions():
    return await instituciones_service.get_institutions()

@router.get(
    "/{institution_id}",
    response_description="Get a single institution by its ID",
    response_model=InstitutionOut,
    status_code=status.HTTP_200_OK,
)
async def get_institution(institution_id: str):
    return await instituciones_service.get_institution(institution_id)

@router.post(
    "/",
    response_description="Create a new institution",
    response_model=InstitutionOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_institution(institution: Institution = Body(...)):
    return await instituciones_service.create_institution(institution)

@router.put(
    "/{institution_id}",
    response_description="Update an institution",
    response_model=InstitutionOut,
    status_code=status.HTTP_200_OK,
)
async def update_institution(institution_id: str, institution: Institution = Body(...)):
    return await instituciones_service.update_institution(institution_id, institution)

@router.delete(
    "/{institution_id}",
    response_description="Delete an institution",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_institution(institution_id: str):
    return await instituciones_service.delete_institution(institution_id)
