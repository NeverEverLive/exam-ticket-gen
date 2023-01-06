import datetime

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String, nullable=True)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    users = relationship(
        "UserModel",
        back_populates="role",
        uselist=True,
        cascade="all,delete-orphan"
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
    )
