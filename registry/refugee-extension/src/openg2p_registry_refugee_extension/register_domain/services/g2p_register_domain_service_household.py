import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import as_int, fallback_record_name, is_blank, validation_error

_logger = logging.getLogger("g2p-register-domain-service")

_REQUIRED_FIELDS = {
    "size_of_group": "Size of Group",
    "number_of_male_members": "Number of Male Members",
    "number_of_female_members": "Number of Female Members",
}

_INFO_FIELDS = (
    "size_of_group",
    "number_of_male_members",
    "number_of_female_members",
    "number_of_children",
    "number_of_elderly_members",
    "settlement_code",
    "zone_code",
)


class G2PRegisterDomainServiceHousehold(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            if not any(field in record for field in _INFO_FIELDS):
                continue
            self._validate_required(record)
            self._validate_household_size(record)

    def _validate_required(self, record: dict) -> None:
        missing = [
            label
            for field, label in _REQUIRED_FIELDS.items()
            if is_blank(record.get(field))
        ]
        if missing:
            validation_error(f"Required household fields missing: {', '.join(missing)}")

    def _validate_household_size(self, record: dict) -> None:
        size_of_group = as_int(record.get("size_of_group"))
        male = as_int(record.get("number_of_male_members"))
        female = as_int(record.get("number_of_female_members"))
        for label, value in (
            ("size_of_group", size_of_group),
            ("number_of_male_members", male),
            ("number_of_female_members", female),
        ):
            if value is None:
                validation_error(f"{label} must be a whole number")
            if value < 0:
                validation_error(f"{label} must not be negative")
        if size_of_group < 1:
            validation_error("size_of_group must be at least 1")
        if male + female > size_of_group:
            validation_error(
                "number_of_male_members + number_of_female_members must not exceed size_of_group"
            )

        children = as_int(record.get("number_of_children"))
        if children is not None and (children < 0 or children > size_of_group):
            validation_error("number_of_children must be between 0 and size_of_group")

        elderly = as_int(record.get("number_of_elderly_members"))
        if elderly is not None and (elderly < 0 or elderly > size_of_group):
            validation_error(
                "number_of_elderly_members must be between 0 and size_of_group"
            )

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for household")
        keys = [
            "functional_record_id",
            "record_name",
            "household_head",
            "settlement_code",
            "zone_code",
            "address_line_1",
            "address_line_2",
            "postal_code",
            "country_code",
        ]
        search_text = []
        if extra:
            search_text.extend(str(v).strip() for v in extra if str(v).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for household")
        keys = ["household_head", "functional_record_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        return " ".join(record_name).strip() or fallback_record_name(payload, "Household")
