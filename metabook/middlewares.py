"""
Middlewares
Functions that run as something gets processed.
@author: Matteo Causio (iXB3)
"""

# # Installed # #
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# # Package # #
#from sapyutils.loggers import APILogger, ConsoleLogger

__all__ = ("request_handler",)


#logger = APILogger()


async def request_handler(request: Request, call_next):
    """
    Middleware used to process each request on FastAPI, provide logging and error handling.
    """
    try:
        response = await call_next(request)
        #logger.manage_request(request, response)
        return response
    except Exception as ex:
        #logger.manage_exception(e=ex)
        if hasattr(ex, 'status_code'):
            ex = HTTPException(status_code=ex.status_code, detail=str(ex))
        # Re-raising other exceptions will return internal error 500 to the client
        raise ex
