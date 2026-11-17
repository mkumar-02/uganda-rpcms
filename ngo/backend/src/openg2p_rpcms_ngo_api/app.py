# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .controllers import NgoController, RequestController
from .migrations import migrate_all
from .services import (
    LocationService,
    MouService,
    NgoService,
    ProvisionerService,
    RequestService,
)

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        NgoService()
        MouService()
        LocationService()
        ProvisionerService()
        RequestService()
        RequestController().post_init()
        NgoController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)
        asyncio.run(migrate_all())
