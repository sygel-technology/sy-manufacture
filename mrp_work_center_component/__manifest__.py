# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "MRP Work Center Component",
    "summary": (
        "Add a Components tab in Work Center form to define needed "
        "products and quantities."
    ),
    "version": "17.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://github.com/sygel-technology/sy-manufacture",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mrp", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_workcenter_views.xml",
        "views/mrp_production_views.xml",
    ],
}
