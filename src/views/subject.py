import logging
from fastapi import APIRouter, Query, Depends

from src.components.subject.schemas import SubjectSchema, SubjectResponse, SubjectsResponse
from src.components.subject.methods import create_subject, get_subject, get_subjects, update_subject, delete_subject
from src.components.authentication.jwt import JWTBearer


router = APIRouter(prefix="/subject")


@router.post("/", response_model=SubjectResponse, status_code=201)
async def create_subject_endpoint(subject: SubjectSchema):
    logging.warning(subject)
    return await create_subject(subject)

@router.get("/", response_model=SubjectsResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subjects_endpoint():
    return await get_subjects()


@router.get("/detail", response_model=SubjectResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id", default=None)):
    return await get_subject(subject_id)


@router.put("/", response_model=SubjectResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject: SubjectSchema):
    return await update_subject(subject)


@router.delete("/", response_model=SubjectResponse, status_code=202, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id")):
    return await delete_subject(subject_id)
