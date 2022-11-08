# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    priority = fields.Selection(
        selection_add=[
            ("2", "Very Urgent"),
        ]
    )
