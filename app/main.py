from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Request(BaseModel):
    message: str = Field()


class Response(BaseModel):
    message: str = Field()


@app.post("/")
async def main(request: Request) -> Response:
    return Response(message="hi")


@app.get("/")
def healthz():
    return "ok"


@app.get("/hello")
def healthz():
    return "hello"


@app.get("/health")
def healthz():
    return "health"


@app.get("/healthz")
def healthz():
    return "healthz"
