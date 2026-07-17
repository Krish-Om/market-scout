from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel


class ScoutRequest(BaseModel):
    topic: str = "Clean Beauty and Preventive Wellness"


class ScoutResponse(BaseModel):
    job_id: str
    status: str
    message: str
