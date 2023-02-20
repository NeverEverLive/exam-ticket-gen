from typing import List, Optional
from pydantic import BaseModel, Field, validator
import uuid

import bcrypt

from src.components.base_response.schema import BaseResponse


class UserSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role_id: uuid.UUID
    first_name: str
    last_name: str
    patronymic: Optional[str]
    username: str
    hash_password: bytes = Field(alias="password")

    @validator("hash_password", pre=True)
    def password_hasher(cls, value: str) -> bytes:
        if isinstance(value, str):
            return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        elif isinstance(value, bytes):
            return value
        else:
            raise ValueError("Пароль должен быть передан строкой.")

    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True


class UserLogin(BaseModel):
    username: str
    hash_password: bytes = Field(alias="password")


class UserSecure(BaseModel):
    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    patronymic: str | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponse(BaseResponse):
    user: Optional[UserSecure]

    class Config:
        allow_population_by_field_name = True


class UsersResponse(BaseResponse):
    users: List[UserSecure] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
