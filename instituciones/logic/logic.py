from models.models import Institution, InstitutionCollection
from models.db import instituciones_collection
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
import httpx

async def student_exists(student_id: int) -> bool:
    """
    Verifica si el estudiante con el ID proporcionado existe.
    :param student_id: El ID del estudiante
    :return: True si el estudiante existe, False si no.
    """
    url = f"http://10.128.0.15:8080/api/usuario/{student_id}/"
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            # Si la respuesta es correcta y contiene 'true' en el JSON
            return True
        else:
            return False

async def get_institutions():
    """
    Get a list of institutions
    :return: A list of institutions
    """
    institutions = await instituciones_collection.find().to_list(1000)
    return InstitutionCollection(institutions=institutions)


async def get_institution(course_name: str):
    """
    Get a single institution by course name
    :param course_name: The course of the institution
    :return: The institution
    """
    if (institution := await instituciones_collection.find_one({"course": course_name})) is not None:
        return institution

    raise HTTPException(
        status_code=404, detail=f"Institution with course {course_name} not found"
    )


async def create_institution(institution: Institution):
    """
    Inserta un nuevo registro de institución, validando que todos los estudiantes existan.
    """

    # Verificar que todos los estudiantes existen
    for student_id in institution.students:
        exists = await student_exists(student_id)
        if not exists:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} does not exist."
            )

    try:
        # Si todos los estudiantes existen, procedemos a crear la institución
        if not institution.students:
            institution.students = []  # Si no se proveen estudiantes, asignamos una lista vacía

        new_institution = await instituciones_collection.insert_one(
            institution.model_dump(by_alias=True, exclude=["id"])
        )
        
        created_institution = await instituciones_collection.find_one({"_id": new_institution.inserted_id})
        return created_institution

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail=f"Institution with course {institution.course} already exists"
        )

async def update_institution(course_name: str, institution: Institution):
    """
    Update an institution
    :param course_name: The course of the institution
    :param institution: The institution data
    :return: The updated institution
    """

    try:
        update_result = await instituciones_collection.update_one(
            {"course": course_name},
            {"$set": institution.model_dump(by_alias=True, exclude=["id"])}
        )
        if update_result.modified_count == 1:
            if (
                updated_institution := await instituciones_collection.find_one({"course": institution.course})
            ) is not None:
                return updated_institution
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail=f"Institution with course {institution.course} already exists"
        )

    raise HTTPException(
        status_code=404,
        detail=f"Institution with course {course_name} not found or no updates were made",
    )


async def delete_institution(course_name: str):
    """
    Delete an institution by course name
    :param course_name: The course of the institution
    """
    delete_result = await instituciones_collection.delete_one({"course": course_name})

    if delete_result.deleted_count == 1:
        return

    raise HTTPException(
        status_code=404, detail=f"Institution with course {course_name} not found"
    )
