"""HTTP error codes for the partner onboarding API."""

from openg2p_fastapi_common.errors.http_exceptions import BadRequestError, NotFoundError


class ErrorCodes:
    ngo_not_found = "NGO-404"
    ngo_exists = "NGO-409"
    request_not_found = "NGO-REQ-404"
    request_not_open = "NGO-REQ-409"
    mou_not_found = "NGO-MOU-404"
    mou_required = "NGO-MOU-409"
    compliance_failed = "NGO-CMP-409"
    location_not_found = "NGO-LOC-404"
    invalid_transition = "NGO-WF-409"


class NgoNotFoundError(NotFoundError):
    def __init__(self, ngo_id: str):
        super().__init__(
            code=ErrorCodes.ngo_not_found, message=f"Partner '{ngo_id}' not found."
        )


class NgoExistsError(BadRequestError):
    def __init__(self, short_code: str):
        super().__init__(
            code=ErrorCodes.ngo_exists,
            message=f"Partner with short_code '{short_code}' already exists.",
        )


class RequestNotFoundError(NotFoundError):
    def __init__(self, request_id: str):
        super().__init__(
            code=ErrorCodes.request_not_found,
            message=f"Request '{request_id}' not found.",
        )


class RequestNotOpenError(BadRequestError):
    def __init__(self, message: str = "Request is not open for this action."):
        super().__init__(code=ErrorCodes.request_not_open, message=message)


class MouNotFoundError(NotFoundError):
    def __init__(self, mou_id: str):
        super().__init__(
            code=ErrorCodes.mou_not_found, message=f"MoU '{mou_id}' not found."
        )


class MouRequiredError(BadRequestError):
    def __init__(self, message: str = "A signed MoU is required before approval."):
        super().__init__(code=ErrorCodes.mou_required, message=message)


class ComplianceFailedError(BadRequestError):
    def __init__(self, message: str = "Compliance checks have not all passed."):
        super().__init__(code=ErrorCodes.compliance_failed, message=message)


class LocationNotFoundError(NotFoundError):
    def __init__(self, location_id: str):
        super().__init__(
            code=ErrorCodes.location_not_found,
            message=f"Location '{location_id}' not found.",
        )


class InvalidTransitionError(BadRequestError):
    def __init__(self, message: str):
        super().__init__(code=ErrorCodes.invalid_transition, message=message)
