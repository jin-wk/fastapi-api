from datetime import datetime, timedelta
from typing import Any
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from decouple import config

from app.model.user import User


class JwtBearer(HTTPBearer):
    def __init__(self, schema_name: str = "Authorization", auto_error: bool = False):
        super(JwtBearer, self).__init__(scheme_name=schema_name, auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(401, "Unauthorized")
            return credentials.credentials
        else:
            raise HTTPException(401, "Unauthorized")


jwt_bearer = JwtBearer()


def encode_jwt(user: User) -> Any:
    payload: dict = {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        "exp": datetime.utcnow() + timedelta(minutes=int(config("JWT_EXPIRES_MIN"))),
    }
    return jwt.encode(payload, config("JWT_SECRET"), "HS256")


def decode_jwt(token: str) -> Any:
    try:
        payload: Any = jwt.decode(token, config("JWT_SECRET"), "HS256")
    except JWTError:
        raise HTTPException(401, "Unauthorized")
    return payload
