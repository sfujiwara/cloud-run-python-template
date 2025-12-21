import logging

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingFilter, StructuredLogHandler
from opentelemetry.instrumentation.logging import LoggingInstrumentor


class CloudTraceFilter(CloudLoggingFilter):
    def __init__(self):
        super(CloudTraceFilter, self).__init__()
        self.project = google.cloud.logging.Client().project

    def filter(self, record) -> bool:
        record.trace = f"projects/{self.project}/traces/{record._trace}" # noqa: SLF001

        super().filter(record)

        return True


def setup_structured_logging() -> None:
    # LoggingInstrumentor().instrument()

    structured_log_handler = StructuredLogHandler()
    structured_log_handler.addFilter(CloudTraceFilter())
    handlers = [structured_log_handler]

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers,
    )
