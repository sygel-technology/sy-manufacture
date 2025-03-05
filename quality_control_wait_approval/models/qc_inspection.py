# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    def action_confirm(self):
        res = super().action_confirm()
        self.write({"state": "waiting"})
        return res
