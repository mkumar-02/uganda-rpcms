from typing import Optional

from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModelWithId
from .enums import LocationKind


class NgoLocationORM(BaseModelWithId):
    """Operating geography for a partner (settlement / zone / service point)."""

    __tablename__ = "ngo_locations"

    ngo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String, default=LocationKind.admin_large.value)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String, index=True)
    parent_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    notes: Mapped[Optional[str]] = mapped_column(Text)
