from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NgoCreate(BaseModel):
    name: str
    short_code: Optional[str] = None
    registration_number: Optional[str] = None
    ursb_number: Optional[str] = None
    ngo_bureau_number: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    legal_address: Optional[str] = None
    notes: Optional[str] = None


class NgoUpdate(BaseModel):
    name: Optional[str] = None
    registration_number: Optional[str] = None
    ursb_number: Optional[str] = None
    ngo_bureau_number: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    legal_address: Optional[str] = None
    notes: Optional[str] = None


class NgoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    short_code: Optional[str] = None
    registration_number: Optional[str] = None
    ursb_number: Optional[str] = None
    ngo_bureau_number: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    legal_address: Optional[str] = None
    status: str
    registry_agent_id: Optional[str] = None
    pbms_agency_id: Optional[str] = None
    pbms_program_id: Optional[str] = None
    approved_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class NgoListResponse(BaseModel):
    count: int
    ngos: list[NgoResponse]


class NgoActionResponse(BaseModel):
    ngo_id: str
    status: str
    message: str = Field(default="")
    registry_agent_id: Optional[str] = None
    pbms_agency_id: Optional[str] = None
    pbms_program_id: Optional[str] = None
