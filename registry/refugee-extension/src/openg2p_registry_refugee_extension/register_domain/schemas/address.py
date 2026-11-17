from typing import Optional


class G2PAddressLinesSchema:
    """address_line_1 / address_line_2 for register and intake schemas.

    The platform's G2PGeo model has both columns, but its G2PGeoSchema does
    not. Change requests are applied through the schema, so these fields must
    be declared or approved edits to address lines are silently dropped.
    """

    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
