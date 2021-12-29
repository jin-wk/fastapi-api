import bcrypt
from fastapi import APIRouter, Depends

from app.repository.user import UserRepository
from app.model.user import UserRegister
from app.model.response import response

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegister, repository: UserRepository = Depends(UserRepository)):
    is_exists = await repository.is_exists(user.email)

    if is_exists.value:
        return response(status_code=409, message="Email Exists")

    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    await repository.create(user.dict())

    return response(status_code=201, message="Created")


@router.get("/{id}")
async def get(id: int, repository: UserRepository = Depends(UserRepository)):
    user = await repository.get(id)
    if user is None:
        return response(status_code=404, message="Not found")
    return response(status_code=200, message="Success", data=user)
