# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = self.env["product.product"].browse(vals.get("product_id"))
            if product_id.exists() and product_id.categ_id:
                mrp_notes = product_id.categ_id.get_mrp_notes()
                if mrp_notes:
                    if vals.get("notes", "") in ["", "<p><br></p>"]:
                        vals["notes"] = mrp_notes
                    else:
                        vals["notes"] = f"{vals.get('notes', '')}\n{mrp_notes}"
        return super().create(vals_list)
