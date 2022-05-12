from pydantic import BaseModel
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any


class Response:
    def __call__(self, status_code: int, detail: str, data: Any | None = None) -> JSONResponse:
        if data is not None:
            data = jsonable_encoder(data)
        return JSONResponse(content=dict(detail=detail, data=data), status_code=status_code)


response = Response()


class ResponseModel(BaseModel):
    detail: str
    data: Any | None
