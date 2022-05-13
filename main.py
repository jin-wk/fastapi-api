from fastapi import FastAPI
from decouple import config

from app.common.conn import conn
from app.routes import auth, board

app = FastAPI(
    title=config("APP_NAME"),
    version=f"{config('APP_ENV')} - {config('APP_VERSION')}",
)

conn.init_app(app)
app.include_router(auth.router)
app.include_router(board.router)
