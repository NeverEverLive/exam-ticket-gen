import uuid
import logging
from pydantic import parse_obj_as
from sqlalchemy import select, update, delete

from src.models.base import get_async_session
from src.models.module import ModuleModel
from src.components.module.schemas import ModuleResponse, ModuleSchema, ModulesResponse


async def create_module(module: ModuleSchema) -> ModuleResponse:
    module_state = ModuleModel().fill(**module.dict())

    async with get_async_session() as session:
        session.add(module_state)
        await session.commit()

    return ModuleResponse(
        module=module,
        message="Module successfully created",
        success=True
    )


async def get_modules() -> ModulesResponse:
    module_state = select(
        ModuleModel.id,
        ModuleModel.subject_id,
        ModuleModel.name,
        ModuleModel.description,
    )

    async with get_async_session() as session:
        return ModulesResponse(
            modules=parse_obj_as(list[ModuleSchema], (await session.execute(module_state)).fetchall()),
            message="Module collected successfully",
            success=True
        )


async def get_modules_by_subject_id(subject_id: uuid.UUID) -> ModulesResponse:
    module_state = select(
        ModuleModel.id,
        ModuleModel.subject_id,
        ModuleModel.name,
        ModuleModel.description,
    ).where(
        ModuleModel.subject_id == subject_id
    )

    async with get_async_session() as session:
        return ModulesResponse(
            modules=parse_obj_as(list[ModuleSchema], (await session.execute(module_state)).fetchall()),
            message="Module collected successfully",
            success=True
        )


async def get_module(id: str) -> ModuleResponse:
    module_state = select(
        ModuleModel.id,
        ModuleModel.subject_id,
        ModuleModel.name,
        ModuleModel.description,
    ).where(
        ModuleModel.id == id
    )

    async with get_async_session() as session:
        logging.warning(ModuleSchema.from_orm((await session.execute(module_state)).fetchone()))
        return ModuleResponse(
            module=ModuleSchema.from_orm((await session.execute(module_state)).fetchone()),
            message="Module successfully taken",
            success=True
        )


async def update_module(module: ModuleSchema) -> ModuleResponse:
    module_state = update(
        ModuleModel
    ).where(
        ModuleModel.id == module.id
    ).values(
        **module.dict()
    )

    async with get_async_session() as session:
        await session.execute(module_state)
        await session.commit()

    return ModuleResponse(
        module=module,
        message="Module successfully updated",
        success=True
    )


async def delete_module(id: str) -> ModuleResponse:
    module_state = delete(
        ModuleModel
    ).where(
        ModuleModel.id == id
    )

    async with get_async_session() as session:
        await session.execute(module_state)
        await session.commit()

    return ModuleResponse(
        message="Module successfully deleted",
        success=True
    )
