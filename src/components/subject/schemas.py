import uuid
from pydantic import Field, BaseModel

from src.components.base_response.schema import BaseResponse


class SubjectSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: str | None


class SubjectResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    subject: SubjectSchema | None


class SubjectsResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    subjects: list[SubjectSchema] = Field(default_factory=list)
