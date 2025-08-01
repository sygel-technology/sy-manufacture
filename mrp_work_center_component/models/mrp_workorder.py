# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    production_state = fields.Selection(
        related="production_id.state",
        store=True,
        readonly=True,
    )

    def _remove_old_components(self, old_workcenter_id):
        for workorder in self:
            production = workorder.production_id
            if not production:
                continue

            old_components = self.env["mrp.workcenter.component"].search(
                [
                    ("work_center_id", "=", old_workcenter_id),
                ]
            )
            product_ids = old_components.mapped("product_id").ids

            moves_to_delete = self.env["stock.move"].search(
                [
                    ("raw_material_production_id", "=", production.id),
                    ("product_id", "in", product_ids),
                    ("state", "in", ["draft"]),
                ]
            )

            if moves_to_delete:
                moves_to_delete.unlink()

    def write(self, vals):
        workorders_to_update = []
        if "workcenter_id" in vals:
            for workorder in self:
                old_workcenter_id = workorder._origin.workcenter_id.id
                new_workcenter_id = vals["workcenter_id"]
                if old_workcenter_id != new_workcenter_id:
                    workorders_to_update.append(
                        (workorder, old_workcenter_id, new_workcenter_id)
                    )
        res = super().write(vals)
        for workorder, old_wc_id, new_wc_id in workorders_to_update:
            production = workorder.production_id
            workorder._remove_old_components(old_wc_id)
            production._add_workcenter_components(workcenter_id=new_wc_id)
        return res
