"""
Building and implementation of Api Router (services exposed by the app).
@author: Matteo Causio (iXB3)
"""
# # Installed # #
from io import StringIO
from fastapi import APIRouter
import typing as tp
from fastapi.responses import FileResponse, StreamingResponse

# # Package # #
from . import errors as err
from .creators import BookCreator, TxtCreator
from .img import PageUrl
from .models import NewKidBookRequest, BookUrlsResponse, NewPromptBookRequest
from .tools import BookLoader, Exporter
from .static import ImgStyle

#__all__ = ("build_routers")


######################
#   -   ROUTERS   -   #
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
            response_model=BookUrlsResponse,
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def from_params(request: NewKidBookRequest | None = None) -> BookUrlsResponse:
    """Create a brand new fabulous book for kids"""
    if not request:
        request = NewKidBookRequest()
    creator = BookCreator(txt_creator=TxtCreator(txt_request=request.txt_request, creativity_risk=0.5))
    # TODO: per mockare il servizio decommentare la linea successiva
    # return NewKidBookResponse(data=[PageUrl(txt='a pippa', idx=0, url='http://a:pippa/a/pippaaaaa')])

    return BookUrlsResponse(data=creator.create(style=request.style))


@new_router.post(path='/from_prompt',
            tags=['new'],
            summary='Create a brand-new book for kids',
            description='Create a brand-new book for kids',
            response_model=BookUrlsResponse,
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def from_prompt(request: NewPromptBookRequest) -> BookUrlsResponse:
    """Create a brand new fabulous book for kids"""
    creator = BookCreator(txt_creator=TxtCreator(txt_request=request.txt_request, creativity_risk=0.5))
    # TODO: per mockare il servizio decommentare la linea successiva
    # return NewKidBookResponse(data=[PageUrl(txt='a pippa', idx=0, url='http://a:pippa/a/pippaaaaa')])
    return BookUrlsResponse(data=creator.create(style=request.style))



static_router: APIRouter = APIRouter(prefix='/static')


@static_router.get(path='/img_styles',
            tags=['style'],
            summary='Export book as PDF',
            description='Export book as PDF',
            response_model=tp.List[ImgStyle],
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def get_img_styles() -> tp.List[ImgStyle]:
    """Create a brand new fabulous book for kids"""
    return list(ImgStyle)


export_router: APIRouter = APIRouter(prefix='/export')


@export_router.post(path='/pdf',
            tags=['pdf'],
            summary='Export book as PDF',
            description='Export book as PDF',
            response_model=None,#FileResponse,
            responses={
                200: {
                    "description": "Success",
                },
            }
                   )
# TODO: raise "ValueError: stat: embedded null character in path" after this function (inside fastapi)
# FileResponse expect string instead ByteIO or ByteIO.read()
async def to_pdf(book: tp.List[PageUrl]) -> StreamingResponse:
    loaded = BookLoader.from_urls(book=book, raise_mode=True)
    #headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return StreamingResponse(Exporter.to_pdf(book=loaded), headers=headers, media_type='application/pdf')


ROUTERS = [new_router, static_router, export_router]
