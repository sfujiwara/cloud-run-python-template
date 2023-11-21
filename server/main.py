import logging
import os
import requests

from fastapi import FastAPI
from fastapi.requests import Request
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

    return Response(message="hi")


@app.get("/health")
def health():
    return "health"
