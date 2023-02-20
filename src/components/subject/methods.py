
import logging
from pydantic import parse_obj_as
from sqlalchemy import select, update, delete

from src.models.base import get_async_session
from src.models.subject import SubjectModel
from src.components.subject.schemas import SubjectSchema, SubjectResponse, SubjectsResponse


async def create_subject(subject: SubjectSchema) -> SubjectResponse:
    subject_state = SubjectModel().fill(**subject.dict())

    async with get_async_session() as session:
        session.add(subject_state)
        await session.commit()

    return SubjectResponse(
        subject=subject,
        message="Subject successfully created",
        success=True
    )

async def get_subjects() -> SubjectsResponse:
    subject_state = select(
        SubjectModel.id,
        SubjectModel.name,
        SubjectModel.description,
    )

    async with get_async_session() as session:
        return SubjectsResponse(
            subjects=parse_obj_as(list[SubjectSchema], (await session.execute(subject_state)).fetchall()),
            message="Subject collected successfully",
            success=True
        )


async def get_subject(id: str) -> SubjectResponse:
    subject_state = select(
        SubjectModel.id,
        SubjectModel.name,
        SubjectModel.description,
    ).where(
        SubjectModel.id == id
    )

    async with get_async_session() as session:
        logging.warning(SubjectSchema.from_orm((await session.execute(subject_state)).fetchone()))
        return SubjectResponse(
            subject=SubjectSchema.from_orm((await session.execute(subject_state)).fetchone()),
            message="Subject successfully taken",
            success=True
        )


async def update_subject(subject: SubjectSchema) -> SubjectResponse:
    subject_state = update(
        SubjectModel
    ).where(
        SubjectModel.id == subject.id
    ).values(
        **subject.dict()
    )

    async with get_async_session() as session:
        await session.execute(subject_state)
        await session.commit()

    return SubjectResponse(
        subject=subject,
        message="Subject successfully updated",
        success=True
    )


async def delete_subject(id: str) -> SubjectResponse:
    subject_state = delete(
        SubjectModel
    ).where(
        SubjectModel.id == id
    )

    async with get_async_session() as session:
        await session.execute(subject_state)
        await session.commit()

    return SubjectResponse(
        message="Subject successfully deleted",
        success=True
    )
