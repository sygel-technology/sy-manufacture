# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    currency_id = fields.Many2one(related="bom_id.currency_id", store=True)
    cost_unit = fields.Float(
        string="Unit Cost", compute="_compute_cost_unit", store=True
    )
    cost_subtotal = fields.Float(
        string="Subtotal Cost", compute="_compute_cost_subtotal", store=True
    )

    @api.depends(
        "product_id.standard_price",
        "product_id.uom_id",
        "product_id.currency_id",
        "product_uom_id",
        "currency_id",
    )
    def _compute_cost_unit(self):
        for rec in self:
            if rec.product_id:
                cost_unit = product_cost_unit = rec.product_id.standard_price
                product_uom = rec.product_uom_id
                product_currency = rec.currency_id
                if product_uom != rec.product_id.uom_id:
                    cost_unit = rec.product_id.uom_id._compute_price(
                        product_cost_unit, product_uom
                    )
                if product_currency != rec.product_id.currency_id:
                    cost_unit = product_currency._convert(
                        cost_unit, rec.product_id.currency_id
                    )
            else:
                cost_unit = 0
            rec.cost_unit = cost_unit

    @api.depends("cost_unit", "product_qty")
    def _compute_cost_subtotal(self):
        for rec in self:
            rec.cost_subtotal = rec.cost_unit * rec.product_qty
