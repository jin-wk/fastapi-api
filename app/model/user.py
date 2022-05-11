from pydantic.main import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str
    password_confrim: str
    name: str
