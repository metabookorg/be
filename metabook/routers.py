"""
Building and implementation of Api Router (services exposed by the app).
@author: Matteo Causio (iXB3)
"""
# # Installed # #
from fastapi import APIRouter, Request
import typing as tp
import asyncio

# # Package # #
from . import errors as err
from .creators import BookCreator, TxtCreator
from .img import PageUrl
from .models import NewKidBookRequest, NewKidBookResponse


#__all__ = ("build_routers")



######################
#   -   ROUTER   -   #
######################

router: APIRouter = APIRouter(prefix='/metabook')


@router.get(path='/',
            tags=['welcome'],
            summary='Welcome',
            description='Welcome',
            response_model=str)
async def welcome() -> str:
    """Welcome service"""
    return "Welcome to Metabooks!"


@router.post(path='/new',
            tags=['new'],
            summary='Create a brand new book for kids',
            description='Create a brand new book for kids',
            response_model=tp.List[PageUrl],
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def new(request: NewKidBookRequest) -> NewKidBookResponse:
    """Create a brand new fabulous book for kids"""
    creator = BookCreator(txt_creator=TxtCreator(text_type='kids story',
                                                 creativity_risk=0.5,
                                                 **request.dict()))
    return NewKidBookResponse(data=creator.create())


