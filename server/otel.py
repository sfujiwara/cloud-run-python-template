import os

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# https://docs.cloud.google.com/trace/docs/setup/python-ot#config-otel
def setup_opentelemetry() -> None:
    """Set up OpenTelemetry tracing and logging instrumentation."""
    resource = Resource.create(
        attributes={
            SERVICE_INSTANCE_ID: f"worker-{os.getpid()}",
        },
    )
    tracer_provider = TracerProvider(resource=resource)
    trace_exporter = CloudTraceSpanExporter()
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)
