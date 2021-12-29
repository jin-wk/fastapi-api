from app.common.conn import conn


class UserRepository:
    async def create(self, user: dict):
        query = "INSERT INTO users (email, password, name) VALUES (:email, :password, :name)"
        await conn.database.execute(query=query, values=user)

    async def is_exists(self, email: str):
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = :email LIMIT 1) as value"
        return await conn.database.fetch_one(query=query, values={"email": email})

    async def get(self, id: int):
        query = "SELECT * FROM users WHERE id = :id LIMIT 1"
        return await conn.database.fetch_one(query=query, values={"id": id})
