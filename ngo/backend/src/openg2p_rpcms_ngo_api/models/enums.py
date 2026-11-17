from enum import Enum


class NgoStatus(str, Enum):
    """Lifecycle of a partner after onboarding is filed."""

    created = "created"  # application filed, not yet active
    pending_compliance = "pending_compliance"
    pending_mou = "pending_mou"
    pending_approval = "pending_approval"
    active = "active"
    rejected = "rejected"
    suspended = "suspended"


class RequestStatus(str, Enum):
    created = "created"
    compliance_passed = "compliance_passed"
    mou_attached = "mou_attached"
    approved = "approved"
    rejected = "rejected"


class RequestType(str, Enum):
    onboarding = "onboarding"
    renewal = "renewal"
    location_update = "location_update"


class ComplianceCheckKind(str, Enum):
    ursb = "ursb"
    ngo_bureau = "ngo_bureau"


class ComplianceCheckStatus(str, Enum):
    pending = "pending"
    passed = "passed"
    failed = "failed"
    skipped = "skipped"


class MouStatus(str, Enum):
    draft = "draft"
    pending_signature = "pending_signature"
    signed = "signed"
    expired = "expired"
    void = "void"


class LocationKind(str, Enum):
    admin_large = "admin_large"  # e.g. district / settlement
    admin_small = "admin_small"  # e.g. zone
    service_point = "service_point"
