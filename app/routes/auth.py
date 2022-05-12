from typing import Any
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from app.dependency.jwt_bearer import decode_jwt, encode_jwt, jwt_bearer

from app.repository.user import UserRepository
from app.model.user import User, UserRegister, UserLogin
from app.model.response import response, ResponseModel

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=ResponseModel, status_code=201)
async def register(user: UserRegister, repository: UserRepository = Depends(UserRepository)):
    is_exists: dict = await repository.is_exists(user.email)

    if is_exists.value:
        raise HTTPException(409, "Email is already exists")

    if user.password != user.password_confrim:
        raise HTTPException(409, "Password and Password Confirm must be same")

    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    await repository.create(user)

    return response(201, "Created")


@router.post("/login", response_model=ResponseModel)
async def login(user: UserLogin, repository: UserRepository = Depends(UserRepository)):
    is_exists: dict = await repository.is_exists(user.email)

    if not is_exists.value:
        raise HTTPException(404, "Email is not found")

    info: User = await repository.getByEmail(user.email)

    if not bcrypt.checkpw(user.password.encode("utf-8"), info.password.encode("utf-8")):
        raise HTTPException(400, "Password does not matched")

    return response(200, "Ok", {"token": encode_jwt(info)})


@router.get("/user", response_model=ResponseModel)
async def getUser(token: str = Depends(jwt_bearer), repository: UserRepository = Depends(UserRepository)):
    payload: Any = decode_jwt(token)
    user: User = await repository.get(payload.get("user")["id"])
    return response(200, "Ok", user)


@router.get("/test", response_model=ResponseModel, dependencies=[Depends(jwt_bearer)])
async def test():
    return response(200, "Ok")
