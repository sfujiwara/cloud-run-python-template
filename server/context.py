import contextvars


cloud_trace_context = contextvars.ContextVar("cloud_trace_context", default="")
http_request_context = contextvars.ContextVar("http_request_context", default=dict({}))
