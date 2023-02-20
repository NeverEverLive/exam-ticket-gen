import logging
from fastapi import APIRouter, Query, Depends

from src.components.module.schemas import ModuleResponse, ModuleSchema, ModulesResponse
from src.components.module.methods import create_module, get_module, get_modules, update_module, delete_module
from src.components.authentication.jwt import JWTBearer


router = APIRouter(prefix="/module")


@router.post("/", response_model=ModuleResponse, status_code=201)
async def create_subject_endpoint(subject: ModuleSchema):
    logging.warning(subject)
    return await create_module(subject)

@router.get("/", response_model=ModulesResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subjects_endpoint():
    return await get_modules()


@router.get("/detail", response_model=ModuleResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id", default=None)):
    return await get_module(subject_id)


@router.put("/", response_model=ModuleResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject: ModuleSchema):
    return await update_module(subject)


@router.delete("/", response_model=ModuleResponse, status_code=202, dependencies=[Depends(JWTBearer())])
async def get_subject_endpoint(subject_id: str = Query(alias="id")):
    return await delete_module(subject_id)
