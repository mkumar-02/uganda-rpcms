from datetime import date
from typing import Optional

from .registry import G2PRegistryPayload


class G2PRefugeeRegistryPayload(G2PRegistryPayload):
    functional_record_id: Optional[str] = None
    progres_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    estimated_age: Optional[int] = None
    settlement_code: Optional[str] = None
    zone_code: Optional[str] = None
    country_of_origin: Optional[str] = None
    arrival_date: Optional[date] = None
    displacement_status: Optional[str] = None
    disabled: Optional[bool] = None
    education_level: Optional[str] = None
