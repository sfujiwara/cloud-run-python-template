from starlette.middleware.base import BaseHTTPMiddleware
from .context import cloud_trace_context


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        cloud_trace_context.set(request.headers.get("x-cloud-trace-context"))
        response = await call_next(request)

        return response
