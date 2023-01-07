import uuid
from pydantic import Field, BaseModel

from src.components.base_response.schema import BaseResponse


class RoleSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleResponse(BaseResponse):
    role: RoleSchema

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    