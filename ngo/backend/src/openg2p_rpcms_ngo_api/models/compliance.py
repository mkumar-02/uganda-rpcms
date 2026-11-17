from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelWithId
from .enums import ComplianceCheckKind, ComplianceCheckStatus


class ComplianceCheckORM(BaseModelWithId):
    """Automated / manual bureau verification against an onboarding request."""

    __tablename__ = "compliance_checks"

    request_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    ngo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String, nullable=False)  # ComplianceCheckKind
    status: Mapped[str] = mapped_column(
        String, default=ComplianceCheckStatus.pending.value
    )
    reference_number: Mapped[Optional[str]] = mapped_column(String)
    checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
    raw_result: Mapped[Optional[str]] = mapped_column(Text)  # JSON string from adapter
    message: Mapped[Optional[str]] = mapped_column(Text)
