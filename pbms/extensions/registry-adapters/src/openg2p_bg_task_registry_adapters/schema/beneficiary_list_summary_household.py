from typing import Optional

from pydantic import BaseModel

from .beneficiary_list_summary import BeneficiaryListSummaryPayload


class BeneficiaryListSummaryHousehold(BaseModel):
    size_of_group_mean: Optional[str] = None
    size_of_group_q1: Optional[str] = None
    size_of_group_q2: Optional[str] = None
    size_of_group_q3: Optional[str] = None
    number_of_children_mean: Optional[str] = None
    number_of_children_q1: Optional[str] = None
    number_of_children_q2: Optional[str] = None
    number_of_children_q3: Optional[str] = None
    number_of_elderly_members_mean: Optional[str] = None
    number_of_elderly_members_q1: Optional[str] = None
    number_of_elderly_members_q2: Optional[str] = None
    number_of_elderly_members_q3: Optional[str] = None
    entitlement_amount_q1: Optional[dict] = None
    entitlement_amount_q2: Optional[dict] = None
    entitlement_amount_q3: Optional[dict] = None


class BeneficiaryListSummaryHouseholdPayload(BeneficiaryListSummaryPayload):
    registry_summary: BeneficiaryListSummaryHousehold
