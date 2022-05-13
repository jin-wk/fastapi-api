from typing import Any, List

from app.common.conn import conn
from app.model.board import Board, BoardDto


class BoardRepository:
    async def list(self) -> List[Board]:
        query = """
            SELECT *
              FROM boards
        """
        return await conn.database.fetch_all(query=query)

    async def get(self, id: int) -> Board:
        query = """
            SELECT *
              FROM boards
             WHERE id = :id
             LIMIT 1
        """
        values = {"id": id}
        return await conn.database.fetch_one(query, values)

    async def is_exists(self, id: int) -> Any:
        query = """
            SELECT EXISTS(
                SELECT 1
                  FROM boards
                 WHERE id = :id
                 LIMIT 1
            ) as value
        """
        values = {"id": id}
        return await conn.database.fetch_one(query, values)

    async def create(self, user_id: int, board_dto: BoardDto) -> None:
        query = """
            INSERT INTO boards (user_id, title, content)
                 VALUES (:user_id, :title, :content)
        """
        values = {
            "user_id": user_id,
            "title": board_dto.title,
            "content": board_dto.content,
        }
        await conn.database.execute(query, values)

    async def update(self, id: int, board_dto: BoardDto) -> None:
        query = """
            UPDATE boards
               SET title = :title,
                   content = :content
             WHERE id = :id
        """
        values = {
            "id": id,
            "title": board_dto.title,
            "content": board_dto.content,
        }
        await conn.database.execute(query, values)

    async def delete(self, id: int) -> None:
        query = """
            DELETE FROM boards
                  WHERE id = :id
        """
        values = {"id": id}
        await conn.database.execute(query, values)
