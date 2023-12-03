import logging
import os

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from google.cloud.logging.handlers import StructuredLogHandler
from pydantic import BaseModel, Field

from .logging import CloudTraceFilter
from .middleware import LogMiddleware
from .context import cloud_trace_context


app = FastAPI()
app.add_middleware(LogMiddleware)

handler = StructuredLogHandler()
# handler.addFilter(CloudTraceFilter())
handler.filters = [CloudTraceFilter()]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class RootRequest(BaseModel):
    message: str = Field()


class Response(BaseModel):
    message: str = Field()


@app.post("/")
def main(
    request: RootRequest,
    r: Request,
) -> Response:

    logger.info("hello")
    logger.debug(str(r.headers))
    logger.debug(str(os.environ))
    
    return Response(message="hi")


@app.get("/health")
def health():
    return "health"


# Override defalut HTTPException handler.
@app.exception_handler(HTTPException)
def hundle_http_exception(request: Request, exc: HTTPException):
    response = JSONResponse(
        content={
            "message": str(exc.detail),
            "type": None,
        },
        status_code=exc.status_code,
    )

    return response


# Override defalut RequestValidationError handler.
@app.exception_handler(RequestValidationError)
def hundle_request_validation_error(request: Request, exc: RequestValidationError):
    
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": exc.errors()[0]["msg"],
            "type": exc.errors()[0]["type"],
        },
    )

    return response


# Hundle 404 error.
@app.exception_handler(404)
def hundle_request_validation_error(request: Request, exc: HTTPException):
    
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Not found",
            "type": "not_found",
        },
    )

    return response


# Hundle other Python exceptions.
@app.exception_handler(Exception)
def hundle_other_exeptions(request: Request, exc: Exception):
    response = JSONResponse(
        content={
            "message": f"{exc.__class__.__name__}: {str(exc)}",
            "type": "internal_server_error",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return response
