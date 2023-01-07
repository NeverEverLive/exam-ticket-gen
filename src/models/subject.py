import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class SubjectModel(BaseModel):
    __tablename__ = "subject"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    modules = relationship(
        "ModuleModel",
        back_populates="subject",
        uselist=True
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )
