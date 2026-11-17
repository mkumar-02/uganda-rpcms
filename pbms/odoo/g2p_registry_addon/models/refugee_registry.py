from odoo import fields, models


class G2PRefugeeRegistry(models.Model):
    _name = "g2p.register.refugees"
    _description = "Refugee Registry"
    _inherit = "g2p.registry"
    _auto = False

    functional_record_id = fields.Char(string="Functional Record ID", index=True)
    link_internal_record_id = fields.Char(string="Link Internal Record ID", index=True)
    link_foundational_id = fields.Char(string="Link Foundational ID", index=True)
    record_name = fields.Char(string="Record Name")
    created_by = fields.Char(string="Created By")
    created_at = fields.Datetime(string="Created At")
    last_approved_at = fields.Datetime(string="Last Approved At")
    last_approved_by = fields.Char(string="Last Approved By")
    search_text = fields.Text(string="Search Text")
    record_status = fields.Selection(
        selection=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("archived", "Archived"),
        ],
        string="Record Status",
        default="active",
    )
    record_status_reason = fields.Char(string="Record Status Reason")

    foundational_id = fields.Char(string="Foundational ID", index=True)
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    given_name = fields.Char(string="Given Name")
    gender = fields.Selection(
        selection=[
            ("MALE", "Male"),
            ("FEMALE", "Female"),
            ("OTHERS", "Others"),
            ("UNKNOWN", "Unknown"),
        ],
        string="Gender",
    )
    birth_date = fields.Date(string="Birth Date")
    phone_numbers = fields.Json(string="Phone Numbers")
    emails = fields.Json(string="Emails")
    marital_status = fields.Selection(
        selection=[
            ("SINGLE", "Single"),
            ("MARRIED", "Married"),
            ("DIVORCED", "Divorced"),
            ("WIDOWED", "Widowed"),
            ("SEPARATED", "Separated"),
            ("UNKNOWN", "Unknown"),
        ],
        string="Marital Status",
    )
    registration_date = fields.Date(string="Registration Date")

    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    country_code = fields.Char(string="Country Code", index=True)

    progres_id = fields.Char(string="ProGres ID", index=True)
    progres_id_valid_to = fields.Date(string="ProGres ID Valid To")
    estimated_age = fields.Integer(string="Estimated Age")
    country_of_origin = fields.Char(string="Country of Origin")
    arrival_date = fields.Date(string="Arrival Date")
    displacement_status = fields.Char(string="Displacement Status")
    settlement_code = fields.Char(string="Settlement Code", index=True)
    zone_code = fields.Char(string="Zone Code", index=True)
    has_personal_phone = fields.Boolean(string="Has Personal Phone")
    language_spoken = fields.Char(string="Language Spoken")
    education_level = fields.Char(string="Education Level")
    disabled = fields.Boolean(string="Disabled")
    disability_type = fields.Char(string="Disability Type")
    disability_severity = fields.Char(string="Disability Severity")
