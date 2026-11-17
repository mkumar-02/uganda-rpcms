from typing import Optional

from .registry import G2PRegistryPayload


class G2PRegisterHouseholdPayload(G2PRegistryPayload):
    functional_record_id: Optional[str] = None
    household_head: Optional[str] = None
    size_of_group: Optional[int] = None
    number_of_children: Optional[int] = None
    number_of_elderly_members: Optional[int] = None
    number_of_female_members: Optional[int] = None
    number_of_male_members: Optional[int] = None
    settlement_code: Optional[str] = None
    zone_code: Optional[str] = None
