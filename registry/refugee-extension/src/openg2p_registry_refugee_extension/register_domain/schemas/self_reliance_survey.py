from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)
from ..models.enums import ChildrenInSchoolEnum, MainFoodSourceEnum


class G2PSchemaSelfRelianceSurvey:

    survey_round: Optional[str] = None
    survey_date: Optional[date] = None
    main_food_source: Optional[MainFoodSourceEnum] = None
    earns_income: Optional[bool] = None
    income_activity: Optional[str] = None
    children_in_school: Optional[ChildrenInSchoolEnum] = None
    savings_group_member: Optional[bool] = None
    self_reliance_index: Optional[int] = None
    notes: Optional[str] = None


class G2PRegisterSchemaSelfRelianceSurvey(
    G2PRegisterBaseSchema, G2PSchemaSelfRelianceSurvey
):
    """Schema for SelfRelianceSurvey register."""


class G2PRegisterHistorySchemaSelfRelianceSurvey(G2PRegisterHistorySchema):
    """Schema for SelfRelianceSurvey history."""


class G2PIntakeFormSchemaSelfRelianceSurvey(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaSelfRelianceSurvey
):
    """Schema for SelfRelianceSurvey intake form."""
