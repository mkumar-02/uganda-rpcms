"""Bureau verification adapters.

Replace the stub implementations with live URSB / NGO Bureau clients when
credentials and endpoints are available. Adapters always return a structured
result so the workflow stays the same.
"""

from __future__ import annotations

import json
from typing import NamedTuple, Optional


class AdapterResult(NamedTuple):
    passed: bool
    reference_number: Optional[str]
    message: str
    raw: dict


def check_ursb(ursb_number: Optional[str], registration_number: Optional[str]) -> AdapterResult:
    ref = (ursb_number or registration_number or "").strip()
    if not ref:
        return AdapterResult(
            passed=False,
            reference_number=None,
            message="URSB number or registration number is required.",
            raw={"adapter": "ursb_stub", "reason": "missing_number"},
        )
    # Stub: numbers that start with FAIL fail; everything else passes.
    if ref.upper().startswith("FAIL"):
        return AdapterResult(
            passed=False,
            reference_number=ref,
            message="URSB stub: registration not found / inactive.",
            raw={"adapter": "ursb_stub", "status": "not_found"},
        )
    return AdapterResult(
        passed=True,
        reference_number=ref,
        message="URSB stub: registration verified.",
        raw={"adapter": "ursb_stub", "status": "active"},
    )


def check_ngo_bureau(ngo_bureau_number: Optional[str], name: str) -> AdapterResult:
    ref = (ngo_bureau_number or "").strip()
    if not ref:
        return AdapterResult(
            passed=False,
            reference_number=None,
            message="NGO Bureau number is required.",
            raw={"adapter": "ngo_bureau_stub", "reason": "missing_number"},
        )
    if ref.upper().startswith("FAIL"):
        return AdapterResult(
            passed=False,
            reference_number=ref,
            message="NGO Bureau stub: permit not valid.",
            raw={"adapter": "ngo_bureau_stub", "status": "invalid"},
        )
    return AdapterResult(
        passed=True,
        reference_number=ref,
        message=f"NGO Bureau stub: '{name}' permit verified.",
        raw={"adapter": "ngo_bureau_stub", "status": "valid", "org": name},
    )


def dumps_raw(raw: dict) -> str:
    return json.dumps(raw)
