from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .ngo import NgoCreate


class OnboardRequest(NgoCreate):
    """Create partner + onboarding request in one step."""

    submitted_by: Optional[str] = None


class DecisionRequest(BaseModel):
    comment: Optional[str] = None
    decided_by: Optional[str] = "staff"


class RequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ngo_id: str
    request_type: str
    status: str
    submitted_by: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None
    decision_comment: Optional[str] = None
    awe_instance_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class RequestDetailResponse(RequestResponse):
    ngo_name: Optional[str] = None
    message: str = Field(default="")


class RequestListResponse(BaseModel):
    count: int
    requests: list[RequestDetailResponse]
