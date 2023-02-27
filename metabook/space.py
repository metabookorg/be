"""
export_router: APIRouter = APIRouter(prefix='/export')


@export_router.get(path='/pdf',
            tags=['pdf'],
            summary='Export book as PDF',
            description='Export book as PDF',
            response_model=StringIO,
            responses={
                200: {
                    "description": "Success",
                },
            },
            response_model_by_alias=True)
async def to_pdf(book: tp.List[PageUrl]) -> StringIO:
    loaded = BookLoader.from_urls(book=book, raise_mode=True)

    return Exporter.to_pdf(book=loaded)
"""