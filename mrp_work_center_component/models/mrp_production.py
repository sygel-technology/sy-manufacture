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

    def _add_workcenter_components(self, workcenter_id=None):
        StockMove = self.env["stock.move"]

        for production in self:
            if workcenter_id:
                components = (
                    self.env["mrp.workcenter"].browse(workcenter_id).component_line_ids
                )
            else:
                components = production.workorder_ids.mapped(
                    "workcenter_id.component_line_ids"
                )

            move_vals = [
                production._prepare_workcenter_component_move_vals(
                    component, additional=not workcenter_id
                )
                for component in components
            ]
            if move_vals:
                StockMove.create(move_vals)

    def _prepare_workcenter_component_move_vals(self, component, additional=False):
        return {
            "name": component.product_id.display_name,
            "product_id": component.product_id.id,
            "product_uom_qty": component.quantity,
            "product_uom": component.product_id.uom_id.id,
            "location_id": self.location_src_id.id,
            "location_dest_id": self.production_location_id.id,
            "raw_material_production_id": self.id,
            "company_id": self.company_id.id,
            "picking_type_id": self.picking_type_id.id,
            "state": "draft",
            "additional": additional,
        }
