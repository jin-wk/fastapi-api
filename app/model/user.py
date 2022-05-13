from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confrim: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
