import logging
from typing import Optional

from openg2p_fastapi_common.controller import BaseController

from ..config import Settings
from ..errors import RequestNotFoundError
from ..schemas import (
    ComplianceCheckResponse,
    ComplianceRunResponse,
    DecisionRequest,
    NgoActionResponse,
    OnboardRequest,
    RequestDetailResponse,
    RequestListResponse,
    RequestResponse,
)
from ..services import NgoService, RequestService

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class RequestController(BaseController):
    """Partner onboarding request workflow endpoints."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.requests = RequestService.get_component()
        self.ngos = NgoService.get_component()
        self.router.tags += ["Requests"]

        self.router.add_api_route(
            "/requests",
            self.list_requests,
            methods=["GET"],
            responses={200: {"model": RequestListResponse}},
        )
        self.router.add_api_route(
            "/requests/{request_id}",
            self.get_request,
            methods=["GET"],
            responses={200: {"model": RequestDetailResponse}},
        )
        self.router.add_api_route(
            "/onboard",
            self.onboard,
            methods=["POST"],
            responses={200: {"model": RequestDetailResponse}},
        )
        self.router.add_api_route(
            "/requests/{request_id}/run-compliance",
            self.run_compliance,
            methods=["POST"],
            responses={200: {"model": ComplianceRunResponse}},
        )
        self.router.add_api_route(
            "/requests/{request_id}/compliance",
            self.list_compliance,
            methods=["GET"],
            responses={200: {"model": list[ComplianceCheckResponse]}},
        )
        self.router.add_api_route(
            "/requests/{request_id}/mark-mou-attached",
            self.mark_mou_attached,
            methods=["POST"],
            responses={200: {"model": RequestResponse}},
        )
        self.router.add_api_route(
            "/requests/{request_id}/approve",
            self.approve,
            methods=["POST"],
            responses={200: {"model": NgoActionResponse}},
        )
        self.router.add_api_route(
            "/requests/{request_id}/reject",
            self.reject,
            methods=["POST"],
            responses={200: {"model": NgoActionResponse}},
        )

    async def list_requests(self, status: Optional[str] = None):
        rows = await self.requests.list_requests(status=status)
        enriched: list[RequestDetailResponse] = []
        for r in rows:
            ngo = await self.ngos.get(r.ngo_id)
            enriched.append(
                RequestDetailResponse(
                    **RequestResponse.model_validate(r).model_dump(),
                    ngo_name=ngo.name if ngo else None,
                )
            )
        return RequestListResponse(count=len(enriched), requests=enriched)


    async def get_request(self, request_id: str):
        req = await self.requests.get(request_id)
        if not req:
            raise RequestNotFoundError(request_id)
        ngo = await self.ngos.get(req.ngo_id)
        return RequestDetailResponse(
            **RequestResponse.model_validate(req).model_dump(),
            ngo_name=ngo.name if ngo else None,
        )

    async def onboard(self, body: OnboardRequest):
        ngo, req = await self.requests.create_onboarding(body)
        return RequestDetailResponse(
            **RequestResponse.model_validate(req).model_dump(),
            ngo_name=ngo.name,
            message="Onboarding request created. Run compliance next.",
        )

    async def run_compliance(self, request_id: str):
        checks, all_passed = await self.requests.run_compliance(request_id)
        return ComplianceRunResponse(
            request_id=request_id,
            all_passed=all_passed,
            checks=[ComplianceCheckResponse.model_validate(c) for c in checks],
        )

    async def list_compliance(self, request_id: str):
        checks = await self.requests.list_compliance(request_id)
        return [ComplianceCheckResponse.model_validate(c) for c in checks]

    async def mark_mou_attached(self, request_id: str):
        req = await self.requests.mark_mou_attached(request_id)
        return RequestResponse.model_validate(req)

    async def approve(self, request_id: str, body: DecisionRequest = None):
        body = body or DecisionRequest()
        _req, ngo = await self.requests.approve(
            request_id, decided_by=body.decided_by or "staff", comment=body.comment
        )
        return NgoActionResponse(
            ngo_id=ngo.id,
            status=ngo.status,
            message="Approved. Registry Agent + PBMS Agency/Program provisioned.",
            registry_agent_id=ngo.registry_agent_id,
            pbms_agency_id=ngo.pbms_agency_id,
            pbms_program_id=ngo.pbms_program_id,
        )

    async def reject(self, request_id: str, body: DecisionRequest = None):
        body = body or DecisionRequest()
        _req, ngo = await self.requests.reject(
            request_id, decided_by=body.decided_by or "staff", comment=body.comment
        )
        return NgoActionResponse(
            ngo_id=ngo.id,
            status=ngo.status,
            message="Request rejected.",
        )
