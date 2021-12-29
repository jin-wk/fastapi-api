from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, Any


class Response:
    def __call__(self, status_code: int, message: str, data: Optional[Any] = None):
        if data is not None:
            data = jsonable_encoder(data)

        return JSONResponse(status_code=status_code, content=dict(message=message, data=data))


response = Response()
