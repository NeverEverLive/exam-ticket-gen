import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import Integer
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class QuestionModel(BaseModel):
    __tablename__ = "question"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    module_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(String, nullable=False)
    probability = Column(Integer, nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    module = relationship(
        "ModuleModel",
        back_populates="questions",
        uselist=False
    )

    tickets = relationship(
        "TicketModel",
        secondary="ticket_question",
        back_populates="questions"
    )

    user = relationship(
        "UserModel",
        back_populates="questions",
        uselist=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (user_id,),
            ("user.id",),
        ),
        ForeignKeyConstraint(
            (module_id,),
            ("module.id",),
        )
    )
