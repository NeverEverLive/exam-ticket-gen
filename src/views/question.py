import logging
from fastapi import APIRouter, Query, Depends, Request

from src.components.question.schemas import QuestionResponse, QuestionSchema, QuestionsResponse
from src.components.question.methods import create_question, get_question, get_questions, update_question, delete_question
from src.components.authentication.jwt import JWTBearer


router = APIRouter(prefix="/question")


@router.post("/", response_model=QuestionResponse, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_subject_endpoint(subject: QuestionSchema, request: Request):
    subject.user_id = request.state.user_id
    return await create_question(subject)

@router.get("/", response_model=QuestionsResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subjects_endpoint():
    return await get_questions()


@router.get("/detail", response_model=QuestionResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id", default=None)):
    return await get_question(subject_id)


@router.put("/", response_model=QuestionResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject: QuestionSchema):
    return await update_question(subject)


@router.delete("/", response_model=QuestionResponse, status_code=202, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id")):
    return await delete_question(subject_id)
