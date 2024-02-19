"""Post request model for JanusAPI."""

from pydantic import BaseModel


class CreateCollectQCRequest(BaseModel):
    case_id: str
    samples: list[str]
    file_names: list[str]
    workflow: str
