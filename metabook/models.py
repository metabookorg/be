"""
Models.
@author: iXB3 (Matteo Causio)
"""

# # Installed
import pydantic as pdt
import typing as tp

# # Package


class BaseModel(pdt.BaseModel):
    "Base model"
    class Config:
        allow_population_by_fields_name = True
        arbitrary_types_allowed = True


class PageUrl(BaseModel):
    txt: str
    idx: int
    url: str


class BaseResponse(BaseModel):
    description: str = "Success"
    data: tp.Union[tp.Dict[str, tp.Any], tp.List[tp.Dict[str, tp.Any]]] | None


class NewKidBookRequest(BaseModel):
    """Request of a brand-new book for kids"""
    argument: str | None
    environment: str | None
    time: tp.Union[str, list] | None
    characters: tp.List[str] | None


class NewKidBookResponse(BaseModel):
    data: tp.List[PageUrl]
