from openg2p_fastapi_common.context import dbengine
from sqlalchemy.ext.asyncio import async_sessionmaker


def session_maker():
    return async_sessionmaker(dbengine.get(), expire_on_commit=False)
