from pydantic import EmailStr
from pydantic.main import BaseModel


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str
    created_at: str
    updated_at: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confrim: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str