from typing import Any

import numpy as np
from openg2p_bg_task_models.models import BeneficiaryListDetails
from openg2p_bg_task_models.schemas import RegistrantDetails
from openg2p_pbms_models.models import Gender
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from ..models import (
    BeneficiaryListSummaryHousehold as BeneficiaryListSummaryHouseholdModel,
)
from ..models import (
    BeneficiaryListSummaryRefugee as BeneficiaryListSummaryRefugeeModel,
)
from ..schema import (
    BeneficiaryListSummary,
    BeneficiaryListSummaryHousehold,
    BeneficiaryListSummaryHouseholdPayload,
    BeneficiaryListSummaryRefugee,
    BeneficiaryListSummaryRefugeePayload,
)
from ._dci_records import age_from_birth_date

def entitlement_stats(entitlements: dict[Any, list[float]]) -> dict[str, dict]:
    stats = {"average": {}, "q1": {}, "q2": {}, "q3": {}, "total": {}}
    for benefit_code_id, values in entitlements.items():
        if not values:
            for key in stats:
                stats[key][benefit_code_id] = 0.0
            continue
        arr = np.array(values)
        stats["average"][benefit_code_id] = round(float(np.mean(arr)), 2)
        stats["q1"][benefit_code_id] = round(
            float(np.percentile(arr, 25, method="midpoint")), 2
        )
        stats["q2"][benefit_code_id] = round(
            float(np.percentile(arr, 50, method="midpoint")), 2
        )
        stats["q3"][benefit_code_id] = round(
            float(np.percentile(arr, 75, method="midpoint")), 2
        )
        stats["total"][benefit_code_id] = float(np.sum(arr))
    return stats


def apply_quartiles(summary_obj, prefix: str, values: list) -> None:
    if not values:
        return
    arr = np.array(values)
    setattr(summary_obj, f"{prefix}_mean", round(float(np.mean(arr)), 2))
    setattr(
        summary_obj,
        f"{prefix}_q1",
        round(float(np.percentile(arr, 25, method="midpoint")), 2),
    )
    setattr(
        summary_obj,
        f"{prefix}_q2",
        round(float(np.percentile(arr, 50, method="midpoint")), 2),
    )
    setattr(
        summary_obj,
        f"{prefix}_q3",
        round(float(np.percentile(arr, 75, method="midpoint")), 2),
    )


def _ids_from_details(details: list[BeneficiaryListDetails]) -> list[list[str]]:
    batches = []
    for detail in details:
        ids = []
        for registrant in detail.registrant_details or []:
            parsed = RegistrantDetails(**registrant)
            ids.append(str(parsed.registrant_id))
        batches.append(ids)
    return batches


def gendered_entitlement_values(adapter, beneficiary_list_id, bg_task_session) -> dict:
    """Entitlement stats overall and split by the registrant's gender."""
    details = (
        bg_task_session.query(BeneficiaryListDetails)
        .filter_by(beneficiary_list_id=beneficiary_list_id)
        .all()
    )
    by_id = {}
    for registrant_ids in _ids_from_details(details):
        for person in adapter.fetch_by_ids(registrant_ids):
            by_id[str(adapter.registrant_id_of(person))] = person

    entitlements: dict = {}
    entitlements_male: dict = {}
    entitlements_female: dict = {}
    for detail in details:
        for registrant in detail.registrant_details or []:
            parsed = RegistrantDetails(**registrant)
            person = by_id.get(str(parsed.registrant_id))
            gender = (getattr(person, "gender", None) or "").lower() if person else ""
            for benefit_code_id, value in (parsed.entitlement or {}).items():
                entitlements.setdefault(benefit_code_id, []).append(value)
                if gender == Gender.MALE.value:
                    entitlements_male.setdefault(benefit_code_id, []).append(value)
                elif gender == Gender.FEMALE.value:
                    entitlements_female.setdefault(benefit_code_id, []).append(value)

    all_stats = entitlement_stats(entitlements)
    male_stats = entitlement_stats(entitlements_male)
    female_stats = entitlement_stats(entitlements_female)
    return {
        "total_disbursement_quantity": dict(all_stats["total"]),
        "average_entitlement_per_person": dict(all_stats["average"]),
        "entitlement_amount_q1": dict(all_stats["q1"]),
        "entitlement_amount_q2": dict(all_stats["q2"]),
        "entitlement_amount_q3": dict(all_stats["q3"]),
        "average_entitlement_male": dict(male_stats["average"]),
        "entitlement_amount_male_q1": dict(male_stats["q1"]),
        "entitlement_amount_male_q2": dict(male_stats["q2"]),
        "entitlement_amount_male_q3": dict(male_stats["q3"]),
        "average_entitlement_female": dict(female_stats["average"]),
        "entitlement_amount_female_q1": dict(female_stats["q1"]),
        "entitlement_amount_female_q2": dict(female_stats["q2"]),
        "entitlement_amount_female_q3": dict(female_stats["q3"]),
    }


