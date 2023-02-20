from fastapi import APIRouter, Query, Depends, Response

from src.components.user.schemas import UserResponse, UserSchema, UsersResponse, UserLogin
from src.components.role.schemas import RoleResponse, RoleSchema
from src.components.user.methods import create_user
from src.components.user.methods import get_users
from src.components.user.methods import get_user
from src.components.user.methods import update_user
from src.components.user.methods import delete_user
from src.components.user.methods import login_user
from src.components.role.methods import create_role
from src.components.authentication.jwt import JWTBearer


router = APIRouter(prefix="/user")


@router.post("/", response_model=UserResponse, status_code=201)
async def register_user_endpoint(user: UserSchema):
    return await create_user(user)


@router.get("/", response_model=UsersResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_users_endpoint():
    return await get_users()


@router.post("/login", response_model=UserResponse, status_code=200)
async def get_users_endpoint(user: UserLogin, response: Response):
    user, token = await login_user(user)
    response.headers["Authorization"] = token
    response.headers["Access-Control-Expose-Headers"] = "*"
    return user


@router.get("/detail", response_model=UserResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_user_endpoint(user_id: str = Query(alias="id", default=None)):
    return await get_user(user_id)


@router.put("/", response_model=UserResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_user_endpoint(user: UserSchema):
    return await update_user(user)


@router.delete("/", response_model=UserResponse, status_code=202, dependencies=[Depends(JWTBearer())])
async def get_user_endpoint(user_id: str = Query(alias="id")):
    return await delete_user(user_id)


@router.post("/role", response_model=RoleResponse, status_code=201)
async def create_role_endpoint(user: RoleSchema):
    return await create_role(user)
