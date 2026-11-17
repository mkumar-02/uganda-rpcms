from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PPersonSchema,
    G2PGeoSchema,
    G2PRegisterHistorySchema,
    G2PPersonHistorySchema,
    G2PGeoHistorySchema,
    G2PIntakeFormSchemaBase,
)
from .address import G2PAddressLinesSchema
from ..models.enums import (
    DisabilitySeverityEnum,
    DisabilityTypeEnum,
    DisplacementStatusEnum,
    EducationalLevelEnum,
)


class G2PSchemaRefugee:

    progres_id: Optional[str] = None
    progres_id_valid_to: Optional[date] = None
    estimated_age: Optional[int] = None
    country_of_origin: Optional[str] = None
    arrival_date: Optional[date] = None
    displacement_status: Optional[DisplacementStatusEnum] = None
    settlement_code: Optional[str] = None
    zone_code: Optional[str] = None
    has_personal_phone: Optional[bool] = None
    language_spoken: Optional[str] = None
    education_level: Optional[EducationalLevelEnum] = None
    disabled: Optional[bool] = None
    disability_type: Optional[DisabilityTypeEnum] = None
    disability_severity: Optional[DisabilitySeverityEnum] = None


class G2PRegisterSchemaRefugee(
    G2PRegisterBaseSchema,
    G2PPersonSchema,
    G2PGeoSchema,
    G2PAddressLinesSchema,
    G2PSchemaRefugee,
):
    """Schema for Refugee register."""


class G2PRegisterHistorySchemaRefugee(
    G2PRegisterHistorySchema, G2PPersonHistorySchema, G2PGeoHistorySchema
):
    """Schema for Refugee history."""


class G2PIntakeFormSchemaRefugee(
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PPersonSchema,
    G2PGeoSchema,
    G2PAddressLinesSchema,
    G2PSchemaRefugee,
):
    """Schema for Refugee intake form."""
