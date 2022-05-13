from typing import Any

from app.common.conn import conn
from app.model.user import User, UserRegister


class UserRepository:
    async def create(self, user: UserRegister) -> None:
        query = """
            INSERT INTO users (email, password, name)
                 VALUES (:email, :password, :name)
        """
        values = {
            "email": user.email,
            "password": user.password,
            "name": user.name,
        }
        await conn.database.execute(query, values)

    async def is_exists(self, email: str) -> Any:
        query = """
            SELECT EXISTS(
                SELECT 1
                  FROM users
                 WHERE email = :email
                 LIMIT 1
            ) as value
        """
        values = {"email": email}
        return await conn.database.fetch_one(query, values)

    async def get(self, id: int) -> User:
        query = """
            SELECT *
              FROM users
             WHERE id = :id
             LIMIT 1
        """
        values = {"id": id}
        return await conn.database.fetch_one(query, values)

    async def getByEmail(self, email: str) -> User:
        query = """
            SELECT *
              FROM users
             WHERE email = :email
             LIMIT 1
        """
        values = {"email": email}
        return await conn.database.fetch_one(query, values)
