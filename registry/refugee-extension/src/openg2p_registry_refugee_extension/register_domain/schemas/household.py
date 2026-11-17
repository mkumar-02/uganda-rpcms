from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PGeoSchema,
    G2PRegisterHistorySchema,
    G2PGeoHistorySchema,
    G2PIntakeFormSchemaBase,
)
from .address import G2PAddressLinesSchema


class G2PSchemaHousehold:

    household_head: Optional[str] = None
    size_of_group: Optional[int] = None
    number_of_children: Optional[int] = None
    number_of_elderly_members: Optional[int] = None
    number_of_female_members: Optional[int] = None
    number_of_male_members: Optional[int] = None
    settlement_code: Optional[str] = None
    zone_code: Optional[str] = None


class G2PRegisterSchemaHousehold(
    G2PRegisterBaseSchema, G2PGeoSchema, G2PAddressLinesSchema, G2PSchemaHousehold
):
    """Schema for Household register."""


class G2PRegisterHistorySchemaHousehold(G2PRegisterHistorySchema, G2PGeoHistorySchema):
    """Schema for Household history."""


class G2PIntakeFormSchemaHousehold(
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PGeoSchema,
    G2PAddressLinesSchema,
    G2PSchemaHousehold,
):
    """Schema for Household intake form."""
