from pydantic import BaseModel
from typing import Literal, Any

class JobSpec(BaseModel):
    job_type: Literal["document_analysis", "log_analysis"]
    objective: str
    inputs: dict
    constraints: dict | None = None
    output_format: str

class JobResult(BaseModel):
    status: Literal["QUEUED", "RUNNING", "COMPLETE", "FAILED"]
    result: Any | None = None