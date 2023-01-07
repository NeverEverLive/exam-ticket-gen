import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func, ForeignKeyConstraint
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class TicketQuestionModel(BaseModel):
    __tablename__ = "ticket_question"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    ticket_id = Column(UUID(as_uuid=True), nullable=False)
    question_id = Column(UUID(as_uuid=True), nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (ticket_id,),
            ("ticket.id",),
        ),
        ForeignKeyConstraint(
            (question_id,),
            ("question.id",),
        )
    )
