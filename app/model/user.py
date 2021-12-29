from pydantic.main import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str
    name: str
