# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        compute="_compute_currency_id",
        store=True,
        precompute=True,
        ondelete="restrict",
    )
    cost_subtotal = fields.Float(
        string="Subtotal Cost", compute="_compute_cost_subtotal", store=True
    )

    @api.depends("company_id")
    def _compute_currency_id(self):
        for rec in self:
            rec.currency_id = (
                rec.company_id.currency_id
                or self.env["res.company"]._get_main_company().currency_id.id
            )

    @api.depends("bom_line_ids.cost_subtotal")
    def _compute_cost_subtotal(self):
        for rec in self:
            domain = [("id", "in", rec.bom_line_ids.ids)]
            fields = ["cost_subtotal:sum"]
            groupby = ["bom_id"]
            rec.cost_subtotal = self.env["mrp.bom.line"].read_group(
                domain, fields, groupby
            )[0]["cost_subtotal"]
