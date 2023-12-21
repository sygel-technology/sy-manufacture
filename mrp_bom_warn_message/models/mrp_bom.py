# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    production_warn = fields.Selection(
        selection=[
            ('no-message', 'No Message'),
            ('warning', 'Warning')
        ],
        string='Production Warnings',
        default='no-message',
        help='''
            Selecting the "Warning" option will notify user with the message.
            The Message has to be written in the next field.
        '''
    )
    production_warn_msg = fields.Text(
        string='Message for Production Warn'
    )
