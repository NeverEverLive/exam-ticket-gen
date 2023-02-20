
import logging
from pydantic import parse_obj_as
from sqlalchemy import select, update, delete

from src.models.base import get_async_session
from src.models.question import QuestionModel
from src.components.question.schemas import QuestionResponse, QuestionSchema, QuestionsResponse


async def create_question(question: QuestionSchema) -> QuestionResponse:
    question_state = QuestionModel().fill(**question.dict())

    async with get_async_session() as session:
        session.add(question_state)
        await session.commit()

    return QuestionResponse(
        question=question,
        message="Question successfully created",
        success=True
    )


async def get_questions() -> QuestionsResponse:
    question_state = select(
        QuestionModel.id,
        QuestionModel.module_id,
        QuestionModel.user_id,
        QuestionModel.text,
        QuestionModel.probability,
    )

    async with get_async_session() as session:
        logging.warning((await session.execute(question_state)).fetchall())
        return QuestionsResponse(
            questions=parse_obj_as(list[QuestionSchema], (await session.execute(question_state)).fetchall()),
            message="Question collected successfully",
            success=True
        )


async def get_question(id: str) -> QuestionResponse:
    question_state = select(
        QuestionModel.id,
        QuestionModel.module_id,
        QuestionModel.user_id,
        QuestionModel.text,
        QuestionModel.probability,
    ).where(
        QuestionModel.id == id
    )

    async with get_async_session() as session:
        logging.warning(QuestionSchema.from_orm((await session.execute(question_state)).fetchone()))
        return QuestionResponse(
            question=QuestionSchema.from_orm((await session.execute(question_state)).fetchone()),
            message="Question successfully taken",
            success=True
        )


async def update_question(question: QuestionSchema) -> QuestionResponse:
    question_state = update(
        QuestionModel
    ).where(
        QuestionModel.id == question.id
    ).values(
        **question.dict()
    )

    async with get_async_session() as session:
        await session.execute(question_state)
        await session.commit()

    return QuestionResponse(
        question=question,
        message="Question successfully updated",
        success=True
    )


async def delete_question(id: str) -> QuestionResponse:
    question_state = delete(
        QuestionModel
    ).where(
        QuestionModel.id == id
    )

    async with get_async_session() as session:
        await session.execute(question_state)
        await session.commit()

    return QuestionResponse(
        message="Question successfully deleted",
        success=True
    )
