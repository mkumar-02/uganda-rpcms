from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from ..services import G2PRegisterDomainServiceSelfRelianceSurvey
from .enums import ChildrenInSchoolEnum, MainFoodSourceEnum


class G2PSelfRelianceSurvey:
    """Self-reliance survey round linked to a household (intake-style)."""

    survey_round: Mapped[str] = mapped_column(String, nullable=True)
    survey_date: Mapped[Date] = mapped_column(Date, nullable=True)
    main_food_source: Mapped[MainFoodSourceEnum] = mapped_column(String, nullable=True)
    earns_income: Mapped[bool] = mapped_column(Boolean, nullable=True)
    income_activity: Mapped[str] = mapped_column(String, nullable=True)
    children_in_school: Mapped[ChildrenInSchoolEnum] = mapped_column(String, nullable=True)
    savings_group_member: Mapped[bool] = mapped_column(Boolean, nullable=True)
    self_reliance_index: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)


class G2PRegisterSelfRelianceSurvey(G2PRegister, G2PSelfRelianceSurvey):
    __tablename__ = "g2p_register_self_reliance_surveys"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSelfRelianceSurvey().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSelfRelianceSurvey().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistorySelfRelianceSurvey(G2PRegisterHistory, G2PSelfRelianceSurvey):
    __tablename__ = "g2p_register_history_self_reliance_surveys"


class G2PIntakeFormSelfRelianceSurvey(G2PIntakeForm, G2PRegister, G2PSelfRelianceSurvey):
    __tablename__ = "g2p_intake_form_self_reliance_surveys"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSelfRelianceSurvey().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSelfRelianceSurvey().construct_record_name(
            self.to_dict()
        )