class RefugeeSummaries:
    async def get_summary(
        self,
        beneficiary_list_id: str,
        bg_task_session: AsyncSession,
        formated: bool = False,
    ) -> BeneficiaryListSummaryRefugeePayload:
        result = await bg_task_session.execute(
            select(BeneficiaryListSummaryRefugeeModel).where(
                BeneficiaryListSummaryRefugeeModel.beneficiary_list_id
                == beneficiary_list_id
            )
        )
        return self._refugee_payload(result.scalars().first())

    def get_summary_sync(
        self, beneficiary_list_id: str, bg_task_session: Session
    ) -> BeneficiaryListSummaryRefugeePayload:
        row = (
            bg_task_session.query(BeneficiaryListSummaryRefugeeModel)
            .filter_by(beneficiary_list_id=beneficiary_list_id)
            .first()
        )
        return self._refugee_payload(row)

    def compute_eligibility_statistics(
        self,
        beneficiary_list_details: list[BeneficiaryListDetails],
        base_summary,
        bg_task_session: Session,
    ):
        summary = BeneficiaryListSummaryRefugeeModel(
            program_id=base_summary.program_id,
            program_mnemonic=base_summary.program_mnemonic,
            target_registry=base_summary.target_registry,
            beneficiary_list_id=base_summary.beneficiary_list_id,
            number_of_registrants=base_summary.number_of_registrants,
            date_created=base_summary.date_created,
        )
        ages = []
        for registrant_ids in _ids_from_details(beneficiary_list_details):
            for refugee in self.fetch_by_ids(registrant_ids):
                if getattr(farmer, "estimated_age", None) is not None:
                    ages.append(refugee.estimated_age)
        apply_quartiles(summary, "estimated_age", ages)
        bg_task_session.add(summary)

    def compute_entitlement_statistics(
        self, beneficiary_list_id: str, bg_task_session: Session
    ):
        values = gendered_entitlement_values(self, beneficiary_list_id, bg_task_session)
        bg_task_session.execute(
            update(BeneficiaryListSummaryRefugeeModel)
            .where(
                BeneficiaryListSummaryRefugeeModel.beneficiary_list_id
                == beneficiary_list_id
            )
            .values(**values)
        )

    def _refugee_payload(self, row) -> BeneficiaryListSummaryRefugeePayload:
        def fmt(value, units):
            return f"{value} {units}" if value is not None else None

        return BeneficiaryListSummaryRefugeePayload(
            beneficiary_list_summary=BeneficiaryListSummary(
                id=row.id,
                program_id=row.program_id,
                program_mnemonic=row.program_mnemonic,
                target_registry=row.target_registry,
                beneficiary_list_id=row.beneficiary_list_id,
                number_of_registrants=row.number_of_registrants,
                date_created=row.date_created,
                total_disbursement_quantity=row.total_disbursement_quantity,
                average_entitlement_per_registrant=row.average_entitlement_per_person,
            ),
            registry_summary=BeneficiaryListSummaryRefugee(
                estimated_age_mean=fmt(row.estimated_age_mean, row.estimated_age_units),
                estimated_age_q1=fmt(row.estimated_age_q1, row.estimated_age_units),
                estimated_age_q2=fmt(row.estimated_age_q2, row.estimated_age_units),
                estimated_age_q3=fmt(row.estimated_age_q3, row.estimated_age_units),
                average_entitlement_female=row.average_entitlement_female,
                average_entitlement_male=row.average_entitlement_male,
                entitlement_amount_q3=row.entitlement_amount_q3,
                entitlement_amount_q2=row.entitlement_amount_q2,
                entitlement_amount_q1=row.entitlement_amount_q1,
                entitlement_amount_male_q3=row.entitlement_amount_male_q3,
                entitlement_amount_male_q2=row.entitlement_amount_male_q2,
                entitlement_amount_male_q1=row.entitlement_amount_male_q1,
                entitlement_amount_female_q3=row.entitlement_amount_female_q3,
                entitlement_amount_female_q2=row.entitlement_amount_female_q2,
                entitlement_amount_female_q1=row.entitlement_amount_female_q1,
            ),
        )


