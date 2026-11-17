from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import (
    G2PRegister,
    G2PRegisterHistory,
    G2PGeo,
    G2PPerson,
    G2PPersonHistory,
    G2PGeoHistory,
)
from ..services import G2PRegisterDomainServiceRefugee
from .enums import (
    DisabilitySeverityEnum,
    DisabilityTypeEnum,
    DisplacementStatusEnum,
    EducationalLevelEnum,
)


class G2PRefugee:
    """Domain attributes for a refugee registrant.

    progres_id is the functional link to UNHCR ProGres v4. Authentication
    against ProGres returns Yes/No only and does not populate these fields.
    """

    progres_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    progres_id_valid_to: Mapped[Date] = mapped_column(Date, nullable=True)

    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)
    arrival_date: Mapped[Date] = mapped_column(Date, nullable=True)
    displacement_status: Mapped[DisplacementStatusEnum] = mapped_column(String, nullable=True)

    settlement_code: Mapped[str] = mapped_column(String, nullable=True)
    zone_code: Mapped[str] = mapped_column(String, nullable=True)

    has_personal_phone: Mapped[bool] = mapped_column(Boolean, nullable=True)
    language_spoken: Mapped[str] = mapped_column(String, nullable=True)
    education_level: Mapped[EducationalLevelEnum] = mapped_column(String, nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disability_type: Mapped[DisabilityTypeEnum] = mapped_column(String, nullable=True)
    disability_severity: Mapped[DisabilitySeverityEnum] = mapped_column(String, nullable=True)


class G2PRegisterRefugee(G2PRegister, G2PPerson, G2PGeo, G2PRefugee):
    __tablename__ = "g2p_register_refugees"

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())


class G2PRegisterHistoryRefugee(
    G2PRegisterHistory, G2PPersonHistory, G2PGeoHistory, G2PRefugee
):
    __tablename__ = "g2p_register_history_refugees"


class G2PIntakeFormRefugee(G2PIntakeForm, G2PRegister, G2PPerson, G2PGeo, G2PRefugee):
    __tablename__ = "g2p_intake_form_refugees"

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())
