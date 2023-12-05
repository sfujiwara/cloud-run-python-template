import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingFilter
from .context import cloud_trace_context


class CloudTraceFilter(CloudLoggingFilter):
    def __init__(self):
        super(CloudTraceFilter, self).__init__()
        self.project = google.cloud.logging.Client().project

    def filter(self, record):
        ctc = cloud_trace_context.get()

        if ctc:
            trace_id = ctc.split("/")[0]
            trace = f"projects/{self.project}/traces/{trace_id}"
        else:
            trace = ""

        record.trace = trace

        super().filter(record)

        return True
