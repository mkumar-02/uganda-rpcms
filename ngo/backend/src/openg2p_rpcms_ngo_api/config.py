from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="rpcms_ngo_", env_file=".env", extra="allow"
    )

    openapi_title: str = "RPCMS Partner Onboarding API"
    openapi_description: str = "Uganda RPCMS partner onboarding"
    openapi_version: str = __version__

    # Reserved for AWE integration (webhook callback URL).
    awe_base_url: str = ""
    awe_enabled: bool = False

    # Provisioning stubs — real Registry/PBMS connectors plug in later.
    registry_provision_enabled: bool = False
    pbms_provision_enabled: bool = False
