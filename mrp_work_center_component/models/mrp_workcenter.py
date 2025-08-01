# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    component_line_ids = fields.One2many(
        "mrp.workcenter.component",
        "work_center_id",
        string="Components",
        domain="[('company_id', '=', company_id)]",
    )


class MrpWorkCenterComponent(models.Model):
    _name = "mrp.workcenter.component"

    name = fields.Char(compute="_compute_name", store=True)
    work_center_id = fields.Many2one("mrp.workcenter", string="Work Center")
    product_id = fields.Many2one(
        "product.product",
        domain="[('type', 'in', ['product', 'consu'])]",
    )
    quantity = fields.Float()
    product_uom_id = fields.Many2one(
        "uom.uom",
        related="product_id.uom_id",
        readonly=True,
        store=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True, required=True
    )

    @api.depends("product_id", "quantity")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.product_id.display_name} ({record.quantity})"
