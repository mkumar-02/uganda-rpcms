from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelWithId
from .enums import NgoStatus


class NgoORM(BaseModelWithId):
    """Partner master record (maps to Registry Agent + PBMS Agency)."""

    __tablename__ = "ngos"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    short_code: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True)
    registration_number: Mapped[Optional[str]] = mapped_column(String, index=True)
    ursb_number: Mapped[Optional[str]] = mapped_column(String)
    ngo_bureau_number: Mapped[Optional[str]] = mapped_column(String)
    contact_email: Mapped[Optional[str]] = mapped_column(String)
    contact_phone: Mapped[Optional[str]] = mapped_column(String)
    legal_address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String, default=NgoStatus.created.value, index=True
    )
    # Set after AWE / staff approval — used by Registry Agent + PBMS Agency provisioners.
    registry_agent_id: Mapped[Optional[str]] = mapped_column(String)
    pbms_agency_id: Mapped[Optional[str]] = mapped_column(String)
    pbms_program_id: Mapped[Optional[str]] = mapped_column(String)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
    notes: Mapped[Optional[str]] = mapped_column(Text)
