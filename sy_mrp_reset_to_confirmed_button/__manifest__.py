# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "SY MRP Reset to Confirmed Button",
    "summary": "Adds a button in MRP Orders to reset status to confirmed",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://github.com/sygel-technology/sy-manufacture",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mrp",
    ],
    "data": [
        "views/mrp_production.xml",
    ],
}
