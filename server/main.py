import logging
import os
import requests

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from google.cloud.logging.handlers import StructuredLogHandler
from pydantic import BaseModel, Field


app = FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(StructuredLogHandler())


def get_project_id() -> str:
    """Get GCP project ID from meta data server.

    Returns:
        str: GCP project ID.
    """

    res = requests.get(
        url="http://metadata/computeMetadata/v1/project/project-id",
        headers={"Metadata-Flavor": "Google"}
    )
    project_id = str(res.content, "utf-8")

    return project_id


def get_trace(request: Request) -> str:
    """Get trace ID from HTTP request instance.

    """
    x_cloud_trace_context = request.headers.get("x-cloud-trace-context")

    if x_cloud_trace_context:
        project_id = get_project_id()
        trace_id = x_cloud_trace_context.split("/")[0]
        return f"projects/{project_id}/traces/{trace_id}"
    else:
        return ""


class RootRequest(BaseModel):
    message: str = Field()


class Response(BaseModel):
    message: str = Field()


@app.post("/")
async def main(
    request: RootRequest,
    r: Request,
) -> Response:
    trace = get_trace(request=r)

    logger.info(str(os.environ), extra={"trace": trace})
    logger.info(str(r.headers), extra={"trace": trace})
    logger.info("hello", extra={"trace": trace})
    logger.info("world", extra={"trace": trace})
    # raise ValueError("raise value error")
    raise HTTPException(status_code=500, detail="error")
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
