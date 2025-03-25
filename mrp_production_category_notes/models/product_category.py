# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    mrp_notes = fields.Html(
        string="Manufacturing order notes",
        help="Add notes to manufacturing orders",
        translate=True,
    )

    def get_mrp_notes(self):
        self.ensure_one()
        mrp_notes = ""

        if self.mrp_notes and self.mrp_notes != "<p><br></p>":
            mrp_notes = self.mrp_notes
        elif self.parent_id:
            mrp_notes = self.parent_id.get_mrp_notes()
        return mrp_notes