class HouseholdSummaries:
    async def get_summary(
        self,
        beneficiary_list_id: str,
        bg_task_session: AsyncSession,
        formated: bool = False,
    ) -> BeneficiaryListSummaryHouseholdPayload:
        result = await bg_task_session.execute(
            select(BeneficiaryListSummaryHouseholdModel).where(
                BeneficiaryListSummaryHouseholdModel.beneficiary_list_id
                == beneficiary_list_id
            )
        )
        return self._household_payload(result.scalars().first())

    def get_summary_sync(
        self, beneficiary_list_id: str, bg_task_session: Session
    ) -> BeneficiaryListSummaryHouseholdPayload:
        row = (
            bg_task_session.query(BeneficiaryListSummaryHouseholdModel)
            .filter_by(beneficiary_list_id=beneficiary_list_id)
            .first()
        )
        return self._household_payload(row)

    def compute_eligibility_statistics(
        self,
        beneficiary_list_details: list[BeneficiaryListDetails],
        base_summary,
        bg_task_session: Session,
    ):
        summary = BeneficiaryListSummaryHouseholdModel(
            program_id=base_summary.program_id,
            program_mnemonic=base_summary.program_mnemonic,
            target_registry=base_summary.target_registry,
            beneficiary_list_id=base_summary.beneficiary_list_id,
            number_of_registrants=base_summary.number_of_registrants,
            date_created=base_summary.date_created,
        )
        buckets = {
            "size_of_group": [],
            "number_of_children": [],
            "number_of_elderly_members": [],
        }
        for registrant_ids in _ids_from_details(beneficiary_list_details):
            for household in self.fetch_by_ids(registrant_ids):
                for field_name, values in buckets.items():
                    value = getattr(household, field_name, None)
                    if value is not None:
                        values.append(value)
        for field_name, values in buckets.items():
            apply_quartiles(summary, field_name, values)
        bg_task_session.add(summary)

    def compute_entitlement_statistics(
        self, beneficiary_list_id: str, bg_task_session: Session
    ):
        details = (
            bg_task_session.query(BeneficiaryListDetails)
            .filter_by(beneficiary_list_id=beneficiary_list_id)
            .all()
        )
        entitlements: dict = {}
        for detail in details:
            for registrant in detail.registrant_details or []:
                parsed = RegistrantDetails(**registrant)
                for benefit_code_id, value in (parsed.entitlement or {}).items():
                    entitlements.setdefault(benefit_code_id, []).append(value)
        stats = entitlement_stats(entitlements)
        bg_task_session.execute(
            update(BeneficiaryListSummaryHouseholdModel)
            .where(
                BeneficiaryListSummaryHouseholdModel.beneficiary_list_id
                == beneficiary_list_id
            )
            .values(
                total_disbursement_quantity=dict(stats["total"]),
                average_entitlement_per_person=dict(stats["average"]),
                entitlement_amount_q1=dict(stats["q1"]),
                entitlement_amount_q2=dict(stats["q2"]),
                entitlement_amount_q3=dict(stats["q3"]),
            )
        )

    def _household_payload(self, row) -> BeneficiaryListSummaryHouseholdPayload:
        def fmt(value, units):
            return f"{value} {units}" if value is not None else None

        return BeneficiaryListSummaryHouseholdPayload(
            beneficiary_list_summary=BeneficiaryListSummary(
                id=row.id,
                program_id=row.program_id,
                program_mnemonic=row.program_mnemonic,
                target_registry=row.target_registry,
                beneficiary_list_id=row.beneficiary_list_id,
                number_of_registrants=row.number_of_registrants,
                date_created=row.date_created,
                total_disbursement_quantity=row.total_disbursement_quantity,
                average_entitlement_per_registrant=row.average_entitlement_per_person,
            ),
            registry_summary=BeneficiaryListSummaryHousehold(
                size_of_group_mean=fmt(row.size_of_group_mean, row.size_of_group_units),
                size_of_group_q1=fmt(row.size_of_group_q1, row.size_of_group_units),
                size_of_group_q2=fmt(row.size_of_group_q2, row.size_of_group_units),
                size_of_group_q3=fmt(row.size_of_group_q3, row.size_of_group_units),
                number_of_children_mean=fmt(
                    row.number_of_children_mean, row.number_of_children_units
                ),
                number_of_children_q1=fmt(
                    row.number_of_children_q1, row.number_of_children_units
                ),
                number_of_children_q2=fmt(
                    row.number_of_children_q2, row.number_of_children_units
                ),
                number_of_children_q3=fmt(
                    row.number_of_children_q3, row.number_of_children_units
                ),
                number_of_elderly_members_mean=fmt(
                    row.number_of_elderly_members_mean,
                    row.number_of_elderly_members_units,
                ),
                number_of_elderly_members_q1=fmt(
                    row.number_of_elderly_members_q1,
                    row.number_of_elderly_members_units,
                ),
                number_of_elderly_members_q2=fmt(
                    row.number_of_elderly_members_q2,
                    row.number_of_elderly_members_units,
                ),
                number_of_elderly_members_q3=fmt(
                    row.number_of_elderly_members_q3,
                    row.number_of_elderly_members_units,
                ),
                entitlement_amount_q1=row.entitlement_amount_q1,
                entitlement_amount_q2=row.entitlement_amount_q2,
                entitlement_amount_q3=row.entitlement_amount_q3,
            ),
        )


