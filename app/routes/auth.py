from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.repository.user import UserRepository
from app.model.user import User, UserRegister, UserLogin
from app.model.response import response, ResponseModel
from app.common.config import get_config
from jose import JWTError, jwt

router = APIRouter(prefix="/api/auth", tags=["Auth"])
config = get_config()
oauth2 = HTTPBearer(scheme_name="Authorization")


@router.post("/register", response_model=ResponseModel)
async def register(user: UserRegister, repository: UserRepository = Depends(UserRepository)):
    is_exists = await repository.is_exists(user.email)

    if is_exists.value:
        raise HTTPException(409, "Email is already exists")

    if user.password != user.password_confrim:
        raise HTTPException(409, "Password and Password Confirm must be same")

    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    await repository.create(user)

    return response(201, "Created")

@router.post("/login", response_model=ResponseModel)
async def login(user: UserLogin, repository: UserRepository = Depends(UserRepository)):
    is_exists = await repository.is_exists(user.email)

    if not is_exists.value:
        raise HTTPException(404, "Email is not found")

    info: User = await repository.getByEmail(user.email)

    if not bcrypt.checkpw(user.password.encode('utf-8'), info.password.encode('utf-8')):
        raise HTTPException(400, "Password does not matched")

    payload = {
        "id": info.id,
        "email": info.email,
        "exp": datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRES_MIN)
    }
    return response(200, "Ok", {"token": jwt.encode(payload, config.JWT_SECRET, "HS256")})

@router.get("/user", response_model=ResponseModel)
async def getUser(token: HTTPAuthorizationCredentials = Depends(oauth2), repository: UserRepository = Depends(UserRepository)):
    try:
        payload = jwt.decode(token.credentials, config.JWT_SECRET, "HS256")
        id = payload.get("id")
        if id is None:
            raise HTTPException(401, "Not authenticated")
    except JWTError:
        raise HTTPException(401, "Not authenticated")

    user = await repository.get(id)
    if user is None:
        raise HTTPException(401, "Not authenticated")

    return response(200, "Ok", user)
