import uuid
from pydantic import Field, BaseModel

from src.components.base_response.schema import BaseResponse


class TicketSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str


class TicketQuestionSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    ticket_id: uuid.UUID
    question_id: uuid.UUID

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TicketResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    ticket: TicketSchema | None


class TicketsResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    tickets: list[TicketSchema] = Field(default_factory=list)
