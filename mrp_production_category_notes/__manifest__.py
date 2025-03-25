# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "MRP Production Category Notes",
    "version": "15.0.1.0.0",
    "category": "Manufacturing",
    "summary": (
        "This module adds a new field to product categories "
        "that allows adding notes to mrp orders."
    ),
    "website": "https://github.com/sygel-technology/sy-manufacture",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["mrp_production_note"],
    "data": [
        "views/product_category_views.xml",
    ],
    "installable": True,
}
