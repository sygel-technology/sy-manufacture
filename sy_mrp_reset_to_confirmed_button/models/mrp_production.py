# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_is_zero


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    action_unstart_available = fields.Boolean(
        compute="_compute_action_unstart_available"
    )

    def _compute_action_unstart_available(self):
        for rec in self:
            rec.action_unstart_available = (
                rec.state == "progress"
                and not any(
                    wo_state in ("progress", "done")
                    for wo_state in rec.workorder_ids.mapped("state")
                )
                and (
                    not rec.product_uom_id
                    or float_is_zero(
                        rec.qty_producing,
                        precision_rounding=rec.product_uom_id.rounding,
                    )
                )
                and not any(rec.move_raw_ids.mapped("picked"))
            )

    def action_unstart(self):
        self.filtered("action_unstart_available").write({"state": "confirmed"})
        return True
