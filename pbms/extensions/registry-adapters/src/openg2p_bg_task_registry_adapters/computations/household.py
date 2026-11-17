from ..dci import identifier_value
from ..models import G2PRegisterHousehold
from ..schema import G2PRegisterHouseholdPayload
from ._base import RegistryDB, RegistryDCI
from ._dci_records import as_int
from ._summary import HouseholdSummaries


class HouseholdDB(HouseholdSummaries, RegistryDB):
    model = G2PRegisterHousehold
    payload = G2PRegisterHouseholdPayload


class HouseholdDCI(HouseholdSummaries, RegistryDCI):
    payload = G2PRegisterHouseholdPayload
    reg_type = "Household"
    reg_record_type = "Household"
    match_field = "functional_record_id"
    fields = {
        "functional_record_id",
        "household_head",
        "size_of_group",
        "number_of_children",
        "number_of_elderly_members",
        "number_of_female_members",
        "number_of_male_members",
        "settlement_code",
        "zone_code",
    }

    @staticmethod
    def flat(record: dict) -> dict:
        family = record.get("family_details") or {}
        location = record.get("location") or {}
        head = (
            (family.get("group_head_info") or {}).get("demographic_info") or {}
        ).get("name") or {}
        return {
            "functional_record_id": identifier_value(
                record, ("family_details", "group_identifier")
            ),
            "household_head": head.get("given_name") or family.get("household_head"),
            "size_of_group": as_int(family.get("group_size") or family.get("size_of_group")),
            "number_of_children": as_int(family.get("number_of_children")),
            "number_of_elderly_members": as_int(family.get("number_of_elderly_members")),
            "number_of_female_members": as_int(family.get("number_of_female_members")),
            "number_of_male_members": as_int(family.get("number_of_male_members")),
            "settlement_code": location.get("settlement_code"),
            "zone_code": location.get("zone_code"),
        }
