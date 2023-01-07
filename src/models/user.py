import datetime

from sqlalchemy import Column, ForeignKeyConstraint, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import LargeBinary
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    role_id = Column(UUID(as_uuid=True), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    username = Column(String, nullable=False)
    hash_password = Column(LargeBinary, nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    role = relationship(
        "RoleModel",
        back_populates="users",
        uselist=False
    )

    questions = relationship(
        "QuestionModel",
        back_populates="user",
        uselist=True
    )

    tickets = relationship(
        "TicketModel",
        back_populates="user",
        uselist=True
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (role_id,),
            ("role.id",)
        )
    )
