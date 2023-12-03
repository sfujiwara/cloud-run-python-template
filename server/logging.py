import logging
import os
import requests
from typing import Optional

from google.cloud.logging.handlers import CloudLoggingFilter
from .context import cloud_trace_context


def get_project_id() -> Optional[str]:
    """Get GCP project ID from meta data server.

    Returns:
        str: GCP project ID.
    """

    if "K_REVISION" in os.environ.keys():
        res = requests.get(
            url="http://metadata/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"}
        )
        project_id = str(res.content, "utf-8")
    else:
        project_id = None

    return project_id


class CloudTraceFilter(CloudLoggingFilter):
    def __init__(self):
        super(CloudTraceFilter, self).__init__()
        self.project = get_project_id()

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
