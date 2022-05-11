import bcrypt
from fastapi import APIRouter, Depends, HTTPException

from app.repository.user import UserRepository
from app.model.user import UserRegister
from app.model.response import Response, response

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegister, repository: UserRepository = Depends(UserRepository)) -> Response:
    is_exists = await repository.is_exists(user.email)

    if is_exists.value:
        raise HTTPException(409, "Email is already exists.")

    if user.password != user.password_confrim:
        raise HTTPException(409, "Password and Password Confirm must be same.")

    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    await repository.create(user)

    return response(201, "Created")


@router.get("/{id}")
async def get(id: int, repository: UserRepository = Depends(UserRepository)) -> Response:
    user = await repository.get(id)
    if user is None:
        raise HTTPException(404, "User not found.")
    return response(200, "Success", user)
