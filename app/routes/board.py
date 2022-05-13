from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

from app.model.board import Board, BoardDto
from app.model.response import response, ResponseModel
from app.repository.board import BoardRepository
from app.dependency.jwt_bearer import decode_jwt, jwt_bearer

router = APIRouter(prefix="/api/boards", tags=["Board"], dependencies=[Depends(jwt_bearer)])


@router.get("/", response_model=ResponseModel)
async def list(repository: BoardRepository = Depends(BoardRepository)):
    boards: List[Board] = await repository.list()
    return response(200, "Ok", boards)


@router.get("/{id}", response_model=ResponseModel)
async def get(id: int, repository: BoardRepository = Depends(BoardRepository)):
    board: Board = await repository.get(id)
    if not board:
        raise HTTPException(404, "Board is not found")
    return response(200, "Ok", board)


@router.post("/", response_model=ResponseModel)
async def create(
    board_dto: BoardDto, token: str = Depends(jwt_bearer), respository: BoardRepository = Depends(BoardRepository)
):
    payload: Any = decode_jwt(token)
    user_id = payload.get("user")["id"]

    await respository.create(user_id, board_dto)
    return response(201, "Created")


@router.put("/{id}", response_model=ResponseModel)
async def update(id: int, board_dto: BoardDto, repository: BoardRepository = Depends(BoardRepository)):
    exists: Any = await repository.is_exists(id)

    if not exists.value:
        raise HTTPException(404, "Board is not found")

    await repository.update(id, board_dto)
    return response(200, "Ok")


@router.delete("/{id}", response_model=ResponseModel)
async def delete(id: int, repository: BoardRepository = Depends(BoardRepository)):
    exists: Any = await repository.is_exists(id)

    if not exists.value:
        raise HTTPException(404, "Board is not found")

    await repository.delete(id)
    return response(200, "Ok")
