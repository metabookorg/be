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

# # Package # #
from .app_settings import AppSettings, RunAppSettings
from .middlewares import request_handler
from .routers import router


__all__ = ("create", "run")


def create(settings: AppSettings = AppSettings(),
           routers: tp.Tuple[APIRouter] | None = None,
           mock_mode: bool = False) -> FastAPI:
    """Create app"""
    app = FastAPI(**settings.dict(exclude_none=True))

    # check and add routers
    if not routers:
        routers = [router]
    for rt in routers:
        app.include_router(rt)


    # add middleware
    app.middleware("http")(request_handler)

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