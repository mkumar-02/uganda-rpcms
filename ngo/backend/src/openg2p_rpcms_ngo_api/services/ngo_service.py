import logging
from typing import Optional

from openg2p_fastapi_common.service import BaseService
from sqlalchemy import select

from ..config import Settings
from ..errors import NgoExistsError, NgoNotFoundError
from ..models import NgoORM, NgoStatus
from ..schemas import NgoCreate, NgoUpdate
from .db import session_maker

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class NgoService(BaseService):
    async def get(self, ngo_id: str) -> NgoORM | None:
        async with session_maker()() as session:
            res = await session.execute(select(NgoORM).where(NgoORM.id == ngo_id))
            return res.scalars().first()

    async def get_by_short_code(self, short_code: str) -> NgoORM | None:
        async with session_maker()() as session:
            res = await session.execute(
                select(NgoORM).where(NgoORM.short_code == short_code)
            )
            return res.scalars().first()

    async def list_ngos(self, status: Optional[str] = None) -> list[NgoORM]:
        async with session_maker()() as session:
            stmt = select(NgoORM).order_by(NgoORM.created_at.desc())
            if status:
                stmt = stmt.where(NgoORM.status == status)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def create(self, data: NgoCreate) -> NgoORM:
        if data.short_code and await self.get_by_short_code(data.short_code):
            raise NgoExistsError(data.short_code)

        async with session_maker()() as session:
            ngo = NgoORM(
                name=data.name,
                short_code=data.short_code,
                registration_number=data.registration_number,
                ursb_number=data.ursb_number,
                ngo_bureau_number=data.ngo_bureau_number,
                contact_email=data.contact_email,
                contact_phone=data.contact_phone,
                legal_address=data.legal_address,
                notes=data.notes,
                status=NgoStatus.created.value,
            )
            session.add(ngo)
            await session.commit()
            await session.refresh(ngo)
            return ngo

    async def update(self, ngo_id: str, data: NgoUpdate) -> NgoORM:
        async with session_maker()() as session:
            res = await session.execute(select(NgoORM).where(NgoORM.id == ngo_id))
            ngo = res.scalars().first()
            if not ngo:
                raise NgoNotFoundError(ngo_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(ngo, field, value)
            await session.commit()
            await session.refresh(ngo)
            return ngo

    async def set_status(self, ngo_id: str, status: NgoStatus) -> NgoORM:
        async with session_maker()() as session:
            res = await session.execute(select(NgoORM).where(NgoORM.id == ngo_id))
            ngo = res.scalars().first()
            if not ngo:
                raise NgoNotFoundError(ngo_id)
            ngo.status = status.value
            await session.commit()
            await session.refresh(ngo)
            return ngo
