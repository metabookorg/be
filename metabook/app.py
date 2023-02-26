"""
APP
FastAPI app definition, initialization and definition of routers.
@author: iXB3 (Matteo Causio)
"""

# # Installed # #
import uvicorn
from fastapi import FastAPI, APIRouter
import asyncio
import typing as tp
from fastapi.middleware.cors import CORSMiddleware

# # Package # #
from .app_settings import AppSettings, RunAppSettings
from .middlewares import request_handler
from .routers import ROUTERS


__all__ = ("create", "run")


def create(settings: AppSettings | None = None,
           routers: tp.Tuple[APIRouter] | None = None,
           add_cors: bool = True,
           mock_mode: bool = False) -> FastAPI:
    """Create app"""
    if not isinstance(settings, AppSettings):
        print("Using default application settings")
        settings = AppSettings()
    app = FastAPI(**settings.dict(exclude_none=True))

    # check and add routers
    if not routers:
        routers = ROUTERS
    for rt in routers:
        app.include_router(rt, prefix=settings.prefix)


    # add middleware
    #app.middleware("http")(request_handler)
    if add_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
        )

    return app


def run(app: FastAPI, settings: RunAppSettings = RunAppSettings()):
    """Run APP using Uvicorn"""
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )


def create_run(settings: RunAppSettings = RunAppSettings()):
    """Create and run APP"""
    run(app=create(), settings=settings)
