from openg2p_bg_task_models.models import BeneficiaryListSummary
from sqlalchemy import JSON, Float, String
from sqlalchemy.orm import mapped_column


class BeneficiaryListSummaryHousehold(BeneficiaryListSummary):
    __tablename__ = "beneficiary_list_summary_household"

    size_of_group_q1 = mapped_column(Float, nullable=True, default=0)
    size_of_group_q2 = mapped_column(Float, nullable=True, default=0)
    size_of_group_q3 = mapped_column(Float, nullable=True, default=0)
    size_of_group_mean = mapped_column(Float, nullable=True, default=0)
    size_of_group_units = mapped_column(String, nullable=False, default="persons")

    number_of_children_q1 = mapped_column(Float, nullable=True, default=0)
    number_of_children_q2 = mapped_column(Float, nullable=True, default=0)
    number_of_children_q3 = mapped_column(Float, nullable=True, default=0)
    number_of_children_mean = mapped_column(Float, nullable=True, default=0)
    number_of_children_units = mapped_column(String, nullable=False, default="persons")

    number_of_elderly_members_q1 = mapped_column(Float, nullable=True, default=0)
    number_of_elderly_members_q2 = mapped_column(Float, nullable=True, default=0)
    number_of_elderly_members_q3 = mapped_column(Float, nullable=True, default=0)
    number_of_elderly_members_mean = mapped_column(Float, nullable=True, default=0)
    number_of_elderly_members_units = mapped_column(
        String, nullable=False, default="persons"
    )

    entitlement_amount_q1 = mapped_column(JSON, nullable=True)
    entitlement_amount_q2 = mapped_column(JSON, nullable=True)
    entitlement_amount_q3 = mapped_column(JSON, nullable=True)
    entitlement_units = mapped_column(JSON, nullable=True)
