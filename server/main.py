import logging
import os

import google.cloud.logging
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel, Field

from .logging import setup_structured_logging
from .otel import setup_opentelemetry

logger = logging.getLogger(__name__)

setup_opentelemetry()
setup_structured_logging()

app = FastAPI()

FastAPIInstrumentor().instrument_app(app)

class RootRequest(BaseModel):
    message: str = Field()


class Response(BaseModel):
    message: str = Field()


@app.post("/")
def main(
    request: RootRequest,
    r: Request,
) -> Response:
    client = google.cloud.logging.Client()
    logger.info(f"project: {client.project}")
    logger.info("hello")
    logger.debug(str(r.headers))
    logger.debug(str(os.environ))

    return Response(message="hi")


@app.get("/health")
def health() -> str:
    tracer = trace.get_tracer_provider().get_tracer(__name__)
    logger.info("health check 0")
    with tracer.start_as_current_span("get_sample"):
        logger.info("health check 1")
        logger.warning("health check 2")
        logger.error("health check 3")
        print("hello")

        return "health"


# Override defalut HTTPException handler.
@app.exception_handler(HTTPException)
def hundle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content={
            "message": str(exc.detail),
            "type": None,
        },
        status_code=exc.status_code,
    )


# Override defalut RequestValidationError handler.
@app.exception_handler(RequestValidationError)
def hundle_request_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": exc.errors()[0]["msg"],
            "type": exc.errors()[0]["type"],
        },
    )


# Hundle 404 error.
@app.exception_handler(404)
def hundle_404_error(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "Not found",
            "type": "not_found",
        },
    )


# Hundle other Python exceptions.
@app.exception_handler(Exception)
def hundle_other_exeptions(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": f"{exc.__class__.__name__}: {str(exc)}",
            "type": "internal_server_error",
        },
    )
