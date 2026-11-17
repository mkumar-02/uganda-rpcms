from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComplianceCheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    request_id: str
    ngo_id: str
    kind: str
    status: str
    reference_number: Optional[str] = None
    checked_at: Optional[datetime] = None
    message: Optional[str] = None
    created_at: datetime


class ComplianceRunResponse(BaseModel):
    request_id: str
    all_passed: bool
    checks: list[ComplianceCheckResponse]
