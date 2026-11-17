import logging
import re
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    fallback_record_name,
    is_blank,
    parse_date,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")

# ProGres individual IDs in the RPCMS demo look like UGA-00423318.
_PROGRES_ID_RE = re.compile(r"^[A-Z]{3}-\d{5,12}$", re.IGNORECASE)


def _enum_fields() -> dict:
    from ..models.enums import (
        DisabilitySeverityEnum,
        DisabilityTypeEnum,
        DisplacementStatusEnum,
        EducationalLevelEnum,
    )

    return {
        "disability_type": DisabilityTypeEnum,
        "disability_severity": DisabilitySeverityEnum,
        "displacement_status": DisplacementStatusEnum,
        "education_level": EducationalLevelEnum,
    }


class G2PRegisterDomainServiceRefugee(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            self._validate_birth_date(record)
            self._validate_progres_id(record)
            self._validate_arrival_date(record)

    def _validate_birth_date(self, record: dict) -> None:
        birth_date = parse_date(record.get("birth_date"))
        if birth_date is not None and birth_date > date.today():
            validation_error("birth_date must not be in the future")

    def _validate_arrival_date(self, record: dict) -> None:
        arrival_date = parse_date(record.get("arrival_date"))
        if arrival_date is not None and arrival_date > date.today():
            validation_error("arrival_date must not be in the future")

    def _validate_progres_id(self, record: dict) -> None:
        progres_id = record.get("progres_id")
        if is_blank(progres_id):
            return
        progres_id = str(progres_id).strip().upper()
        record["progres_id"] = progres_id
        if not _PROGRES_ID_RE.match(progres_id):
            validation_error(
                "progres_id must look like a ProGres individual ID "
                "(e.g. UGA-00423318)"
            )

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for refugee")
        keys = [
            "functional_record_id",
            "progres_id",
            "first_name",
            "last_name",
            "middle_name",
            "given_name",
            "gender",
            "birth_date",
            "country_of_origin",
            "settlement_code",
            "zone_code",
            "displacement_status",
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
        _logger.info("Constructing record name for refugee")
        keys = ["first_name", "last_name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        name = " ".join(record_name).strip()
        if name:
            return name
        progres_id = str(payload.get("progres_id") or "").strip()
        if progres_id:
            return f"Refugee {progres_id}"
        return fallback_record_name(payload, "Refugee")
