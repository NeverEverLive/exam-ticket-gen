import uuid
from pydantic import Field, BaseModel

from src.components.base_response.schema import BaseResponse


class ModuleSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    subject_id: uuid.UUID
    name: str
    description: str | None


class ModuleResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    module: ModuleSchema | None


class ModulesResponse(BaseResponse):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    modules: list[ModuleSchema] = Field(default_factory=list)
