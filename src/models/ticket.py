import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class TicketModel(BaseModel):
    __tablename__ = "ticket"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    questions = relationship(
        "QuestionModel",
        secondary="ticket_question",
        back_populates="tickets"
    )

    user = relationship(
        "UserModel",
        back_populates="tickets",
        uselist=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (user_id,),
            ("user.id",),
        )
    )
