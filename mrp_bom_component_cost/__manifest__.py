# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mrp Bom Component Cost",
    "summary": "Adds Product Costs to MRP Bom and lines",
    "version": "17.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/sygel-technology/sy-manufacture",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mrp",
    ],
    "data": [
        "security/mrp_bom_component_cost_security.xml",
        "views/mrp_bom_views.xml",
    ],
}
