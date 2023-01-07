import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func, ForeignKeyConstraint
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class QuestionModuleModel(BaseModel):
    __tablename__ = "question_module"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    question_id = Column(UUID(as_uuid=True), nullable=False)
    module_id = Column(UUID(as_uuid=True), nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (module_id,),
            ("module.id",),
        ),
        ForeignKeyConstraint(
            (question_id,),
            ("question.id",),
        )
    )
