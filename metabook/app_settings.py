"""
App settings loaders using Pydantic BaseSettings classes (load from environment variables)
@author: Matteo Causio (iXB3)
"""

# # Installed # #
import pydantic as pdt
import typing as tp

# # Sub-modules # #


__all__ = (
    "AppSettings",
    "RunAppSettings",
)


class BaseSettings(pdt.BaseSettings):
    pass


class AppSettings(BaseSettings):
    """
    Settings for app.
    """
    title: str = "Metabook"
    description: str = "Create fabulous books 4 kids"
    version: str = "0.0.1"
    contact: tp.Dict[str, tp.Any] = {
        "email": "matteocausio@yahoo"
    }
    app_licence: tp.Dict[str, tp.Any] = {
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    }



class RunAppSettings(BaseSettings):
    """
    Settings to run app.
    """
    host: str = pdt.Field(env="HOST", default='localhost')
    port: int = pdt.Field(env="PORT", default=1312)
    log_level: str = "INFO"

