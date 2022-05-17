import bcrypt
from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from app.model.user import User, UserRegister, UserLogin
from app.model.response import response, Response
from app.repository.user import UserRepository
from app.dependency.jwt_bearer import decode_jwt, encode_jwt, jwt_bearer

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", status_code=201, response_model=Response)
async def register(user: UserRegister, repository: UserRepository = Depends(UserRepository)):
    exists: Any = await repository.is_exists(user.email)

    if exists.value:
        raise HTTPException(409, "Email is already exists")

    if user.password != user.password_confrim:
        raise HTTPException(409, "Password and Password Confirm must be same")

    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    await repository.create(user)

    return response(201, "Created")


@router.post("/login", response_model=Response)
async def login(user: UserLogin, repository: UserRepository = Depends(UserRepository)):
    exists: Any = await repository.is_exists(user.email)

    if not exists.value:
        raise HTTPException(404, "Email is not found")

    info: User = await repository.getByEmail(user.email)

    if not bcrypt.checkpw(user.password.encode("utf-8"), info.password.encode("utf-8")):
        raise HTTPException(400, "Password does not matched")

    return response(200, "Ok", {"token": encode_jwt(info)})


@router.get("/user", response_model=Response)
async def getUser(token: str = Depends(jwt_bearer), repository: UserRepository = Depends(UserRepository)):
    payload: Any = decode_jwt(token)
    user: User = await repository.get(payload.get("user")["id"])
    return response(200, "Ok", user)


@router.get("/test", dependencies=[Depends(jwt_bearer)], response_model=Response)
async def test():
    return response(200, "Ok")
