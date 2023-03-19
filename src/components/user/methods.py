import logging
from typing import List

from sqlalchemy import select, update, delete
from pydantic import parse_obj_as
import bcrypt

from src.models.user import UserModel
from src.models.base import get_session
from src.models.base import get_async_session
from src.components.user.schemas import UserSchema
from src.components.user.schemas import UserResponse
from src.components.user.schemas import UsersResponse
from src.components.user.schemas import UserSecure
from src.components.authentication.methods import encode_jwt_token


async def create_user(user: UserSchema):
    user_query = UserModel().fill(**user.dict())
    
    async with get_async_session() as session:
        session.add(user_query)
        await session.commit()

    return UserResponse(
        user=user,
        message="User successfully created",
        success=True
        )


async def get_users():
    user_state = select(
        UserModel.id,
        UserModel.username,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.patronymic,
    )

    async with get_async_session() as session:
        return UsersResponse(
            users=parse_obj_as(list[UserSecure], (await session.execute(user_state)).fetchall()),
            message="Users collected successfully",
            success=True
        )


async def get_user(id: str):
    user_state = select(
        UserModel.id,
        UserModel.username,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.patronymic,
    ).where(
        UserModel.id == id
    )

    async with get_async_session() as session:
        return UserResponse(
            user=(await session.execute(user_state)).fetchone(),
            message="User successfully taken",
            success=True
        )


async def update_user(user: UserSchema):
    user_state = update(
        UserModel
    ).where(
        UserModel.id == user.id
    ).values(
        **user.dict()
    )

    async with get_async_session() as session:
        await session.execute(user_state)
        await session.commit()

    return UserResponse(
        user=user,
        message="User successfully updated",
        success=True
    )


async def delete_user(id: str):
    user_state = delete(
        UserModel
    ).where(
        UserModel.id == id
    )

    async with get_async_session() as session:
        await session.execute(user_state)
        await session.commit()

    return UserResponse(
        message="User successfully deleted",
        success=True
    )


async def login_user(user: UserSchema):
    
    user_state = select(
        UserModel
    ).where(
        UserModel.username == user.username
    )

    async with get_async_session() as session:
        try: 
            user_state = (await session.execute(user_state)).fetchone()[0]
        except IndexError:
            raise IndexError("This user doesn't exist")

    logging.warning(user)
    logging.warning(user_state)

    if not bcrypt.checkpw(user.hash_password, user_state.hash_password):
        raise ValueError('Неверный пароль')

    token = encode_jwt_token(user_state.id)

    return UserResponse(
        user=UserSecure.from_orm(user_state),
        message="You're successfully authorized",
        success=True
    ), token
