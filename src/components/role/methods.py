import logging
from sqlalchemy import select

from src.models.role import RoleModel
from src.components.role.schemas import RoleSchema
from src.models.base import get_session
from src.components.role.schemas import RoleResponse

async def create_role(role: RoleSchema):
    role_query = RoleModel().fill(**role.dict())

    async with get_session() as session:
        await session.add(role_query)
        await session.commit()

    return RoleResponse(
        role=role,
        message="Role successfully created",
        success=True
        )

async def get_role():
    role_query = select(RoleModel)
    with get_session() as session:
        role = session.execute(role_query).first()

    logging.warning(role)

    return RoleResponse(
        role=role[0],
        message="Role successfully created",
        success=True
        )
