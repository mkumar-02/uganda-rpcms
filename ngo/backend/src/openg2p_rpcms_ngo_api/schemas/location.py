from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    kind: str = "admin_large"
    name: str
    code: Optional[str] = None
    parent_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None


class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ngo_id: str
    kind: str
    name: str
    code: Optional[str] = None
    parent_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class LocationListResponse(BaseModel):
    count: int
    locations: list[LocationResponse]
