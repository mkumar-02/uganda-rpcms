from openg2p_pbms_models.models import G2PRegistry
from sqlalchemy import JSON, Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class G2PRefugeeRegistry(G2PRegistry):
    """Maps to Uganda Registry table ``g2p_register_refugees`` (DB connector)."""

    __tablename__ = "g2p_register_refugees"

    # G2PRegister identity
    functional_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_internal_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_foundational_id: Mapped[str] = mapped_column(String, nullable=True)
    record_name: Mapped[str] = mapped_column(String, nullable=True)
    record_status: Mapped[str] = mapped_column(String, nullable=True)
    record_status_reason: Mapped[str] = mapped_column(String, nullable=True)

    # Person
    foundational_id: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    given_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    phone_numbers: Mapped[list] = mapped_column(JSON, nullable=True)
    emails: Mapped[list] = mapped_column(JSON, nullable=True)
    marital_status: Mapped[str] = mapped_column(String, nullable=True)
    registration_date: Mapped[Date] = mapped_column(Date, nullable=True)

    # Geo
    latitude: Mapped[str] = mapped_column(String, nullable=True)
    longitude: Mapped[str] = mapped_column(String, nullable=True)
    country_code: Mapped[str] = mapped_column(String, nullable=True)

    # Refugee domain (aligned with registry/refugee-extension)
    progres_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    progres_id_valid_to: Mapped[Date] = mapped_column(Date, nullable=True)
    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)
    arrival_date: Mapped[Date] = mapped_column(Date, nullable=True)
    displacement_status: Mapped[str] = mapped_column(String, nullable=True)
    settlement_code: Mapped[str] = mapped_column(String, nullable=True)
    zone_code: Mapped[str] = mapped_column(String, nullable=True)
    has_personal_phone: Mapped[bool] = mapped_column(Boolean, nullable=True)
    language_spoken: Mapped[str] = mapped_column(String, nullable=True)
    education_level: Mapped[str] = mapped_column(String, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disability_type: Mapped[str] = mapped_column(String, nullable=True)
    disability_severity: Mapped[str] = mapped_column(String, nullable=True)
