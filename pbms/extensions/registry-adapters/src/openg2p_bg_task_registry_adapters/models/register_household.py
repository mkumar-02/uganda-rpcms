from openg2p_pbms_models.models import G2PRegistry
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class G2PRegisterHousehold(G2PRegistry):
    """Maps to Uganda Registry table ``g2p_register_households``."""

    __tablename__ = "g2p_register_households"

    functional_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_internal_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_foundational_id: Mapped[str] = mapped_column(String, nullable=True)
    record_name: Mapped[str] = mapped_column(String, nullable=True)
    record_status: Mapped[str] = mapped_column(String, nullable=True)
    record_status_reason: Mapped[str] = mapped_column(String, nullable=True)

    # Geo (from G2PGeo on registry side)
    latitude: Mapped[str] = mapped_column(String, nullable=True)
    longitude: Mapped[str] = mapped_column(String, nullable=True)
    country_code: Mapped[str] = mapped_column(String, nullable=True)

    # Uganda household domain
    household_head: Mapped[str] = mapped_column(String, nullable=True)
    size_of_group: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_children: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_elderly_members: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_female_members: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_male_members: Mapped[int] = mapped_column(Integer, nullable=True)
    settlement_code: Mapped[str] = mapped_column(String, nullable=True)
    zone_code: Mapped[str] = mapped_column(String, nullable=True)
