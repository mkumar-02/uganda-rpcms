import uuid
from datetime import datetime, timezone
from typing import Optional

from openg2p_fastapi_common.models import BaseORMModel
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


class BaseModelWithId(BaseORMModel):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=_utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=_utcnow, onupdate=_utcnow
    )

    def __init__(self, **kwargs):
        if kwargs.get("id") is None:
            kwargs["id"] = str(uuid.uuid4())
        super().__init__(**kwargs)
