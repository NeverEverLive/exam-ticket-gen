from typing import List
import itertools as it

from sqlalchemy import select, update, delete
from pydantic import parse_obj_as
import bcrypt

from src.models.user import UserModel
from src.models.base import get_session
from src.components.user.schemas import UserSchema
from src.components.user.schemas import UserResponse
from src.components.user.schemas import UsersResponse
from src.components.user.schemas import UserSecure
from src.components.authentication.methods import encode_jwt_token


def create_user(user: UserSchema):
    user_query = UserModel().fill(**user.dict())
    
    with get_session() as session:
        session.add(user_query)
        session.commit()
    
    return UserResponse(
        user=user,
        message="User successfully created",
        success=True
        )


def get_users():
    user_state = select(
        UserModel.id,
        UserModel.username,
    )

    with get_session() as session:
        print(list(it.chain(*session.execute(user_state).fetchall())))
        return UsersResponse(
            users=parse_obj_as(List[UserSecure], session.execute(user_state).fetchall()),
            message="Users collected successfully",
            success=True
        )


def get_user(id: str):
    user_state = select(
        UserModel.id,
        UserModel.username,
    ).where(
        UserModel.id == id
    )

    with get_session() as session:
        return UserResponse(
            user=session.execute(user_state).fetchone(),
            message="User successfully taken",
            success=True
        )


def update_user(user: UserSchema):
    user_state = update(
        UserModel
    ).where(
        UserModel.id == user.id
    ).values(
        **user.dict()
    )

    with get_session() as session:
        session.execute(user_state)
        session.commit()

    return UserResponse(
        user=user,
        message="User successfully updated",
        success=True
    )


def delete_user(id: str):
    user_state = delete(
        UserModel
    ).where(
        UserModel.id == id
    )

    with get_session() as session:
        session.execute(user_state)
        session.commit()

    return UserResponse(
        message="User successfully deleted",
        success=True
    )


def login_user(user: UserSchema):
    
    user_state = select(
        UserModel
    ).where(
        UserModel.username == user.username
    )

    with get_session() as session:
        try: 
            user_state = session.execute(user_state).fetchone()[0]
        except IndexError:
            raise IndexError("This user doesn't exist")

    print(user_state)

    if not bcrypt.checkpw(user.hash_password, user_state.hash_password):
        raise ValueError('Неверный пароль')

    token = encode_jwt_token(user_state.id)


    return UserResponse(
        user=UserSecure.from_orm(user_state),
        message="You're successfully authorized",
        success=True
    ), token
