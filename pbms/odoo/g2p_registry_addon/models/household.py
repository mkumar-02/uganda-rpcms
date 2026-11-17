from odoo import fields, models


class G2PRegisterHousehold(models.Model):
    _name = "g2p.register.households"
    _description = "Register Household"
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

    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    country_code = fields.Char(string="Country Code", index=True)

    household_head = fields.Char(string="Household Head")
    size_of_group = fields.Integer(string="Size of Group")
    number_of_children = fields.Integer(string="Number of Children")
    number_of_elderly_members = fields.Integer(string="Number of Elderly Members")
    number_of_female_members = fields.Integer(string="Number of Female Members")
    number_of_male_members = fields.Integer(string="Number of Male Members")
    settlement_code = fields.Char(string="Settlement Code", index=True)
    zone_code = fields.Char(string="Zone Code", index=True)
