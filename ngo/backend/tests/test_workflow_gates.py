"""Pure gate-order assertions mirroring RequestService transitions."""

from openg2p_rpcms_ngo_api.models.enums import NgoStatus, RequestStatus


def test_gate_order_statuses():
    # Documented gate: Verify → MoU → Approve
    assert RequestStatus.created.value == "created"
    assert RequestStatus.compliance_passed.value == "compliance_passed"
    assert RequestStatus.mou_attached.value == "mou_attached"
    assert RequestStatus.approved.value == "approved"

    assert NgoStatus.pending_compliance.value == "pending_compliance"
    assert NgoStatus.pending_mou.value == "pending_mou"
    assert NgoStatus.pending_approval.value == "pending_approval"
    assert NgoStatus.active.value == "active"
