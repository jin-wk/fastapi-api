from fastapi import FastAPI
from starlette.requests import Request
from app.common.config import get_config
from app.common.conn import conn
from app.routes import auth

get_config.cache_clear()
config = get_config()

app = FastAPI(
    title=config.APP_NAME,
    version=f"{config.APP_ENV} - {config.APP_VERSION}",
)

conn.init_app(app, config)
app.include_router(auth.router)
