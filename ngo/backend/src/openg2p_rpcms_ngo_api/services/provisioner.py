"""Provisioning stubs for Registry Agent + PBMS Agency/Program.

When registry_provision_enabled / pbms_provision_enabled are true, replace the
ID generators with real HTTP clients against those platforms.
"""

from __future__ import annotations

import logging
import uuid

from openg2p_fastapi_common.service import BaseService

from ..config import Settings
from ..models import NgoORM

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class ProvisionerService(BaseService):
    """Creates downstream identifiers after staff / AWE approval."""

    async def provision_after_approval(self, ngo: NgoORM) -> NgoORM:
        code = (ngo.short_code or ngo.name[:8] or "NGO").upper().replace(" ", "-")

        if not ngo.registry_agent_id:
            ngo.registry_agent_id = self._registry_agent_id(code)
            _logger.info(
                "Provisioned Registry Agent %s for partner %s",
                ngo.registry_agent_id,
                ngo.id,
            )

        if not ngo.pbms_agency_id:
            ngo.pbms_agency_id = self._pbms_agency_id(code)
            _logger.info(
                "Provisioned PBMS Agency %s for partner %s",
                ngo.pbms_agency_id,
                ngo.id,
            )

        if not ngo.pbms_program_id:
            ngo.pbms_program_id = self._pbms_program_id(code)
            _logger.info(
                "Provisioned PBMS Program %s for partner %s",
                ngo.pbms_program_id,
                ngo.id,
            )
        return ngo

    def _registry_agent_id(self, code: str) -> str:
        if _config.registry_provision_enabled:
            # Placeholder for live Registry Agent API call.
            return f"agent-{code.lower()}-{uuid.uuid4().hex[:8]}"
        return f"stub-agent-{code.lower()}-{uuid.uuid4().hex[:8]}"

    def _pbms_agency_id(self, code: str) -> str:
        if _config.pbms_provision_enabled:
            return f"agency-{code.lower()}-{uuid.uuid4().hex[:8]}"
        return f"stub-agency-{code.lower()}-{uuid.uuid4().hex[:8]}"

    def _pbms_program_id(self, code: str) -> str:
        if _config.pbms_provision_enabled:
            return f"program-{code.lower()}-{uuid.uuid4().hex[:8]}"
        return f"stub-program-{code.lower()}-{uuid.uuid4().hex[:8]}"
