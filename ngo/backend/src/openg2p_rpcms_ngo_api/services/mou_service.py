import logging
from datetime import datetime, timezone
from typing import Optional

from openg2p_fastapi_common.service import BaseService
from sqlalchemy import or_, select

from ..config import Settings
from ..errors import MouNotFoundError, NgoNotFoundError
from ..models import MouORM, MouStatus, NgoORM
from ..schemas import MouCreate, MouSignRequest
from .db import session_maker

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


def _utcnow():
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


class MouService(BaseService):
    async def list_for_ngo(self, ngo_id: str) -> list[MouORM]:
        async with session_maker()() as session:
            res = await session.execute(
                select(MouORM)
                .where(MouORM.ngo_id == ngo_id)
                .order_by(MouORM.created_at.desc())
            )
            return list(res.scalars().all())

    async def get(self, mou_id: str) -> MouORM | None:
        async with session_maker()() as session:
            res = await session.execute(select(MouORM).where(MouORM.id == mou_id))
            return res.scalars().first()

    async def create(self, ngo_id: str, data: MouCreate) -> MouORM:
        async with session_maker()() as session:
            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == ngo_id))
            ).scalars().first()
            if not ngo:
                raise NgoNotFoundError(ngo_id)

            status = MouStatus.signed.value if data.mark_signed else MouStatus.draft.value
            mou = MouORM(
                ngo_id=ngo_id,
                request_id=data.request_id,
                title=data.title,
                status=status,
                document_uri=data.document_uri,
                effective_from=data.effective_from,
                effective_to=data.effective_to,
                notes=data.notes,
                signed_at=_utcnow() if data.mark_signed else None,
            )
            session.add(mou)
            await session.commit()
            await session.refresh(mou)
            return mou

    async def mark_signed(self, mou_id: str, data: Optional[MouSignRequest] = None) -> MouORM:
        async with session_maker()() as session:
            res = await session.execute(select(MouORM).where(MouORM.id == mou_id))
            mou = res.scalars().first()
            if not mou:
                raise MouNotFoundError(mou_id)
            mou.status = MouStatus.signed.value
            mou.signed_at = _utcnow()
            if data:
                if data.document_uri is not None:
                    mou.document_uri = data.document_uri
                if data.effective_from is not None:
                    mou.effective_from = data.effective_from
                if data.effective_to is not None:
                    mou.effective_to = data.effective_to
            await session.commit()
            await session.refresh(mou)
            return mou

    async def has_signed_mou(self, ngo_id: str, request_id: Optional[str] = None) -> bool:
        async with session_maker()() as session:
            stmt = select(MouORM).where(
                MouORM.ngo_id == ngo_id, MouORM.status == MouStatus.signed.value
            )
            if request_id:
                stmt = stmt.where(
                    or_(MouORM.request_id == request_id, MouORM.request_id.is_(None))
                )
            res = await session.execute(stmt)
            return res.scalars().first() is not None
