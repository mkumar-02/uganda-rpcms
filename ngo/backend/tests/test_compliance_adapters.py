from openg2p_rpcms_ngo_api.services.compliance_adapters import (
    check_ngo_bureau,
    check_ursb,
)


def test_ursb_requires_number():
    r = check_ursb(None, None)
    assert r.passed is False


def test_ursb_passes():
    r = check_ursb("URSB-12345", None)
    assert r.passed is True
    assert r.reference_number == "URSB-12345"


def test_ursb_fail_prefix():
    r = check_ursb("FAIL-001", None)
    assert r.passed is False


def test_bureau_passes():
    r = check_ngo_bureau("NB-99", "Hope NGO")
    assert r.passed is True


def test_bureau_missing():
    r = check_ngo_bureau(None, "Hope NGO")
    assert r.passed is False
