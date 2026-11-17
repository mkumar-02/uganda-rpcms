# ruff: noqa: B018
{
    "name": "PBMS Registry Addon (Uganda RPCMS)",
    "version": "0.1.0",
    "summary": "Refugee and Household registry views for Uganda RPCMS PBMS",
    "description": "Odoo register models aligned with uganda-rpcms/registry",
    "category": "G2P",
    "license": "LGPL-3",
    "depends": ["base_setup", "web", "g2p_pbms"],
    "data": [
        "security/ir.model.access.csv",
        "views/eligibility/eligibility_rule_view.xml",
        "views/entitlement/entitlement_rule_view.xml",
        "views/priority/priority_rule_view.xml",
        "views/registry/refugee_registry_view.xml",
        "views/registry/household_registry_view.xml",
        "views/bgtask/bgtask_view.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/g2p_registry_addon/static/src/css/registry_styles.scss",
            "/g2p_registry_addon/static/src/js/beneficiaries_widget.js",
            "/g2p_registry_addon/static/src/xml/g2p_beneficiaries_info_tpl.xml",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
