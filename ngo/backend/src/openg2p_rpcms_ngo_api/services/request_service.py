import logging
from datetime import datetime, timezone
from typing import Optional

from openg2p_fastapi_common.service import BaseService
from sqlalchemy import select

from ..config import Settings
from ..errors import (
    ComplianceFailedError,
    InvalidTransitionError,
    MouRequiredError,
    NgoExistsError,
    NgoNotFoundError,
    RequestNotFoundError,
    RequestNotOpenError,
)
from ..models import (
    ComplianceCheckKind,
    ComplianceCheckORM,
    ComplianceCheckStatus,
    NgoORM,
    NgoRequestORM,
    NgoStatus,
    RequestStatus,
    RequestType,
)
from ..schemas import OnboardRequest
from .compliance_adapters import check_ngo_bureau, check_ursb, dumps_raw
from .db import session_maker
from .mou_service import MouService
from .provisioner import ProvisionerService

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


def _utcnow():
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


class RequestService(BaseService):
    """Onboarding workflow: Verify → MoU → Approve → provision Agent/Agency/Program."""

    async def list_requests(self, status: Optional[str] = None) -> list[NgoRequestORM]:
        async with session_maker()() as session:
            stmt = select(NgoRequestORM).order_by(NgoRequestORM.created_at.desc())
            if status:
                stmt = stmt.where(NgoRequestORM.status == status)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def get(self, request_id: str) -> NgoRequestORM | None:
        async with session_maker()() as session:
            res = await session.execute(
                select(NgoRequestORM).where(NgoRequestORM.id == request_id)
            )
            return res.scalars().first()

    async def create_onboarding(self, data: OnboardRequest) -> tuple[NgoORM, NgoRequestORM]:
        async with session_maker()() as session:
            if data.short_code:
                existing = (
                    await session.execute(
                        select(NgoORM).where(NgoORM.short_code == data.short_code)
                    )
                ).scalars().first()
                if existing:
                    raise NgoExistsError(data.short_code)

            ngo = NgoORM(
                name=data.name,
                short_code=data.short_code,
                registration_number=data.registration_number,
                ursb_number=data.ursb_number,
                ngo_bureau_number=data.ngo_bureau_number,
                contact_email=data.contact_email,
                contact_phone=data.contact_phone,
                legal_address=data.legal_address,
                notes=data.notes,
                status=NgoStatus.pending_compliance.value,
            )
            session.add(ngo)
            await session.flush()

            req = NgoRequestORM(
                ngo_id=ngo.id,
                request_type=RequestType.onboarding.value,
                status=RequestStatus.created.value,
                submitted_by=data.submitted_by or "staff",
            )
            session.add(req)
            await session.commit()
            await session.refresh(ngo)
            await session.refresh(req)
            return ngo, req

    async def run_compliance(self, request_id: str) -> tuple[list[ComplianceCheckORM], bool]:
        async with session_maker()() as session:
            req = (
                await session.execute(
                    select(NgoRequestORM).where(NgoRequestORM.id == request_id)
                )
            ).scalars().first()
            if not req:
                raise RequestNotFoundError(request_id)
            if req.status not in (
                RequestStatus.created.value,
                RequestStatus.compliance_passed.value,
            ):
                raise RequestNotOpenError(
                    f"Cannot run compliance on request in status '{req.status}'."
                )

            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == req.ngo_id))
            ).scalars().first()
            if not ngo:
                raise NgoNotFoundError(req.ngo_id)

            # Replace prior pending/failed runs for a clean re-check.
            existing = (
                await session.execute(
                    select(ComplianceCheckORM).where(
                        ComplianceCheckORM.request_id == request_id
                    )
                )
            ).scalars().all()
            for row in existing:
                await session.delete(row)
            await session.flush()

            results: list[ComplianceCheckORM] = []
            ursb = check_ursb(ngo.ursb_number, ngo.registration_number)
            results.append(
                ComplianceCheckORM(
                    request_id=request_id,
                    ngo_id=ngo.id,
                    kind=ComplianceCheckKind.ursb.value,
                    status=(
                        ComplianceCheckStatus.passed.value
                        if ursb.passed
                        else ComplianceCheckStatus.failed.value
                    ),
                    reference_number=ursb.reference_number,
                    checked_at=_utcnow(),
                    raw_result=dumps_raw(ursb.raw),
                    message=ursb.message,
                )
            )
            bureau = check_ngo_bureau(ngo.ngo_bureau_number, ngo.name)
            results.append(
                ComplianceCheckORM(
                    request_id=request_id,
                    ngo_id=ngo.id,
                    kind=ComplianceCheckKind.ngo_bureau.value,
                    status=(
                        ComplianceCheckStatus.passed.value
                        if bureau.passed
                        else ComplianceCheckStatus.failed.value
                    ),
                    reference_number=bureau.reference_number,
                    checked_at=_utcnow(),
                    raw_result=dumps_raw(bureau.raw),
                    message=bureau.message,
                )
            )
            for row in results:
                session.add(row)

            all_passed = all(
                r.status == ComplianceCheckStatus.passed.value for r in results
            )
            if all_passed:
                req.status = RequestStatus.compliance_passed.value
                ngo.status = NgoStatus.pending_mou.value
            else:
                ngo.status = NgoStatus.pending_compliance.value

            await session.commit()
            for row in results:
                await session.refresh(row)
            return results, all_passed

    async def list_compliance(self, request_id: str) -> list[ComplianceCheckORM]:
        async with session_maker()() as session:
            res = await session.execute(
                select(ComplianceCheckORM)
                .where(ComplianceCheckORM.request_id == request_id)
                .order_by(ComplianceCheckORM.kind)
            )
            return list(res.scalars().all())

    async def mark_mou_attached(self, request_id: str) -> NgoRequestORM:
        mou_svc = MouService.get_component()
        async with session_maker()() as session:
            req = (
                await session.execute(
                    select(NgoRequestORM).where(NgoRequestORM.id == request_id)
                )
            ).scalars().first()
            if not req:
                raise RequestNotFoundError(request_id)
            if req.status not in (
                RequestStatus.compliance_passed.value,
                RequestStatus.mou_attached.value,
            ):
                raise InvalidTransitionError(
                    "MoU can only be attached after compliance has passed."
                )

            if not await mou_svc.has_signed_mou(req.ngo_id, request_id):
                raise MouRequiredError(
                    "Attach and sign an MoU for this partner before marking MoU attached."
                )

            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == req.ngo_id))
            ).scalars().first()
            req.status = RequestStatus.mou_attached.value
            if ngo:
                ngo.status = NgoStatus.pending_approval.value
            await session.commit()
            await session.refresh(req)
            return req

    async def approve(
        self, request_id: str, decided_by: str = "staff", comment: Optional[str] = None
    ) -> tuple[NgoRequestORM, NgoORM]:
        provisioner = ProvisionerService.get_component()
        mou_svc = MouService.get_component()

        async with session_maker()() as session:
            req = (
                await session.execute(
                    select(NgoRequestORM).where(NgoRequestORM.id == request_id)
                )
            ).scalars().first()
            if not req:
                raise RequestNotFoundError(request_id)
            if req.status != RequestStatus.mou_attached.value:
                raise RequestNotOpenError(
                    "Approve only after compliance + signed MoU (status mou_attached)."
                )

            checks = (
                await session.execute(
                    select(ComplianceCheckORM).where(
                        ComplianceCheckORM.request_id == request_id
                    )
                )
            ).scalars().all()
            if not checks or any(
                c.status != ComplianceCheckStatus.passed.value for c in checks
            ):
                raise ComplianceFailedError()

            if not await mou_svc.has_signed_mou(req.ngo_id, request_id):
                raise MouRequiredError()

            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == req.ngo_id))
            ).scalars().first()
            if not ngo:
                raise NgoNotFoundError(req.ngo_id)

            await provisioner.provision_after_approval(ngo)
            ngo.status = NgoStatus.active.value
            ngo.approved_at = _utcnow()
            req.status = RequestStatus.approved.value
            req.decided_by = decided_by
            req.decided_at = _utcnow()
            req.decision_comment = comment

            if _config.awe_enabled and _config.awe_base_url:
                # Hook for AWE callback / instance id — no-op until wired.
                req.awe_instance_id = req.awe_instance_id or f"awe-stub-{req.id[:8]}"

            await session.commit()
            await session.refresh(req)
            await session.refresh(ngo)
            return req, ngo

    async def reject(
        self, request_id: str, decided_by: str = "staff", comment: Optional[str] = None
    ) -> tuple[NgoRequestORM, NgoORM]:
        async with session_maker()() as session:
            req = (
                await session.execute(
                    select(NgoRequestORM).where(NgoRequestORM.id == request_id)
                )
            ).scalars().first()
            if not req:
                raise RequestNotFoundError(request_id)
            if req.status in (
                RequestStatus.approved.value,
                RequestStatus.rejected.value,
            ):
                raise RequestNotOpenError("Request already decided.")

            ngo = (
                await session.execute(select(NgoORM).where(NgoORM.id == req.ngo_id))
            ).scalars().first()
            if not ngo:
                raise NgoNotFoundError(req.ngo_id)

            req.status = RequestStatus.rejected.value
            req.decided_by = decided_by
            req.decided_at = _utcnow()
            req.decision_comment = comment
            ngo.status = NgoStatus.rejected.value
            await session.commit()
            await session.refresh(req)
            await session.refresh(ngo)
            return req, ngo
