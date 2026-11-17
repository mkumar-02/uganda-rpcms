from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelWithId
from .enums import RequestStatus, RequestType


class NgoRequestORM(BaseModelWithId):
    """Partner onboarding / change request."""

    __tablename__ = "ngo_requests"

    ngo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    request_type: Mapped[str] = mapped_column(
        String, default=RequestType.onboarding.value, index=True
    )
    status: Mapped[str] = mapped_column(
        String, default=RequestStatus.created.value, index=True
    )
    submitted_by: Mapped[Optional[str]] = mapped_column(String)
    decided_by: Mapped[Optional[str]] = mapped_column(String)
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
    decision_comment: Mapped[Optional[str]] = mapped_column(Text)
    # Optional AWE workflow instance id when awe_enabled.
    awe_instance_id: Mapped[Optional[str]] = mapped_column(String)
