"""Lightweight checks that do not require openg2p_registry_core at import time."""

import re

_PROGRES_ID_RE = re.compile(r"^[A-Z]{3}-\d{5,12}$", re.IGNORECASE)


def test_progres_id_accepts_demo_shape():
    assert _PROGRES_ID_RE.match("UGA-00423318")
    assert _PROGRES_ID_RE.match("uga-00419907")


def test_progres_id_rejects_bad_shape():
    assert not _PROGRES_ID_RE.match("UGA00423318")
    assert not _PROGRES_ID_RE.match("UGA-42")
    assert not _PROGRES_ID_RE.match("")
