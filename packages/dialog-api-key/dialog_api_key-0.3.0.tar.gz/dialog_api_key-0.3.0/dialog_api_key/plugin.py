from http import HTTPStatus

from decouple import Csv, config
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


API_KEY_HEADER = config("API_KEY_HEADER", default="X-Api-Key")
API_KEYS = config("API_KEYS", cast=Csv(post_process=set))
API_KEY_IGNORED_PATHS = config(
    "API_KEY_IGNORED_PATHS", cast=Csv(post_process=set), default="/docs,"
)


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in API_KEY_IGNORED_PATHS:
            return await call_next(request)

        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key or api_key not in API_KEYS:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="API key inválida ou não fornecida.",
            )

        return await call_next(request)


def register_plugin(app: FastAPI):
    app.add_middleware(APIKeyMiddleware)
