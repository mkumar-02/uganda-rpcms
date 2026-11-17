import logging

from .config import Settings
from .models import ComplianceCheckORM, MouORM, NgoLocationORM, NgoORM, NgoRequestORM

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


async def migrate_all():
    _logger.info("Migrating RPCMS partner onboarding database")
    await NgoORM.create_migrate()
    await NgoRequestORM.create_migrate()
    await ComplianceCheckORM.create_migrate()
    await MouORM.create_migrate()
    await NgoLocationORM.create_migrate()
