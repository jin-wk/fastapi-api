from datetime import datetime
from pydantic import BaseModel


class Board(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class BoardDto(BaseModel):
    title: str
    content: str
