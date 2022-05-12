from fastapi import FastAPI
from databases import Database, DatabaseURL
from decouple import config


class Conn:
    def __init__(self, app: FastAPI = None):
        self.database = None

        if app is not None:
            self.init_app(app=app)

    def make_connection(self, username: str, password: str, host: str, port: str, database: str):
        return DatabaseURL(f"mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4")

    def init_connection(self):
        connection = self.make_connection(
            username=config("DB_USERNAME"),
            password=config("DB_PASSWORD"),
            host=config("DB_HOST"),
            port=config("DB_PORT"),
            database=config("DB_DATABASE"),
        )
        return Database(connection, ssl=False, pool_recycle=900)

    def init_app(self, app: FastAPI):
        self.database = self.init_connection()

        @app.on_event("startup")
        async def startup():
            await self.database.connect()

        @app.on_event("shutdown")
        async def shutdown():
            await self.database.disconnect()


conn = Conn()
