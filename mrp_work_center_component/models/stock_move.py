from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    workcenter_id = fields.Many2one("mrp.workcenter", string="Centro de trabajo")
