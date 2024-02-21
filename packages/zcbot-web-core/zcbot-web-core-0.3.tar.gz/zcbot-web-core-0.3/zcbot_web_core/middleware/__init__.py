from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


def register_middleware(app: FastAPI, middlewares: List[BaseHTTPMiddleware] = None):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if middlewares:
        for middleware in middlewares:
            app.add_middleware(middleware)
