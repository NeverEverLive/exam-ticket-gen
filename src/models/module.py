import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class ModuleModel(BaseModel):
    __tablename__ = "module"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    subject_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    questions = relationship(
        "QuestionModel",
        secondary="question_module",
        back_populates="modules",
    )

    subject = relationship(
        "SubjectModel",
        back_populates="modules",
        uselist=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (subject_id,),
            ("subject.id",),
        ),
    )
