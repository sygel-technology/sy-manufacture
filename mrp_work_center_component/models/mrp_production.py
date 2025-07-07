# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model_create_multi
    def create(self, vals_list):
        productions = super().create(vals_list)
        productions._add_workcenter_components()
        return productions

    def write(self, vals):
        res = super().write(vals)
        if "workorder_ids" in vals or "some_workcenter_field" in vals:
            self._update_workcenter_components()
        return res

    def _update_workcenter_components(self):
        for production in self:
            old_moves = self.env["stock.move"].search(
                [
                    ("raw_material_production_id", "=", production.id),
                    ("additional", "=", True),
                ]
            )
            old_moves.unlink()
            production._add_workcenter_components()

    def _add_workcenter_components(self):
        StockMove = self.env["stock.move"]
        WorkcenterComponent = self.env["mrp.workcenter.component"]

        for production in self:
            components = WorkcenterComponent.search(
                [
                    (
                        "work_center_id",
                        "in",
                        production.workorder_ids.mapped("workcenter_id").ids,
                    )
                ]
            )
            move_vals = []
            for component in components:
                move_vals.append(
                    {
                        "name": component.product_id.display_name,
                        "product_id": component.product_id.id,
                        "product_uom_qty": component.quantity,
                        "product_uom": component.product_id.uom_id.id,
                        "location_id": production.location_src_id.id,
                        "location_dest_id": production.production_location_id.id,
                        "raw_material_production_id": production.id,
                        "company_id": production.company_id.id,
                        "picking_type_id": production.picking_type_id.id,
                        "state": "draft",
                        "additional": True,
                    }
                )
            if move_vals:
                StockMove.create(move_vals)
