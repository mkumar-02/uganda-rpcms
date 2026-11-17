from ..dci import identifier_value
from ..models import G2PRefugeeRegistry
from ..schema import G2PRefugeeRegistryPayload
from ._base import RegistryDB, RegistryDCI
from ._dci_records import as_bool
from ._summary import RefugeeSummaries


class RefugeeDB(RefugeeSummaries, RegistryDB):
    model = G2PRefugeeRegistry
    payload = G2PRefugeeRegistryPayload


class RefugeeDCI(RefugeeSummaries, RegistryDCI):
    payload = G2PRefugeeRegistryPayload
    reg_type = "Refugee"
    reg_record_type = "Refugee"
    match_field = "progres_id"
    fields = {
        "progres_id",
        "first_name",
        "middle_name",
        "last_name",
        "gender",
        "birth_date",
        "phone_numbers",
        "settlement_code",
        "zone_code",
        "country_of_origin",
        "arrival_date",
        "displacement_status",
        "disabled",
        "education_level",
        "language_spoken",
    }

    @staticmethod
    def flat(record: dict) -> dict:
        personal = record.get("refugee_personal_details") or record.get(
            "personal_details"
        ) or {}
        demographic = personal.get("demographic_info") or {}
        name = demographic.get("name") or {}
        location = record.get("location") or {}
        return {
            "progres_id": identifier_value(
                record,
                ("refugee_personal_details", "progres_id"),
                ("progres_id",),
            )
            or personal.get("progres_id"),
            "first_name": name.get("given_name"),
            "middle_name": name.get("second_name"),
            "last_name": name.get("surname"),
            "gender": demographic.get("sex"),
            "birth_date": demographic.get("birth_date"),
            "phone_numbers": demographic.get("phone_number"),
            "settlement_code": location.get("settlement_code"),
            "zone_code": location.get("zone_code"),
            "country_of_origin": personal.get("country_of_origin"),
            "arrival_date": personal.get("arrival_date"),
            "displacement_status": personal.get("displacement_status"),
            "disabled": as_bool(personal.get("disabled")),
            "education_level": personal.get("education_level"),
            "language_spoken": personal.get("language_spoken"),
        }
