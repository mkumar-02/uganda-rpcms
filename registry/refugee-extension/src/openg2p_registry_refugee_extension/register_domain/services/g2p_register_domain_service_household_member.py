import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_bool,
    fallback_record_name,
    is_blank,
    parse_date,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")

_HEAD_RELATIONSHIP = "SELF"


def _allowed_relationships() -> set[str]:
    from ..models.enums import RelationshipToTheHeadEnum

    return {item.value for item in RelationshipToTheHeadEnum}


class G2PRegisterDomainServiceHouseholdMember(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_birth_date(record)
            self._validate_head_and_relationship(record)
        self._validate_single_head(records)

    def _validate_birth_date(self, record: dict) -> None:
        birth_date = parse_date(record.get("birth_date"))
        if birth_date is not None and birth_date > date.today():
            validation_error("birth_date must not be in the future")

    def _validate_head_and_relationship(self, record: dict) -> None:
        if "is_head" not in record and "relationship_to_the_head" not in record:
            return
        relationship = record.get("relationship_to_the_head")
        if not is_blank(relationship) and str(relationship) not in _allowed_relationships():
            validation_error(
                "relationship_to_the_head must be one of "
                + ", ".join(sorted(_allowed_relationships()))
            )
        if self._is_head(record):
            if not is_blank(relationship) and str(relationship) != _HEAD_RELATIONSHIP:
                validation_error(
                    "The household head cannot have a relationship_to_the_head other than SELF"
                )
            record["relationship_to_the_head"] = _HEAD_RELATIONSHIP
        else:
            if is_blank(relationship):
                validation_error(
                    "relationship_to_the_head is required for every member who is not the head"
                )
            if str(relationship) == _HEAD_RELATIONSHIP:
                validation_error(
                    "relationship_to_the_head SELF is reserved for the head; tick is_head instead"
                )

    def _validate_single_head(self, records: list[dict]) -> None:
        heads = [record for record in records if self._is_head(record)]
        if len(heads) > 1:
            validation_error(
                "Only one household member can be marked as the head (is_head)"
            )

    @staticmethod
    def _is_head(record: dict) -> bool:
        return bool(as_bool(record.get("is_head")))

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for household member")
        keys = [
            "progres_id",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "birth_date",
            "is_head",
            "relationship_to_the_head",
            "is_disabled",
        ]
        search_text = []
        if extra:
            search_text.extend(str(item).strip() for item in extra if str(item).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for household member")
        keys = ["first_name", "last_name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        return " ".join(record_name).strip() or fallback_record_name(
            payload, "Household member"
        )
