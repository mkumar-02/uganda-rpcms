from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelWithId
from .enums import MouStatus


class MouORM(BaseModelWithId):
    """Memorandum of Understanding (UGPass e-sign can attach later)."""

    __tablename__ = "mous"

    ngo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    request_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default=MouStatus.draft.value)
    document_uri: Mapped[Optional[str]] = mapped_column(String)  # object store / URL
    signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
    effective_from: Mapped[Optional[date]] = mapped_column(Date)
    effective_to: Mapped[Optional[date]] = mapped_column(Date)
    notes: Mapped[Optional[str]] = mapped_column(Text)
