import uuid
from pydantic import Field, BaseModel

from src.components.base_response.schema import BaseResponse


class QuestionSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    module_id: uuid.UUID
    user_id: uuid.UUID | None
    probability: int = Field(default=100)
    text: str


class QuestionResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    question: QuestionSchema | None


class QuestionsResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    questions: list[QuestionSchema] = Field(default_factory=list)
