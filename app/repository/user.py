from app.common.conn import conn
from app.model.user import UserRegister


class UserRepository:
    async def create(self, user: UserRegister):
        query = """
            INSERT INTO users (email, password, name)
                 VALUES (:email, :password, :name)
        """
        await conn.database.execute(
            query=query, values={"email": user.email, "password": user.password, "name": user.name}
        )

    async def is_exists(self, email: str):
        query = """
            SELECT EXISTS(
                SELECT 1
                  FROM users
                 WHERE email = :email
                 LIMIT 1
            ) as value
        """
        return await conn.database.fetch_one(query=query, values={"email": email})

    async def get(self, id: int):
        query = """
            SELECT *
              FROM users
             WHERE id = :id
             LIMIT 1
        """
        return await conn.database.fetch_one(query=query, values={"id": id})

    async def getByEmail(self, email: str):
        query = """
            SELECT *
              FROM users
             WHERE email = :email
             LIMIT 1
        """
        return await conn.database.fetch_one(query=query, values={"email": email})