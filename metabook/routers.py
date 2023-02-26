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
from .models import NewKidBookRequest, NewKidBookResponse, NewPromptBookRequest


#__all__ = ("build_routers")

DEFAULT_TEXT_TYPE = 'kid story'

######################
#   -   ROUTER   -   #
######################

new_router: APIRouter = APIRouter(prefix='/new')


@new_router.get(path='/',
            tags=['welcome'],
            summary='Welcome',
            description='Welcome',
            response_model=str)
async def welcome() -> str:
    """Welcome service"""
    return "Welcome to Metabook's generation services"


@new_router.post(path='/from_params',
            tags=['new'],
            summary='Create a brand-new book for kids',
            description='Create a brand-new book for kids',
            response_model=NewKidBookResponse,
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def from_params(request: NewKidBookRequest | None = None) -> NewKidBookResponse:
    """Create a brand new fabulous book for kids"""
    if not request:
        request = NewKidBookRequest()
    creator = BookCreator(txt_creator=TxtCreator(txt_request=request.txt_request, creativity_risk=0.5))
    # TODO: per mockare il servizio decommentare la linea successiva
    # return NewKidBookResponse(data=[PageUrl(txt='a pippa', idx=0, url='http://a:pippa/a/pippaaaaa')])

    return NewKidBookResponse(data=creator.create(style=request.style))


@new_router.post(path='/from_prompt',
            tags=['new'],
            summary='Create a brand-new book for kids',
            description='Create a brand-new book for kids',
            response_model=NewKidBookResponse,
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def from_prompt(request: NewPromptBookRequest) -> NewKidBookResponse:
    """Create a brand new fabulous book for kids"""
    creator = BookCreator(txt_creator=TxtCreator(txt_request=request.txt_request, creativity_risk=0.5))
    # TODO: per mockare il servizio decommentare la linea successiva
    # return NewKidBookResponse(data=[PageUrl(txt='a pippa', idx=0, url='http://a:pippa/a/pippaaaaa')])
    return NewKidBookResponse(data=creator.create(style=request.style))

ROUTERS = [new_router]
