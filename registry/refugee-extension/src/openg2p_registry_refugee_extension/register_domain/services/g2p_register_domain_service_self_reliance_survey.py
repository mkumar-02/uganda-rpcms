import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int,
    fallback_record_name,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import ChildrenInSchoolEnum, MainFoodSourceEnum

    return {
        "main_food_source": MainFoodSourceEnum,
        "children_in_school": ChildrenInSchoolEnum,
    }


class G2PRegisterDomainServiceSelfRelianceSurvey(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            index = as_int(record.get("self_reliance_index"))
            if index is not None and (index < 0 or index > 100):
                validation_error("self_reliance_index must be between 0 and 100")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for self-reliance survey")
        keys = [
            "functional_record_id",
            "survey_round",
            "survey_date",
            "main_food_source",
            "income_activity",
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
        _logger.info("Constructing record name for self-reliance survey")
        round_name = str(payload.get("survey_round") or "").strip()
        if round_name:
            return f"Survey {round_name}"
        return fallback_record_name(payload, "Self-reliance survey")
