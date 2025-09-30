from pydantic import BaseModel

class StatusResponse(BaseModel):
    """Model for status endpoint response."""
    status: str