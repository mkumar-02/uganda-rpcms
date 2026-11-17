import logging

from openg2p_fastapi_common.service import BaseService
from sqlalchemy import select

from ..config import Settings
from ..errors import LocationNotFoundError, NgoNotFoundError
from ..models import NgoLocationORM, NgoORM
from ..schemas import LocationCreate
from .db import session_maker

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class LocationService(BaseService):
    async def list_for_ngo(self, ngo_id: str) -> list[NgoLocationORM]:
        async with session_maker()() as session:
            res = await session.execute(
                select(NgoLocationORM)
                .where(NgoLocationORM.ngo_id == ngo_id)
                .order_by(NgoLocationORM.name)
            )
            return list(res.scalars().all())

    async def create(self, ngo_id: str, data: LocationCreate) -> NgoLocationORM:
        async with session_maker()() as session:
            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == ngo_id))
            ).scalars().first()
            if not ngo:
                raise NgoNotFoundError(ngo_id)

            loc = NgoLocationORM(
                ngo_id=ngo_id,
                kind=data.kind,
                name=data.name,
                code=data.code,
                parent_id=data.parent_id,
                latitude=data.latitude,
                longitude=data.longitude,
                notes=data.notes,
            )
            session.add(loc)
            await session.commit()
            await session.refresh(loc)
            return loc

    async def delete(self, location_id: str) -> None:
        async with session_maker()() as session:
            res = await session.execute(
                select(NgoLocationORM).where(NgoLocationORM.id == location_id)
            )
            loc = res.scalars().first()
            if not loc:
                raise LocationNotFoundError(location_id)
            await session.delete(loc)
            await session.commit()
