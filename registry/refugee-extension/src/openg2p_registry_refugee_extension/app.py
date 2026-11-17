# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_registry_core.app import Initializer as CoreInitializer

from .register_domain.models import (
    G2PRegisterRefugee,
    G2PRegisterHistoryRefugee,
    G2PIntakeFormRefugee,
    G2PRegisterHousehold,
    G2PRegisterHistoryHousehold,
    G2PIntakeFormHousehold,
    G2PRegisterHouseholdMember,
    G2PRegisterHistoryHouseholdMember,
    G2PIntakeFormHouseholdMember,
    G2PRegisterSelfRelianceSurvey,
    G2PRegisterHistorySelfRelianceSurvey,
    G2PIntakeFormSelfRelianceSurvey,
)
from .register_domain.services import (
    G2PRegisterDomainServiceRefugee,
    G2PRegisterDomainServiceHousehold,
    G2PRegisterDomainServiceHouseholdMember,
    G2PRegisterDomainServiceSelfRelianceSurvey,
)

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        G2PRegisterDomainServiceRefugee()
        G2PRegisterDomainServiceHousehold()
        G2PRegisterDomainServiceHouseholdMember()
        G2PRegisterDomainServiceSelfRelianceSurvey()

    def migrate_database(self, args):
        async def migrate():
            _logger.info("Migrating refugee registry extension database")

            await G2PRegisterHousehold.create_migrate()
            await G2PRegisterHistoryHousehold.create_migrate()
            await G2PIntakeFormHousehold.create_migrate()

            await G2PRegisterHouseholdMember.create_migrate()
            await G2PRegisterHistoryHouseholdMember.create_migrate()
            await G2PIntakeFormHouseholdMember.create_migrate()

            await G2PRegisterRefugee.create_migrate()
            await G2PRegisterHistoryRefugee.create_migrate()
            await G2PIntakeFormRefugee.create_migrate()

            await G2PRegisterSelfRelianceSurvey.create_migrate()
            await G2PRegisterHistorySelfRelianceSurvey.create_migrate()
            await G2PIntakeFormSelfRelianceSurvey.create_migrate()

        asyncio.run(migrate())
