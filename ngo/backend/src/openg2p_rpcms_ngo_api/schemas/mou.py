from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MouCreate(BaseModel):
    title: str
    document_uri: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None
    request_id: Optional[str] = None
    mark_signed: bool = False


class MouSignRequest(BaseModel):
    document_uri: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None


class MouResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ngo_id: str
    request_id: Optional[str] = None
    title: str
    status: str
    document_uri: Optional[str] = None
    signed_at: Optional[datetime] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class MouListResponse(BaseModel):
    count: int
    mous: list[MouResponse]
